#!/usr/bin/env python3

"""
Performance Benchmarking Tool for Digital Twin Simulation

This script benchmarks the simulation performance to verify
the 30+ FPS requirement and other performance metrics.
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState, Image, LaserScan
from std_msgs.msg import Float64, Header
from builtin_interfaces.msg import Time
import time
import statistics
from collections import deque


class PerformanceBenchmark(Node):
    def __init__(self):
        super().__init__('performance_benchmark')

        # Performance tracking
        self.joint_timestamps = deque(maxlen=100)
        self.image_timestamps = deque(maxlen=100)
        self.laser_timestamps = deque(maxlen=100)

        self.joint_frequencies = deque(maxlen=50)
        self.image_frequencies = deque(maxlen=50)
        self.laser_frequencies = deque(maxlen=50)

        # Subscriptions to monitor update rates
        self.joint_sub = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_callback,
            10
        )

        self.image_sub = self.create_subscription(
            Image,
            '/depth_cam/rgb/image_raw',
            self.image_callback,
            10
        )

        self.laser_sub = self.create_subscription(
            LaserScan,
            '/scan',
            self.laser_callback,
            10
        )

        # Publishers for performance metrics
        self.fps_pub = self.create_publisher(Float64, '/performance/fps', 10)
        self.joint_rate_pub = self.create_publisher(Float64, '/performance/joint_rate', 10)
        self.cpu_usage_pub = self.create_publisher(Float64, '/performance/cpu_usage', 10)

        # Timer for publishing performance metrics
        self.timer = self.create_timer(2.0, self.publish_performance_metrics)
        self.benchmark_start_time = time.time()

        self.get_logger().info('Performance Benchmark Node Started')
        self.get_logger().info('Monitoring simulation performance...')

    def joint_callback(self, msg):
        """Track joint state update frequency"""
        current_time = time.time()
        self.joint_timestamps.append(current_time)

        # Calculate frequency if we have enough data
        if len(self.joint_timestamps) >= 2:
            time_diffs = [self.joint_timestamps[i] - self.joint_timestamps[i-1]
                         for i in range(1, len(self.joint_timestamps))]
            if time_diffs:
                avg_period = statistics.mean(time_diffs)
                freq = 1.0 / avg_period if avg_period > 0 else 0
                self.joint_frequencies.append(freq)

    def image_callback(self, msg):
        """Track image update frequency"""
        current_time = time.time()
        self.image_timestamps.append(current_time)

        # Calculate frequency if we have enough data
        if len(self.image_timestamps) >= 2:
            time_diffs = [self.image_timestamps[i] - self.image_timestamps[i-1]
                         for i in range(1, len(self.image_timestamps))]
            if time_diffs:
                avg_period = statistics.mean(time_diffs)
                freq = 1.0 / avg_period if avg_period > 0 else 0
                self.image_frequencies.append(freq)

    def laser_callback(self, msg):
        """Track laser scan update frequency"""
        current_time = time.time()
        self.laser_timestamps.append(current_time)

        # Calculate frequency if we have enough data
        if len(self.laser_timestamps) >= 2:
            time_diffs = [self.laser_timestamps[i] - self.laser_timestamps[i-1]
                         for i in range(1, len(self.laser_timestamps))]
            if time_diffs:
                avg_period = statistics.mean(time_diffs)
                freq = 1.0 / avg_period if avg_period > 0 else 0
                self.laser_frequencies.append(freq)

    def publish_performance_metrics(self):
        """Publish current performance metrics"""
        # Calculate FPS based on image frequency (primary visual indicator)
        avg_image_freq = 0
        if self.image_frequencies:
            avg_image_freq = statistics.mean(list(self.image_frequencies)[-10:])  # Last 10 samples

        # Calculate joint state frequency
        avg_joint_freq = 0
        if self.joint_frequencies:
            avg_joint_freq = statistics.mean(list(self.joint_frequencies)[-10:])

        # Calculate laser frequency
        avg_laser_freq = 0
        if self.laser_frequencies:
            avg_laser_freq = statistics.mean(list(self.laser_frequencies)[-10:])

        # Publish FPS
        fps_msg = Float64()
        fps_msg.data = float(avg_image_freq)
        self.fps_pub.publish(fps_msg)

        # Publish joint rate
        joint_rate_msg = Float64()
        joint_rate_msg.data = float(avg_joint_freq)
        self.joint_rate_pub.publish(joint_rate_msg)

        # Publish CPU usage estimate (simulated)
        cpu_msg = Float64()
        # Simulate CPU usage based on performance (higher FPS = lower CPU in simulation)
        cpu_usage = max(0.0, min(100.0, 100.0 - (avg_image_freq * 2)))  # Inverted relationship for simulation
        cpu_msg.data = cpu_usage
        self.cpu_usage_pub.publish(cpu_msg)

        # Log performance metrics
        self.get_logger().info(f'\n--- Performance Metrics ---')
        self.get_logger().info(f'Image Frequency: {avg_image_freq:.2f} Hz')
        self.get_logger().info(f'Joint Frequency: {avg_joint_freq:.2f} Hz')
        self.get_logger().info(f'Laser Frequency: {avg_laser_freq:.2f} Hz')
        self.get_logger().info(f'Estimated CPU Usage: {cpu_usage:.2f}%')

        # Performance assessment
        fps_requirement_met = avg_image_freq >= 30
        control_requirement_met = avg_joint_freq >= 50  # Control loop should be higher

        if fps_requirement_met:
            self.get_logger().info(f'✅ FPS requirement met: {avg_image_freq:.2f} Hz >= 30 Hz')
        else:
            self.get_logger().warn(f'❌ FPS requirement not met: {avg_image_freq:.2f} Hz < 30 Hz')

        if control_requirement_met:
            self.get_logger().info(f'✅ Control rate requirement met: {avg_joint_freq:.2f} Hz >= 50 Hz')
        else:
            self.get_logger().warn(f'❌ Control rate requirement not met: {avg_joint_freq:.2f} Hz < 50 Hz')

        # Overall performance assessment
        if fps_requirement_met and control_requirement_met:
            self.get_logger().info(f'🎉 Overall performance target achieved!')
        else:
            self.get_logger().info(f'⚠️  Performance optimization may be needed')

    def get_performance_summary(self):
        """Return a summary of performance metrics"""
        summary = {
            'runtime_seconds': time.time() - self.benchmark_start_time,
            'image_frequency_avg': statistics.mean(self.image_frequencies) if self.image_frequencies else 0,
            'joint_frequency_avg': statistics.mean(self.joint_frequencies) if self.joint_frequencies else 0,
            'laser_frequency_avg': statistics.mean(self.laser_frequencies) if self.laser_frequencies else 0,
            'fps_target_met': (statistics.mean(self.image_frequencies) if self.image_frequencies else 0) >= 30
        }
        return summary


def main(args=None):
    rclpy.init(args=args)

    benchmark = PerformanceBenchmark()

    try:
        rclpy.spin(benchmark)
    except KeyboardInterrupt:
        benchmark.get_logger().info('Performance benchmark interrupted by user')

        # Print final summary
        summary = benchmark.get_performance_summary()
        benchmark.get_logger().info(f'\n=== FINAL PERFORMANCE SUMMARY ===')
        benchmark.get_logger().info(f'Runtime: {summary["runtime_seconds"]:.2f} seconds')
        benchmark.get_logger().info(f'Average Image Frequency: {summary["image_frequency_avg"]:.2f} Hz')
        benchmark.get_logger().info(f'Average Joint Frequency: {summary["joint_frequency_avg"]:.2f} Hz')
        benchmark.get_logger().info(f'Average Laser Frequency: {summary["laser_frequency_avg"]:.2f} Hz')
        benchmark.get_logger().info(f'FPS Target (30Hz) Met: {summary["fps_target_met"]}')

    finally:
        benchmark.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()