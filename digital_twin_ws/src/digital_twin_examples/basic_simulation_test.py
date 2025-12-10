#!/usr/bin/env python3

"""
Basic Simulation Test Script

This script tests the basic Gazebo simulation setup by launching the simulation
and verifying that the robot spawns correctly in the environment.
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from tf2_msgs.msg import TFMessage
from std_msgs.msg import String
import subprocess
import time
import sys

class BasicSimulationTester(Node):
    def __init__(self):
        super().__init__('basic_simulation_tester')

        # Subscription to joint states to verify robot is publishing data
        self.joint_sub = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            10
        )

        # Subscription to TF to verify transforms are being published
        self.tf_sub = self.create_subscription(
            TFMessage,
            '/tf',
            self.tf_callback,
            10
        )

        self.joint_data_received = False
        self.tf_data_received = False

        self.get_logger().info('Basic Simulation Tester Node Started')
        self.get_logger().info('Waiting for simulation data to verify robot spawn...')

    def joint_state_callback(self, msg):
        """Callback for joint state messages"""
        if len(msg.name) > 0:
            self.joint_data_received = True
            self.get_logger().info(f'Received joint state data with {len(msg.name)} joints: {msg.name[:5]}...')

    def tf_callback(self, msg):
        """Callback for TF messages"""
        if len(msg.transforms) > 0:
            self.tf_data_received = True
            self.get_logger().info(f'Received TF data with {len(msg.transforms)} transforms')

    def run_simulation_test(self):
        """Run the basic simulation test"""
        # Wait for data to confirm robot has spawned
        start_time = time.time()
        timeout = 30  # 30 second timeout

        while time.time() - start_time < timeout:
            time.sleep(1)

            if self.joint_data_received and self.tf_data_received:
                self.get_logger().info('SUCCESS: Robot spawned correctly and is publishing data')
                self.get_logger().info('  - Joint states are being published')
                self.get_logger().info('  - TF transforms are being published')
                return True

        # If we get here, the test timed out
        if not self.joint_data_received:
            self.get_logger().error('ERROR: No joint state data received - robot may not have spawned correctly')

        if not self.tf_data_received:
            self.get_logger().error('ERROR: No TF data received - robot transforms may not be publishing')

        return False

def main(args=None):
    rclpy.init(args=args)

    tester = BasicSimulationTester()

    # Give some time for connections to establish
    time.sleep(5)

    try:
        # Run the simulation test in a separate thread while spinning
        import threading
        test_result = [False]  # Use a list to store result from thread

        def run_test():
            test_result[0] = tester.run_simulation_test()
            rclpy.shutdown()

        test_thread = threading.Thread(target=run_test)
        test_thread.start()

        rclpy.spin(tester)

        test_thread.join()

        if test_result[0]:
            print("BASIC SIMULATION TEST PASSED: Robot spawned correctly and is publishing data")
            return 0
        else:
            print("BASIC SIMULATION TEST FAILED: Robot may not have spawned correctly")
            return 1

    except KeyboardInterrupt:
        tester.get_logger().info('Basic Simulation Test interrupted by user')
        return 1
    finally:
        tester.destroy_node()

if __name__ == '__main__':
    result = main()
    sys.exit(result)