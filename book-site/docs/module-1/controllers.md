---
id: controllers
title: "Controllers"
sidebar_label: "Controllers"
sidebar_position: 6
---

# Chapter 6: Robot Controllers

## Learning Objectives

By the end of this chapter, you will be able to:

- Understand the role of controllers in robot systems
- Implement feedback control loops using ROS 2 Timer API
- Subscribe to sensor topics and publish actuator commands
- Create a PID controller for position control
- Implement velocity and trajectory controllers
- Handle control timing and synchronization

## Prerequisites

- Chapters 1-5 completion
- Understanding of topics and publishers/subscribers
- Basic control theory knowledge (helpful but not required)

## What is a Robot Controller?

A **controller** is a node that:
1. **Reads sensor data** (inputs) - current robot state
2. **Computes control commands** (processing) - desired actions
3. **Sends actuator commands** (outputs) - motor velocities, torques, etc.

Controllers implement the **sense-think-act** cycle that enables autonomous robot behavior.

### Controller Types

| Type | Input | Output | Example |
|------|-------|--------|---------|
| **Position** | Desired position | Joint commands | Move arm to specific pose |
| **Velocity** | Desired velocity | Motor speeds | Drive robot at 0.5 m/s |
| **Trajectory** | Path waypoints | Time-based commands | Follow planned path |
| **Feedback** | Sensor readings | Corrective actions | Balance using IMU |

## ROS 2 Timer API

Controllers run at fixed frequencies using timers. The Timer API ensures periodic execution.

```python
import rclpy
from rclpy.node import Node


class TimerExample(Node):
    def __init__(self):
        super().__init__('timer_example')

        # Create timer that calls callback every 0.1 seconds (10 Hz)
        self.timer_period = 0.1  # seconds
        self.timer = self.create_timer(self.timer_period, self.timer_callback)

        self.counter = 0

    def timer_callback(self):
        """
        Called every timer_period seconds.
        """
        self.counter += 1
        self.get_logger().info(f'Timer callback #{self.counter} at 10 Hz')


def main(args=None):
    rclpy.init(args=args)
    node = TimerExample()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Why Fixed Frequency Matters

- **Predictable behavior**: Control algorithms expect consistent timing
- **Stability**: Irregular timing can cause oscillations or instability
- **Synchronization**: Multiple controllers can coordinate at known rates

## Simple Velocity Controller

This controller reads desired velocity commands and forwards them to motors:

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64


class VelocityController(Node):
    """
    Simple velocity controller that converts Twist commands
    to individual wheel velocities for a differential drive robot.
    """

    def __init__(self):
        super().__init__('velocity_controller')

        # Robot parameters
        self.wheel_radius = 0.05  # meters
        self.wheel_separation = 0.3  # meters

        # Subscribe to velocity commands
        self.cmd_sub = self.create_subscription(
            Twist,
            'cmd_vel',
            self.cmd_callback,
            10
        )

        # Publish to individual wheel controllers
        self.left_wheel_pub = self.create_publisher(
            Float64,
            'left_wheel_velocity',
            10
        )
        self.right_wheel_pub = self.create_publisher(
            Float64,
            'right_wheel_velocity',
            10
        )

        # Control loop timer (100 Hz)
        self.timer = self.create_timer(0.01, self.control_loop)

        # Current command (updated by callback)
        self.linear_vel = 0.0
        self.angular_vel = 0.0

        self.get_logger().info('Velocity controller started at 100 Hz')

    def cmd_callback(self, msg):
        """
        Receive new velocity command.
        """
        self.linear_vel = msg.linear.x
        self.angular_vel = msg.angular.z

    def control_loop(self):
        """
        Compute and publish wheel velocities at fixed rate.
        """
        # Differential drive kinematics
        # v_left = (linear - angular * separation / 2) / radius
        # v_right = (linear + angular * separation / 2) / radius

        left_vel = (self.linear_vel - self.angular_vel * self.wheel_separation / 2) / self.wheel_radius
        right_vel = (self.linear_vel + self.angular_vel * self.wheel_separation / 2) / self.wheel_radius

        # Publish wheel velocities
        left_msg = Float64()
        left_msg.data = left_vel
        self.left_wheel_pub.publish(left_msg)

        right_msg = Float64()
        right_msg.data = right_vel
        self.right_wheel_pub.publish(right_msg)

        self.get_logger().debug(f'Left: {left_vel:.2f}, Right: {right_vel:.2f}')


def main(args=None):
    rclpy.init(args=args)
    node = VelocityController()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Testing the Controller

```bash
# Terminal 1: Start controller
python3 velocity_controller.py

# Terminal 2: Send velocity command
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.5}, angular: {z: 0.3}}"

# Monitor wheel velocities
ros2 topic echo /left_wheel_velocity
ros2 topic echo /right_wheel_velocity
```

## PID Position Controller

A PID (Proportional-Integral-Derivative) controller minimizes error between desired and actual positions.

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64


class PIDController(Node):
    """
    PID controller for single joint position control.
    Reads current position, computes error, outputs velocity command.
    """

    def __init__(self):
        super().__init__('pid_controller')

        # PID gains
        self.kp = 2.0   # Proportional gain
        self.ki = 0.1   # Integral gain
        self.kd = 0.5   # Derivative gain

        # Control state
        self.setpoint = 0.0        # Desired position (radians)
        self.current_position = 0.0  # Actual position (radians)
        self.error_integral = 0.0   # Accumulated error
        self.previous_error = 0.0   # Last error (for derivative)

        # Subscribe to current position
        self.position_sub = self.create_subscription(
            Float64,
            'joint_position',
            self.position_callback,
            10
        )

        # Subscribe to desired position
        self.setpoint_sub = self.create_subscription(
            Float64,
            'joint_setpoint',
            self.setpoint_callback,
            10
        )

        # Publish velocity command
        self.command_pub = self.create_publisher(
            Float64,
            'joint_velocity_command',
            10
        )

        # Control loop at 50 Hz
        self.dt = 0.02  # 20 ms
        self.timer = self.create_timer(self.dt, self.control_loop)

        self.get_logger().info('PID controller started')

    def position_callback(self, msg):
        """
        Update current position from sensor.
        """
        self.current_position = msg.data

    def setpoint_callback(self, msg):
        """
        Update desired position.
        """
        self.setpoint = msg.data
        self.get_logger().info(f'New setpoint: {self.setpoint:.3f} rad')

    def control_loop(self):
        """
        PID control computation at fixed rate.
        """
        # Compute error
        error = self.setpoint - self.current_position

        # Proportional term
        p_term = self.kp * error

        # Integral term (accumulated error over time)
        self.error_integral += error * self.dt
        # Anti-windup: limit integral term
        max_integral = 10.0
        self.error_integral = max(-max_integral, min(max_integral, self.error_integral))
        i_term = self.ki * self.error_integral

        # Derivative term (rate of error change)
        error_derivative = (error - self.previous_error) / self.dt
        d_term = self.kd * error_derivative

        # Total control output
        output = p_term + i_term + d_term

        # Limit output
        max_velocity = 5.0  # rad/s
        output = max(-max_velocity, min(max_velocity, output))

        # Publish command
        cmd_msg = Float64()
        cmd_msg.data = output
        self.command_pub.publish(cmd_msg)

        # Log for tuning
        self.get_logger().debug(
            f'Error: {error:.3f}, P: {p_term:.2f}, I: {i_term:.2f}, '
            f'D: {d_term:.2f}, Output: {output:.2f}'
        )

        # Store for next iteration
        self.previous_error = error


def main(args=None):
    rclpy.init(args=args)
    node = PIDController()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### PID Tuning Guide

1. **Start with P only** (Ki=0, Kd=0):
   - Increase Kp until system responds quickly
   - Too high → oscillations

2. **Add D term**:
   - Increase Kd to reduce oscillations
   - Provides damping

3. **Add I term**:
   - Increase Ki to eliminate steady-state error
   - Too high → instability

## Feedback Controller with Sensor Input

This controller uses LIDAR to avoid obstacles while moving toward a goal:

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, PoseStamped
from sensor_msgs.msg import LaserScan
import math


class ObstacleAvoidanceController(Node):
    """
    Controller that navigates to a goal while avoiding obstacles.
    Uses LIDAR for obstacle detection and implements reactive control.
    """

    def __init__(self):
        super().__init__('obstacle_avoidance_controller')

        # Control parameters
        self.max_linear_vel = 0.5   # m/s
        self.max_angular_vel = 1.0  # rad/s
        self.safe_distance = 0.5    # meters
        self.goal_tolerance = 0.1   # meters

        # State
        self.goal_x = 0.0
        self.goal_y = 0.0
        self.current_x = 0.0
        self.current_y = 0.0
        self.current_yaw = 0.0
        self.min_obstacle_distance = float('inf')

        # Subscribe to laser scan
        self.scan_sub = self.create_subscription(
            LaserScan,
            'scan',
            self.scan_callback,
            10
        )

        # Subscribe to current pose
        self.pose_sub = self.create_subscription(
            PoseStamped,
            'current_pose',
            self.pose_callback,
            10
        )

        # Subscribe to goal
        self.goal_sub = self.create_subscription(
            PoseStamped,
            'goal_pose',
            self.goal_callback,
            10
        )

        # Publish velocity commands
        self.cmd_pub = self.create_publisher(Twist, 'cmd_vel', 10)

        # Control loop at 20 Hz
        self.timer = self.create_timer(0.05, self.control_loop)

        self.get_logger().info('Obstacle avoidance controller started')

    def scan_callback(self, msg):
        """
        Process LIDAR scan to find closest obstacle.
        """
        valid_ranges = [r for r in msg.ranges if msg.range_min < r < msg.range_max]
        if valid_ranges:
            self.min_obstacle_distance = min(valid_ranges)
        else:
            self.min_obstacle_distance = float('inf')

    def pose_callback(self, msg):
        """
        Update current robot pose.
        """
        self.current_x = msg.pose.position.x
        self.current_y = msg.pose.position.y

        # Extract yaw from quaternion
        q = msg.pose.orientation
        siny_cosp = 2 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1 - 2 * (q.y * q.y + q.z * q.z)
        self.current_yaw = math.atan2(siny_cosp, cosy_cosp)

    def goal_callback(self, msg):
        """
        Update goal position.
        """
        self.goal_x = msg.pose.position.x
        self.goal_y = msg.pose.position.y
        self.get_logger().info(f'New goal: ({self.goal_x:.2f}, {self.goal_y:.2f})')

    def control_loop(self):
        """
        Main control loop: compute velocity to reach goal while avoiding obstacles.
        """
        # Compute distance and angle to goal
        dx = self.goal_x - self.current_x
        dy = self.goal_y - self.current_y
        distance_to_goal = math.sqrt(dx**2 + dy**2)
        angle_to_goal = math.atan2(dy, dx)
        angle_error = angle_to_goal - self.current_yaw

        # Normalize angle to [-pi, pi]
        angle_error = math.atan2(math.sin(angle_error), math.cos(angle_error))

        # Create velocity command
        cmd = Twist()

        # Check if goal reached
        if distance_to_goal < self.goal_tolerance:
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0
            self.get_logger().info('Goal reached!')
        # Check for obstacles
        elif self.min_obstacle_distance < self.safe_distance:
            # Obstacle detected - rotate to find clear path
            cmd.linear.x = 0.0
            cmd.angular.z = self.max_angular_vel * (1.0 if angle_error > 0 else -1.0)
            self.get_logger().warn(f'Obstacle at {self.min_obstacle_distance:.2f}m - rotating')
        else:
            # Clear path - navigate toward goal
            # Linear velocity proportional to distance
            cmd.linear.x = min(self.max_linear_vel, 0.5 * distance_to_goal)

            # Angular velocity proportional to angle error
            cmd.angular.z = max(-self.max_angular_vel,
                               min(self.max_angular_vel, 2.0 * angle_error))

            self.get_logger().info(
                f'Moving to goal: dist={distance_to_goal:.2f}m, '
                f'angle_err={math.degrees(angle_error):.1f}°'
            )

        # Publish command
        self.cmd_pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = ObstacleAvoidanceController()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Controller Features

- **Reactive behavior**: Responds to immediate sensor input
- **Goal-directed**: Navigates toward target position
- **Safety**: Stops and rotates when obstacles detected
- **Proportional control**: Speed varies with distance/angle error

## Control Loop Timing Best Practices

```python
class TimingExample(Node):
    def __init__(self):
        super().__init__('timing_example')

        # Use parameters for configurable timing
        self.declare_parameter('control_frequency', 50.0)
        frequency = self.get_parameter('control_frequency').value

        # Calculate timer period
        self.dt = 1.0 / frequency

        # Create timer
        self.timer = self.create_timer(self.dt, self.control_loop)

        # Performance monitoring
        self.last_time = self.get_clock().now()
        self.max_loop_time = 0.0

    def control_loop(self):
        # Measure actual loop time
        current_time = self.get_clock().now()
        actual_dt = (current_time - self.last_time).nanoseconds / 1e9
        self.last_time = current_time

        # Warn if timing is off
        if actual_dt > self.dt * 1.5:
            self.get_logger().warn(
                f'Control loop slow: {actual_dt*1000:.1f}ms '
                f'(expected {self.dt*1000:.1f}ms)'
            )

        # Your control computation here
        # ...

        # Track maximum loop time
        self.max_loop_time = max(self.max_loop_time, actual_dt)
```

## Summary

In this chapter, you learned:

- The role of controllers in robot systems (sense-think-act cycle)
- How to use ROS 2 Timer API for periodic control loops
- How to implement velocity controllers for differential drive robots
- How to create PID controllers for position control
- How to build feedback controllers using sensor data (LIDAR)
- Best practices for control timing and synchronization

## Congratulations!

You've completed Module 1: ROS 2 Fundamentals! You now have the foundation to:

- Install and configure ROS 2 systems
- Create nodes that communicate via topics, services, and actions
- Organize code into packages and build with colcon
- Configure systems using launch files and parameters
- Model robots with URDF
- Implement controllers for autonomous behavior

## Next Steps

Continue to Module 2 to learn about Digital Twins, where you'll simulate robots in Gazebo and Unity before deploying to real hardware.

---

[← Chapter 5: URDF](./chapter-5.md) | [Module 1 Overview](./index.md)
