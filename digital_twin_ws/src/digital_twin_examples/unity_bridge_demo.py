#!/usr/bin/env python3

"""
Unity Bridge Demo for Digital Twin

This script demonstrates how to bridge data between ROS 2 and Unity
for visualization purposes. This is a simulation of the bridge functionality
since actual Unity integration requires the Unity environment.
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState, LaserScan, Imu
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import socket
import json
import threading
import time


class UnityBridgeDemo(Node):
    def __init__(self):
        super().__init__('unity_bridge_demo')

        # Subscription to robot data
        self.joint_sub = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_callback,
            10
        )

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

        # Publishers for Unity commands
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        # Simulated Unity connection (in real implementation, this would connect to Unity)
        self.unity_connected = False
        self.unity_socket = None

        self.get_logger().info('Unity Bridge Demo Node Started')
        self.get_logger().info('Simulating connection between ROS 2 and Unity')

        # Start simulated Unity connection thread
        self.unity_thread = threading.Thread(target=self.simulate_unity_connection)
        self.unity_thread.daemon = True
        self.unity_thread.start()

    def joint_callback(self, msg):
        """Handle joint state messages"""
        # In a real implementation, this would send joint data to Unity
        if self.unity_connected:
            joint_data = {
                'type': 'joint_state',
                'timestamp': self.get_clock().now().nanoseconds,
                'joints': {}
            }

            for i, name in enumerate(msg.name):
                if i < len(msg.position):
                    joint_data['joints'][name] = msg.position[i]

            self.send_to_unity(joint_data)

    def laser_callback(self, msg):
        """Handle laser scan messages"""
        # In a real implementation, this would send laser data to Unity
        if self.unity_connected:
            laser_data = {
                'type': 'laser_scan',
                'timestamp': self.get_clock().now().nanoseconds,
                'ranges': msg.ranges[:100],  # Limit for performance
                'angle_min': msg.angle_min,
                'angle_max': msg.angle_max,
                'angle_increment': msg.angle_increment
            }

            self.send_to_unity(laser_data)

    def imu_callback(self, msg):
        """Handle IMU messages"""
        # In a real implementation, this would send IMU data to Unity
        if self.unity_connected:
            imu_data = {
                'type': 'imu',
                'timestamp': self.get_clock().now().nanoseconds,
                'orientation': {
                    'x': msg.orientation.x,
                    'y': msg.orientation.y,
                    'z': msg.orientation.z,
                    'w': msg.orientation.w
                },
                'angular_velocity': {
                    'x': msg.angular_velocity.x,
                    'y': msg.angular_velocity.y,
                    'z': msg.angular_velocity.z
                },
                'linear_acceleration': {
                    'x': msg.linear_acceleration.x,
                    'y': msg.linear_acceleration.y,
                    'z': msg.linear_acceleration.z
                }
            }

            self.send_to_unity(imu_data)

    def simulate_unity_connection(self):
        """Simulate Unity connection (in real implementation, this would be a TCP server/client)"""
        self.unity_connected = True
        self.get_logger().info('✅ Simulated Unity connection established')

        # In a real implementation, this would be a TCP server listening for Unity connections
        # For this demo, we just simulate the connection state
        while rclpy.ok():
            time.sleep(1)

    def send_to_unity(self, data):
        """Send data to Unity (simulated)"""
        # In real implementation, this would serialize and send data via TCP
        self.get_logger().debug(f'Simulated sending to Unity: {data["type"]}')


def main(args=None):
    rclpy.init(args=args)

    unity_bridge = UnityBridgeDemo()

    try:
        rclpy.spin(unity_bridge)
    except KeyboardInterrupt:
        unity_bridge.get_logger().info('Unity Bridge Demo interrupted by user')
    finally:
        unity_bridge.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()