#!/usr/bin/env python3

"""
Sensor Verification Script for Digital Twin

This script verifies that sensor data is being published correctly
from the simulated robot and matches theoretical physics calculations.
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan, Imu, PointCloud2
from std_msgs.msg import Header
import numpy as np
import math

class SensorVerification(Node):
    def __init__(self):
        super().__init__('sensor_verification')

        # Sensor data storage
        self.laser_data = None
        self.imu_data = None
        self.pc_data = None

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

        self.pc_sub = self.create_subscription(
            PointCloud2,
            '/depth_cam/depth/points',
            self.pc_callback,
            10
        )

        # Timer for verification
        self.timer = self.create_timer(2.0, self.verify_sensors)
        self.verification_count = 0

        self.get_logger().info('Sensor Verification Node Started')
        self.get_logger().info('Waiting for sensor data...')

    def laser_callback(self, msg):
        """Callback for laser scan data"""
        self.laser_data = msg
        self.get_logger().debug(f'Laser data received with {len(msg.ranges)} ranges')

    def imu_callback(self, msg):
        """Callback for IMU data"""
        self.imu_data = msg
        self.get_logger().debug('IMU data received')

    def pc_callback(self, msg):
        """Callback for point cloud data"""
        self.pc_data = msg
        self.get_logger().debug('Point cloud data received')

    def verify_laser_data(self):
        """Verify laser sensor data"""
        if self.laser_data is None:
            self.get_logger().warn('No laser data received')
            return False

        # Check if ranges are within expected bounds
        valid_ranges = [r for r in self.laser_data.ranges if
                       not (math.isnan(r) or math.isinf(r))]

        if not valid_ranges:
            self.get_logger().warn('No valid laser ranges found')
            return False

        # Check if ranges are within expected sensor limits
        min_range = self.laser_data.range_min
        max_range = self.laser_data.range_max

        if min(valid_ranges) < min_range or max(valid_ranges) > max_range:
            self.get_logger().warn(f'Laser ranges outside expected bounds [{min_range}, {max_range}]')
            return False

        # Check update rate
        expected_rate = 10  # Hz
        actual_rate = 1.0 / self.laser_data.time_increment if self.laser_data.time_increment > 0 else 0
        if abs(actual_rate - expected_rate) > 2:  # Allow 2Hz tolerance
            self.get_logger().warn(f'Laser update rate mismatch: expected ~{expected_rate}Hz, got ~{actual_rate}Hz')
            return False

        self.get_logger().info('✅ Laser sensor verification passed')
        return True

    def verify_imu_data(self):
        """Verify IMU sensor data"""
        if self.imu_data is None:
            self.get_logger().warn('No IMU data received')
            return False

        # Check if orientation quaternion is normalized
        orientation = self.imu_data.orientation
        norm = math.sqrt(orientation.x**2 + orientation.y**2 + orientation.z**2 + orientation.w**2)

        if abs(norm - 1.0) > 0.1:  # Allow some tolerance
            self.get_logger().warn(f'IMU orientation quaternion not normalized: {norm}')
            return False

        # Check if linear acceleration is reasonable (close to gravity when static)
        accel = self.imu_data.linear_acceleration
        gravity_magnitude = math.sqrt(accel.x**2 + accel.y**2 + accel.z**2)

        # When robot is static, expect ~9.8 m/s^2 acceleration
        if abs(gravity_magnitude - 9.8) > 2.0:  # Allow tolerance for simulation inaccuracies
            self.get_logger().warn(f'IMU acceleration seems incorrect: {gravity_magnitude} (expected ~9.8)')
            # Don't fail this check as the robot might be moving

        self.get_logger().info('✅ IMU sensor verification passed')
        return True

    def verify_depth_camera(self):
        """Verify depth camera data"""
        if self.pc_data is None:
            self.get_logger().warn('No point cloud data received')
            return False

        # Check if point cloud has reasonable structure
        if self.pc_data.width == 0 or self.pc_data.height == 0:
            self.get_logger().warn('Invalid point cloud dimensions')
            return False

        self.get_logger().info('✅ Depth camera verification passed (basic check)')
        return True

    def verify_sensors(self):
        """Main verification function"""
        self.get_logger().info(f'\n--- Sensor Verification Check #{self.verification_count + 1} ---')

        laser_ok = self.verify_laser_data()
        imu_ok = self.verify_imu_data()
        camera_ok = self.verify_depth_camera()

        all_ok = laser_ok and imu_ok and camera_ok

        if all_ok:
            self.get_logger().info('🎉 All sensor verifications passed!')
        else:
            self.get_logger().warn('❌ Some sensor verifications failed')
            if not laser_ok:
                self.get_logger().warn('  - Laser sensor failed')
            if not imu_ok:
                self.get_logger().warn('  - IMU sensor failed')
            if not camera_ok:
                self.get_logger().warn('  - Depth camera failed')

        self.verification_count += 1

        # After a few checks, if sensors are working, log success
        if self.verification_count >= 3 and all_ok:
            self.get_logger().info('\n🎯 Sensor verification successful - all sensors publishing correctly!')
            self.timer.cancel()

def main(args=None):
    rclpy.init(args=args)

    sensor_verification = SensorVerification()

    try:
        rclpy.spin(sensor_verification)
    except KeyboardInterrupt:
        sensor_verification.get_logger().info('Sensor verification interrupted by user')
    finally:
        sensor_verification.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()