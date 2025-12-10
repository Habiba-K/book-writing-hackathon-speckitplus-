---
id: packages
title: "Packages"
sidebar_label: "Packages"
sidebar_position: 3
---

# Chapter 3: ROS 2 Packages and Build System

## Learning Objectives

By the end of this chapter, you will be able to:

- Understand the structure of ROS 2 packages
- Create a Python package from scratch
- Configure package.xml and setup.py files
- Use colcon to build and install packages
- Organize multiple nodes in a single package

## Prerequisites

- Chapters 1-2 completion
- ROS 2 Humble installed
- Basic understanding of Python modules

## What is a ROS 2 Package?

A **package** is the fundamental unit of ROS 2 software organization. It contains:

- Nodes (executable programs)
- Libraries
- Configuration files
- Message/service/action definitions
- Launch files
- Documentation

Packages allow you to:
- Organize code logically
- Share and reuse software
- Manage dependencies
- Build and install software consistently

## ROS 2 Package Structure

A typical Python ROS 2 package has this structure:

```text
my_robot_package/
├── my_robot_package/          # Python module directory
│   ├── __init__.py           # Makes it a Python package
│   ├── node1.py              # First node
│   ├── node2.py              # Second node
│   └── utils.py              # Shared utilities
├── resource/                  # Package marker for install
│   └── my_robot_package      # Empty marker file
├── test/                      # Test files
│   ├── test_copyright.py
│   ├── test_flake8.py
│   └── test_pep257.py
├── package.xml               # Package metadata and dependencies
├── setup.py                  # Python package installation configuration
├── setup.cfg                 # Install configuration
└── README.md                 # Package documentation
```

## Creating Your First Package

### Step 1: Create Workspace

ROS 2 packages are organized in workspaces. Create one:

```bash
# Create workspace directory structure
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
```

### Step 2: Create Package

Use the ROS 2 package creation tool:

```bash
ros2 pkg create --build-type ament_python my_robot_package
```

This creates a package with the correct structure and boilerplate files.

### Step 3: Navigate to Package

```bash
cd my_robot_package
```

## Understanding package.xml

The `package.xml` file contains metadata and dependencies:

```xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <!-- Package name (must match directory name) -->
  <name>my_robot_package</name>
  <version>0.0.1</version>
  <description>My first ROS 2 package for robot control</description>

  <!-- Maintainer contact information -->
  <maintainer email="you@example.com">Your Name</maintainer>
  <license>Apache-2.0</license>

  <!-- Build tool dependency -->
  <buildtool_depend>ament_python</buildtool_depend>

  <!-- Runtime dependencies (packages needed to run) -->
  <exec_depend>rclpy</exec_depend>
  <exec_depend>std_msgs</exec_depend>
  <exec_depend>geometry_msgs</exec_depend>
  <exec_depend>sensor_msgs</exec_depend>

  <!-- Test dependencies -->
  <test_depend>ament_copyright</test_depend>
  <test_depend>ament_flake8</test_depend>
  <test_depend>ament_pep257</test_depend>
  <test_depend>python3-pytest</test_depend>

  <!-- Specifies build system -->
  <export>
    <build_type>ament_python</build_type>
  </export>
</package>
```

### Key Elements

- **`<name>`**: Package identifier (must be unique)
- **`<version>`**: Semantic versioning (MAJOR.MINOR.PATCH)
- **`<description>`**: Brief explanation of package purpose
- **`<buildtool_depend>`**: Build system required (ament_python or ament_cmake)
- **`<exec_depend>`**: Runtime dependencies (other packages needed)
- **`<test_depend>`**: Testing framework dependencies

## Understanding setup.py

The `setup.py` file configures how Python code is installed:

```python
from setuptools import setup

package_name = 'my_robot_package'

setup(
    # Package name (must match package.xml)
    name=package_name,
    version='0.0.1',

    # Include all Python packages found
    packages=[package_name],

    # Data files to install
    data_files=[
        # Install package marker file
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        # Install package.xml
        ('share/' + package_name, ['package.xml']),
    ],

    # Install dependencies from package.xml
    install_requires=['setuptools'],

    # ZIP installation is not safe for ROS 2
    zip_safe=True,

    # Package metadata
    maintainer='Your Name',
    maintainer_email='you@example.com',
    description='My first ROS 2 package for robot control',
    license='Apache-2.0',

    # Testing framework
    tests_require=['pytest'],

    # Entry points define executable scripts
    # Format: 'executable_name = package.module:function'
    entry_points={
        'console_scripts': [
            'velocity_publisher = my_robot_package.velocity_publisher:main',
            'laser_subscriber = my_robot_package.laser_subscriber:main',
            'controller_node = my_robot_package.controller:main',
        ],
    },
)
```

### Entry Points Explanation

Entry points create executable commands that can be run with `ros2 run`:

```python
'velocity_publisher = my_robot_package.velocity_publisher:main'
#        ↑                    ↑                ↑           ↑
#   command name      package name      file name    function to call
```

After installation, you can run:
```bash
ros2 run my_robot_package velocity_publisher
```

## Understanding setup.cfg

The `setup.cfg` file specifies install directories:

```ini
[develop]
script_dir=$base/lib/my_robot_package

[install]
install_scripts=$base/lib/my_robot_package
```

This ensures executables are installed to the correct location for ROS 2 to find them.

## Adding Nodes to Your Package

### Create a Node File

Create `my_robot_package/controller.py`:

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


class ObstacleAvoidanceController(Node):
    """
    Simple obstacle avoidance controller.
    Slows down when obstacles are detected in front.
    """

    def __init__(self):
        super().__init__('obstacle_avoidance_controller')

        # Publisher for velocity commands
        self.cmd_pub = self.create_publisher(Twist, 'cmd_vel', 10)

        # Subscriber for laser scan data
        self.scan_sub = self.create_subscription(
            LaserScan,
            'scan',
            self.scan_callback,
            10
        )

        self.min_safe_distance = 0.5  # meters
        self.get_logger().info('Obstacle avoidance controller started')

    def scan_callback(self, msg):
        """
        Process laser scan and publish velocity commands.
        """
        # Get minimum distance from front sensors
        # Assuming front is center of scan
        front_ranges = msg.ranges[len(msg.ranges)//3:2*len(msg.ranges)//3]
        min_distance = min(front_ranges) if front_ranges else float('inf')

        # Create velocity command
        cmd = Twist()

        if min_distance < self.min_safe_distance:
            # Obstacle detected - stop
            cmd.linear.x = 0.0
            cmd.angular.z = 0.5  # Rotate to find clear path
            self.get_logger().warn(f'Obstacle at {min_distance:.2f}m - stopping!')
        else:
            # Clear path - move forward
            cmd.linear.x = 0.3
            cmd.angular.z = 0.0
            self.get_logger().info(f'Clear path - moving forward')

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

### Register the Node

Add to `setup.py` entry_points:

```python
entry_points={
    'console_scripts': [
        'controller_node = my_robot_package.controller:main',
    ],
},
```

## Building with Colcon

Colcon is the ROS 2 build tool that compiles and installs packages.

### Build Commands

```bash
# Navigate to workspace root
cd ~/ros2_ws

# Build all packages
colcon build

# Build specific package
colcon build --packages-select my_robot_package

# Build with Python debug symbols
colcon build --symlink-install

# Clean build
rm -rf build/ install/ log/
colcon build
```

### Symlink Install (Recommended for Development)

The `--symlink-install` flag creates symbolic links instead of copying files. This means you can edit Python code and run it immediately without rebuilding:

```bash
colcon build --symlink-install
```

### Source the Workspace

After building, source the setup script to use your package:

```bash
# Source the install script
source ~/ros2_ws/install/setup.bash

# Add to ~/.bashrc for automatic sourcing
echo "source ~/ros2_ws/install/setup.bash" >> ~/.bashrc
```

### Verify Installation

```bash
# List packages in workspace
ros2 pkg list | grep my_robot

# Check if executable is found
ros2 pkg executables my_robot_package

# Run the node
ros2 run my_robot_package controller_node
```

## Workspace Overlay

ROS 2 supports workspace overlays - stacking multiple workspaces:

```bash
# Base layer: ROS 2 installation
source /opt/ros/humble/setup.bash

# Overlay: Your workspace
source ~/ros2_ws/install/setup.bash
```

Packages in the overlay take precedence over the base layer.

## Dependency Management

### Adding Dependencies

1. Add to `package.xml`:
```xml
<exec_depend>nav2_msgs</exec_depend>
```

2. Install the dependency:
```bash
sudo apt install ros-humble-nav2-msgs
```

3. Use in your code:
```python
from nav2_msgs.action import NavigateToPose
```

4. Rebuild:
```bash
colcon build --packages-select my_robot_package
```

## Common Colcon Commands

```bash
# Build all packages
colcon build

# Build with verbose output
colcon build --event-handlers console_direct+

# Build and run tests
colcon build && colcon test

# Show test results
colcon test-result --all

# List packages in workspace
colcon list

# Build packages up to a specific package
colcon build --packages-up-to my_robot_package
```

## Best Practices

1. **One package per robot/functionality**: Don't put everything in one package
2. **Use symlink install during development**: Faster iteration
3. **Keep package names lowercase**: Follow ROS 2 conventions
4. **Document your packages**: Maintain good README.md files
5. **Version your packages**: Use semantic versioning
6. **Declare all dependencies**: Explicit is better than implicit

## Summary

In this chapter, you learned:

- The structure and purpose of ROS 2 packages
- How to create packages with `ros2 pkg create`
- The role of `package.xml`, `setup.py`, and `setup.cfg`
- How to build packages using colcon
- How to organize nodes within packages
- Dependency management in ROS 2

## Next Steps

In the next chapter, we'll learn about launch files - a powerful way to start multiple nodes simultaneously with parameter configuration.

---

[← Chapter 2: Communication](./chapter-2.md) | [Chapter 4: Launch Files →](./chapter-4.md)
