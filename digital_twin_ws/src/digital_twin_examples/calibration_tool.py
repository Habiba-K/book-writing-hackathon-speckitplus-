#!/usr/bin/env python3

"""
Calibration Tool for Digital Twin Sensors

This script implements calibration tools for sensor validation
against theoretical physics calculations.
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan, Imu, PointCloud2
from geometry_msgs.msg import Vector3
from std_msgs.msg import Float64
import numpy as np
import math
from scipy.spatial.transform import Rotation as R


class CalibrationTool(Node):
    def __init__(self):
        super().__init__('calibration_tool')

        # Sensor data storage for calibration
        self.laser_data_history = []
        self.imu_data_history = []
        self.calibration_step = 0

        # Subscriptions to sensor topics
        self.laser_sub = self.create_subscription(
            LaserScan,
            '/scan',
            self.laser_callback,
            10
        )

        self.imu_sub = self.create_subscription(
            Imu,
            '/imu/data',
            self.imu_callback,
            10
        )

        # Publishers for calibration results
        self.calibration_pub = self.create_publisher(
            Float64,
            '/calibration/accuracy',
            10
        )

        # Timer for calibration process
        self.timer = self.create_timer(5.0, self.run_calibration_step)
        self.calibration_count = 0

        self.get_logger().info('Calibration Tool Node Started')
        self.get_logger().info('Starting sensor calibration process...')

    def laser_callback(self, msg):
        """Callback for laser scan data"""
        # Store laser data for calibration analysis
        self.laser_data_history.append({
            'timestamp': self.get_clock().now().nanoseconds,
            'ranges': msg.ranges,
            'intensities': msg.intensities,
            'angle_min': msg.angle_min,
            'angle_max': msg.angle_max,
            'angle_increment': msg.angle_increment
        })

        # Keep only recent data to avoid memory issues
        if len(self.laser_data_history) > 100:
            self.laser_data_history = self.laser_data_history[-50:]

    def imu_callback(self, msg):
        """Callback for IMU data"""
        # Store IMU data for calibration analysis
        self.imu_data_history.append({
            'timestamp': msg.header.stamp.sec * 1e9 + msg.header.stamp.nanosec,
            'orientation': msg.orientation,
            'angular_velocity': msg.angular_velocity,
            'linear_acceleration': msg.linear_acceleration
        })

        # Keep only recent data to avoid memory issues
        if len(self.imu_data_history) > 100:
            self.imu_data_history = self.imu_data_history[-50:]

    def validate_laser_calibration(self):
        """Validate LiDAR sensor calibration against theoretical values"""
        if len(self.laser_data_history) < 5:
            self.get_logger().warn('Insufficient laser data for calibration')
            return 0.0

        # Get the most recent laser scan
        recent_scan = self.laser_data_history[-1]

        # Check if ranges are within expected bounds based on our world
        # In our world file, we have test objects at known positions
        valid_ranges = [r for r in recent_scan['ranges']
                       if not (math.isnan(r) or math.isinf(r)) and r > 0]

        if not valid_ranges:
            self.get_logger().warn('No valid laser ranges found')
            return 0.0

        # Calculate statistics
        avg_range = sum(valid_ranges) / len(valid_ranges)
        min_range = min(valid_ranges)
        max_range = max(valid_ranges)

        # Theoretical validation: our test box is at position (2, 0, 0.5)
        # So distance should be approximately sqrt(2^2 + 0^2) = 2m
        expected_distance_box = 2.0
        distance_error_box = abs(avg_range - expected_distance_box)

        # If we have a measurement close to the expected distance, calibration is good
        calibration_score = 0.0
        if distance_error_box < 0.5:  # Within 50cm tolerance
            calibration_score = 1.0 - (distance_error_box / 0.5)
        else:
            calibration_score = max(0.0, 1.0 - (distance_error_box / 2.0))  # Lower score for larger errors

        self.get_logger().info(f'LiDAR calibration - Avg range: {avg_range:.2f}m, Expected: {expected_distance_box}m, Score: {calibration_score:.2f}')

        return min(calibration_score, 1.0)

    def validate_imu_calibration(self):
        """Validate IMU sensor calibration against theoretical values"""
        if len(self.imu_data_history) < 5:
            self.get_logger().warn('Insufficient IMU data for calibration')
            return 0.0

        # Get the most recent IMU data
        recent_imu = self.imu_data_history[-1]

        # Check if orientation quaternion is normalized
        orientation = recent_imu['orientation']
        norm = math.sqrt(orientation.x**2 + orientation.y**2 + orientation.z**2 + orientation.w**2)

        # When robot is static, the IMU should show gravity in the Z direction
        accel = recent_imu['linear_acceleration']
        gravity_magnitude = math.sqrt(accel.x**2 + accel.y**2 + accel.z**2)

        # For calibration, we expect the robot to be mostly static
        # Check if acceleration magnitude is close to gravity (9.8 m/s^2)
        gravity_error = abs(gravity_magnitude - 9.8)

        # Calculate calibration score based on both normalization and gravity
        norm_score = max(0.0, 1.0 - abs(norm - 1.0))
        gravity_score = max(0.0, 1.0 - (gravity_error / 2.0))  # Allow 2 m/s^2 tolerance

        # Average the scores
        calibration_score = (norm_score + gravity_score) / 2.0

        self.get_logger().info(f'IMU calibration - Gravity: {gravity_magnitude:.2f} m/s², Norm: {norm:.3f}, Score: {calibration_score:.2f}')

        return min(calibration_score, 1.0)

    def run_calibration_step(self):
        """Run one step of the calibration process"""
        self.get_logger().info(f'\n--- Calibration Step #{self.calibration_count + 1} ---')

        # Validate different sensors
        lidar_score = self.validate_laser_calibration()
        imu_score = self.validate_imu_calibration()

        # Calculate overall calibration score
        overall_score = (lidar_score + imu_score) / 2.0

        # Publish the overall calibration accuracy
        accuracy_msg = Float64()
        accuracy_msg.data = overall_score
        self.calibration_pub.publish(accuracy_msg)

        self.get_logger().info(f'Calibration Results:')
        self.get_logger().info(f'  LiDAR: {lidar_score:.2f}')
        self.get_logger().info(f'  IMU: {imu_score:.2f}')
        self.get_logger().info(f'  Overall: {overall_score:.2f}')

        # Log status based on score
        if overall_score > 0.8:
            self.get_logger().info('✅ Excellent calibration - sensors are well calibrated')
        elif overall_score > 0.6:
            self.get_logger().info('✅ Good calibration - acceptable for most applications')
        elif overall_score > 0.4:
            self.get_logger().info('⚠️  Fair calibration - may need adjustment')
        else:
            self.get_logger().info('❌ Poor calibration - requires recalibration')

        self.calibration_count += 1

        # After several calibration steps, if scores are good, indicate success
        if self.calibration_count >= 5 and overall_score > 0.7:
            self.get_logger().info('\n🎯 Calibration successful - sensors validated against theoretical physics!')
            self.timer.cancel()


def main(args=None):
    rclpy.init(args=args)

    calibration_tool = CalibrationTool()

    try:
        rclpy.spin(calibration_tool)
    except KeyboardInterrupt:
        calibration_tool.get_logger().info('Calibration tool interrupted by user')
    finally:
        calibration_tool.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()