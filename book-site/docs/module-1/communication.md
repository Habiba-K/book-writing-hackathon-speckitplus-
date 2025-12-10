---
id: communication
title: "Communication"
sidebar_label: "Communication"
sidebar_position: 2
---

# Chapter 2: ROS 2 Communication Patterns

## Learning Objectives

By the end of this chapter, you will be able to:

- Understand the three main ROS 2 communication patterns: topics, services, and actions
- Implement publishers and subscribers for asynchronous data streams
- Create service servers and clients for request-reply interactions
- Work with actions for long-running tasks with feedback
- Choose the appropriate communication pattern for different robotic tasks

## Prerequisites

- Chapter 1 completion (ROS 2 installation and basic node concepts)
- Python 3.10+ installed
- ROS 2 Humble environment sourced

## Communication Pattern Overview

ROS 2 provides three primary communication patterns, each suited for different use cases:

| Pattern | Type | Use Case | Example |
|---------|------|----------|---------|
| **Topics** | Publish-Subscribe | Continuous data streams | Sensor data, robot state |
| **Services** | Request-Reply | Short computations | Calculate inverse kinematics |
| **Actions** | Goal-Feedback-Result | Long-running tasks | Navigate to waypoint |

## Example 1: Publisher Node

This example publishes robot velocity commands at a fixed rate.

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class VelocityPublisher(Node):
    """
    Publisher node that sends velocity commands to a robot.
    Publishes Twist messages (linear and angular velocity) at 10 Hz.
    """

    def __init__(self):
        super().__init__('velocity_publisher')
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.timer_callback)  # 10 Hz
        self.get_logger().info('Velocity Publisher has been started')

    def timer_callback(self):
        """
        Publishes velocity commands.
        Move forward at 0.5 m/s and rotate at 0.3 rad/s.
        """
        msg = Twist()
        msg.linear.x = 0.5   # Forward velocity (m/s)
        msg.linear.y = 0.0
        msg.linear.z = 0.0
        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = 0.3  # Rotation velocity (rad/s)

        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: linear.x={msg.linear.x}, angular.z={msg.angular.z}')


def main(args=None):
    rclpy.init(args=args)
    node = VelocityPublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Running the Publisher

Save the code as `velocity_publisher.py` and run:

```bash
python3 velocity_publisher.py
```

You should see velocity commands being published. To monitor the topic:

```bash
# In a new terminal
ros2 topic echo /cmd_vel
```

## Example 2: Subscriber Node

This example subscribes to laser scan data from a LIDAR sensor.

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan


class LaserSubscriber(Node):
    """
    Subscriber node that processes LIDAR sensor data.
    Detects obstacles by finding the minimum distance in the scan.
    """

    def __init__(self):
        super().__init__('laser_subscriber')
        self.subscription = self.create_subscription(
            LaserScan,
            'scan',
            self.listener_callback,
            10
        )
        self.get_logger().info('Laser Subscriber has been started')

    def listener_callback(self, msg):
        """
        Processes incoming laser scan data.
        Finds the minimum distance and logs a warning if obstacle is too close.
        """
        # Get minimum distance from all ranges
        min_distance = min(msg.ranges)

        if min_distance < 0.5:  # Obstacle within 50 cm
            self.get_logger().warn(f'Obstacle detected at {min_distance:.2f}m!')
        else:
            self.get_logger().info(f'Closest obstacle: {min_distance:.2f}m')


def main(args=None):
    rclpy.init(args=args)
    node = LaserSubscriber()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Running the Subscriber

Save as `laser_subscriber.py` and run:

```bash
python3 laser_subscriber.py
```

To test with simulated data, publish a fake scan:

```bash
ros2 topic pub /scan sensor_msgs/msg/LaserScan "{ranges: [0.3, 0.4, 0.5, 1.0, 2.0]}"
```

## Example 3: Service Server

This example creates a service that adds two integers.

```python
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts


class AddTwoIntsServer(Node):
    """
    Service server that adds two integers.
    Demonstrates synchronous request-reply communication.
    """

    def __init__(self):
        super().__init__('add_two_ints_server')
        self.srv = self.create_service(
            AddTwoInts,
            'add_two_ints',
            self.add_two_ints_callback
        )
        self.get_logger().info('Add Two Ints Server ready')

    def add_two_ints_callback(self, request, response):
        """
        Service callback that performs the addition.
        Args:
            request: Contains 'a' and 'b' integers
            response: Will contain 'sum' result
        """
        response.sum = request.a + request.b
        self.get_logger().info(f'Incoming request: {request.a} + {request.b} = {response.sum}')
        return response


def main(args=None):
    rclpy.init(args=args)
    node = AddTwoIntsServer()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Running the Service Server

Save as `add_server.py` and run:

```bash
python3 add_server.py
```

Test the service from command line:

```bash
# Call the service with arguments
ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 5, b: 3}"
```

## Example 4: Service Client

This example creates a client that calls the AddTwoInts service.

```python
import sys
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts


class AddTwoIntsClient(Node):
    """
    Service client that requests addition of two integers.
    Demonstrates how to make synchronous service calls.
    """

    def __init__(self):
        super().__init__('add_two_ints_client')
        self.client = self.create_client(AddTwoInts, 'add_two_ints')

        # Wait for service to become available
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting...')

    def send_request(self, a, b):
        """
        Sends a service request and waits for the response.
        Args:
            a: First integer
            b: Second integer
        Returns:
            The sum of a and b
        """
        request = AddTwoInts.Request()
        request.a = a
        request.b = b

        self.get_logger().info(f'Sending request: {a} + {b}')
        future = self.client.call_async(request)

        # Wait for response
        rclpy.spin_until_future_complete(self, future)

        if future.result() is not None:
            response = future.result()
            self.get_logger().info(f'Result: {response.sum}')
            return response.sum
        else:
            self.get_logger().error('Service call failed')
            return None


def main(args=None):
    rclpy.init(args=args)

    if len(sys.argv) != 3:
        print('Usage: python3 add_client.py <a> <b>')
        return

    a = int(sys.argv[1])
    b = int(sys.argv[2])

    node = AddTwoIntsClient()
    result = node.send_request(a, b)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Running the Service Client

First, make sure the service server is running, then:

```bash
python3 add_client.py 10 20
```

You should see the result: 30

## Quality of Service (QoS)

ROS 2 allows you to configure Quality of Service settings for reliable communication:

```python
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

# Create custom QoS profile
qos_profile = QoSProfile(
    reliability=ReliabilityPolicy.RELIABLE,  # or BEST_EFFORT
    history=HistoryPolicy.KEEP_LAST,
    depth=10
)

# Use with publisher
self.publisher_ = self.create_publisher(
    String,
    'topic',
    qos_profile
)
```

### QoS Policies

- **Reliability**:
  - `RELIABLE`: Guarantees message delivery (like TCP)
  - `BEST_EFFORT`: Fast but may drop messages (like UDP)

- **History**:
  - `KEEP_LAST`: Keep only N most recent messages
  - `KEEP_ALL`: Keep all messages (limited by resources)

- **Durability**:
  - `TRANSIENT_LOCAL`: Store messages for late-joining subscribers
  - `VOLATILE`: No historical messages

## Choosing Communication Patterns

| Use Case | Recommended Pattern | Reason |
|----------|-------------------|---------|
| Sensor data (camera, LIDAR) | Topic (Publisher/Subscriber) | Continuous stream, multiple consumers |
| Robot state (position, velocity) | Topic | Continuous updates, many listeners |
| Quick calculations (IK solver) | Service | Request-reply, short execution |
| Navigation to goal | Action | Long-running, needs feedback and cancel |
| Emergency stop | Topic with RELIABLE QoS | Fast broadcast to all nodes |

## Testing Communication

Useful commands for debugging:

```bash
# List all active topics
ros2 topic list

# Show message type of a topic
ros2 topic info /cmd_vel

# Monitor messages on a topic
ros2 topic echo /cmd_vel

# List all services
ros2 service list

# Show service type
ros2 service type /add_two_ints

# Call a service
ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 1, b: 2}"

# Monitor node graph
rqt_graph
```

## Summary

In this chapter, you learned:

- The three main ROS 2 communication patterns: topics, services, and actions
- How to implement publishers and subscribers for continuous data streams
- How to create service servers and clients for request-reply interactions
- Quality of Service (QoS) configuration for reliable communication
- How to choose the right communication pattern for different tasks

## Next Steps

In the next chapter, we'll learn how to organize ROS 2 code into packages, use colcon build system, and structure projects properly.

---

[← Chapter 1: Architecture](./chapter-1.md) | [Chapter 3: Packages →](./chapter-3.md)
