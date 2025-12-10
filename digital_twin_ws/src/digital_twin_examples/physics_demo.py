#!/usr/bin/env python3

"""
Physics Demo for Digital Twin Simulation

This script demonstrates various physics scenarios in the simulation,
including falling objects and collision responses.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist
from sensor_msgs.msg import JointState
import time
import math


class PhysicsDemo(Node):
    def __init__(self):
        super().__init__('physics_demo')

        # Publisher for joint commands
        self.joint_cmd_publisher = self.create_publisher(
            JointState,
            '/joint_commands',
            10
        )

        # Timer for demonstration
        self.timer = self.create_timer(0.1, self.demo_callback)
        self.demo_step = 0

        self.get_logger().info('Physics Demo Node Started')

    def demo_callback(self):
        """Execute different physics scenarios based on step"""
        if self.demo_step == 0:
            self.get_logger().info('Demonstrating: Gravity and Falling Object')
            self.demo_gravity()
        elif self.demo_step == 1:
            self.get_logger().info('Demonstrating: Joint Damping and Friction')
            self.demo_joint_dynamics()
        elif self.demo_step == 2:
            self.get_logger().info('Demonstrating: Collision Response')
            self.demo_collision()

        self.demo_step = (self.demo_step + 1) % 3

    def demo_gravity(self):
        """Demonstrate gravity effects on objects"""
        # In a real scenario, this would spawn objects and observe their fall
        # For this demo, we'll just log what would happen
        self.get_logger().info('Gravity demo: Objects fall at 9.8 m/s² acceleration')
        self.get_logger().info('With damping, objects reach terminal velocity')

    def demo_joint_dynamics(self):
        """Demonstrate joint dynamics (damping, friction)"""
        # Create a joint state message to command movement
        msg = JointState()
        msg.name = ['left_shoulder_joint', 'right_shoulder_joint']
        msg.position = [0.5, -0.5]
        msg.velocity = [0.0, 0.0]
        msg.effort = [0.0, 0.0]

        # Add timestamp
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'

        self.joint_cmd_publisher.publish(msg)

        self.get_logger().info('Joint dynamics demo: Moving shoulders with damping/friction')

    def demo_collision(self):
        """Demonstrate collision response"""
        # In a real scenario, this would create collision scenarios
        # For this demo, we'll just log what would happen
        self.get_logger().info('Collision demo: Objects respond to contact based on material properties')
        self.get_logger().info('Proper collision geometry ensures realistic contact detection')


def main(args=None):
    rclpy.init(args=args)

    physics_demo = PhysicsDemo()

    try:
        rclpy.spin(physics_demo)
    except KeyboardInterrupt:
        physics_demo.get_logger().info('Physics Demo interrupted by user')
    finally:
        physics_demo.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()