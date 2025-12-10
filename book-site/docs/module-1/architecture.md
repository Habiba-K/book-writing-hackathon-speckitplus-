---
id: architecture
title: "Architecture"
sidebar_label: "Architecture"
sidebar_position: 1
---

# Chapter 1: ROS 2 Architecture and Installation

## Learning Objectives

By the end of this chapter, you will be able to:

- Understand the core architecture of ROS 2
- Install ROS 2 Humble on Ubuntu 22.04 LTS
- Create your first ROS 2 publisher and subscriber nodes
- Run and test ROS 2 communication patterns

## Prerequisites

- Ubuntu 22.04 LTS installed (native or virtual machine)
- Basic Python programming knowledge
- Terminal/command line familiarity

## ROS 2 Architecture Overview

ROS 2 (Robot Operating System 2) is a flexible framework for writing robot software. It's a collection of tools, libraries, and conventions designed to simplify the task of creating complex and robust robot behavior across a wide variety of robotic platforms.

### Key Architectural Components

**Nodes**: Independent processes that perform computation. Each node typically handles a specific task (e.g., sensor reading, motor control, path planning).

**Topics**: Named buses over which nodes exchange messages. Topics implement a publish-subscribe pattern for one-to-many, many-to-many data distribution.

**Messages**: Data structures that define the type of information exchanged over topics.

**Services**: Synchronous request-reply communication pattern for client-server interactions.

**Actions**: Asynchronous goal-based communication with feedback during execution.

**Graph**: The network of all ROS 2 nodes and their connections through topics, services, and actions.

### ROS 2 vs ROS 1

ROS 2 introduces significant improvements over ROS 1:

- **Real-time capabilities**: Support for deterministic execution
- **Security**: Built-in security features (DDS-Security)
- **Multi-robot systems**: Better support for distributed systems
- **Quality of Service (QoS)**: Configurable reliability and durability settings
- **No ROS Master required**: Decentralized discovery using DDS

## Installing ROS 2 Humble on Ubuntu 22.04

### Set locale

Ensure you have a locale that supports UTF-8:

```bash
locale  # check for UTF-8

sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

locale  # verify settings
```

### Setup Sources

Add the ROS 2 apt repository:

```bash
# Ensure Ubuntu Universe repository is enabled
sudo apt install software-properties-common
sudo add-apt-repository universe

# Add ROS 2 GPG key
sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

# Add repository to sources list
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
```

### Install ROS 2 Packages

Update your apt repository and install ROS 2 Humble Desktop:

```bash
sudo apt update
sudo apt upgrade

# Install ROS 2 Humble Desktop (includes RViz, demos, tutorials)
sudo apt install ros-humble-desktop

# Install development tools and ROS tools
sudo apt install ros-dev-tools
```

### Environment Setup

Source the ROS 2 environment setup script:

```bash
# Add to your shell startup script (~/.bashrc for bash)
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc

# Source for current terminal session
source /opt/ros/humble/setup.bash
```

### Verify Installation

Test your installation:

```bash
# Check ROS 2 version
ros2 --version

# List available ROS 2 commands
ros2 --help

# Run a demo talker node (publisher)
ros2 run demo_nodes_cpp talker
```

Open a new terminal and run the listener:

```bash
source /opt/ros/humble/setup.bash
ros2 run demo_nodes_cpp listener
```

You should see messages being published and received. Press `Ctrl+C` to stop.

## Your First ROS 2 Publisher Node

Let's create a simple publisher node in Python that sends string messages.

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MinimalPublisher(Node):
    """
    A minimal publisher node that publishes string messages.
    """

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        """
        Callback function executed every timer period.
        Publishes a new message with an incrementing counter.
        """
        msg = String()
        msg.data = f'Hello World: {self.i}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.i += 1


def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()

    try:
        rclpy.spin(minimal_publisher)
    except KeyboardInterrupt:
        pass

    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Code Explanation

- **`rclpy.init()`**: Initializes the ROS 2 Python client library
- **`Node` class**: Base class for all ROS 2 nodes
- **`create_publisher()`**: Creates a publisher for the specified message type and topic
- **`create_timer()`**: Sets up a timer that calls a callback function at regular intervals
- **`publish()`**: Sends a message on the topic
- **`rclpy.spin()`**: Keeps the node alive and processes callbacks

## Your First ROS 2 Subscriber Node

Now let's create a subscriber node that receives the messages:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MinimalSubscriber(Node):
    """
    A minimal subscriber node that listens to string messages.
    """

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10
        )
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        """
        Callback function executed when a message is received.
        """
        self.get_logger().info(f'I heard: "{msg.data}"')


def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()

    try:
        rclpy.spin(minimal_subscriber)
    except KeyboardInterrupt:
        pass

    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Code Explanation

- **`create_subscription()`**: Creates a subscriber for the specified message type and topic
- **`listener_callback()`**: Function called whenever a message is received on the subscribed topic
- **QoS depth (10)**: Queue size for buffering incoming messages

## Testing Publisher and Subscriber

To test these nodes, save them as separate Python files (`publisher.py` and `subscriber.py`), make them executable, and run them in separate terminals:

**Terminal 1 - Publisher:**
```bash
python3 publisher.py
```

**Terminal 2 - Subscriber:**
```bash
python3 subscriber.py
```

You should see the publisher sending messages and the subscriber receiving them in real-time.

## ROS 2 Command Line Tools

Useful commands for inspecting the ROS 2 graph:

```bash
# List all active nodes
ros2 node list

# Get information about a specific node
ros2 node info /minimal_publisher

# List all active topics
ros2 topic list

# See messages being published on a topic
ros2 topic echo /topic

# Get information about a topic
ros2 topic info /topic

# Publish a message from command line
ros2 topic pub /topic std_msgs/msg/String "data: 'Hello from CLI'"
```

## Summary

In this chapter, you learned:

- The core architecture of ROS 2 and its key components
- How to install ROS 2 Humble on Ubuntu 22.04 LTS
- How to create simple publisher and subscriber nodes in Python
- How to use ROS 2 command line tools to inspect the system

## Next Steps

In the next chapter, we'll explore ROS 2 communication patterns in depth, including topics, services, and actions with complete runnable examples.

---

[← Module 1 Overview](./index.md) | [Chapter 2: Communication Patterns →](./chapter-2.md)
