---
id: launch
title: "Launch"
sidebar_label: "Launch"
sidebar_position: 4
---

# Chapter 4: Launch Files and Parameters

## Learning Objectives

By the end of this chapter, you will be able to:

- Understand the purpose of launch files in ROS 2
- Create Python launch files to start multiple nodes
- Configure nodes using parameters
- Load parameters from YAML files
- Use launch file arguments and substitutions

## Prerequisites

- Chapters 1-3 completion
- Understanding of ROS 2 packages and colcon build system
- Python programming knowledge

## Why Launch Files?

Imagine starting a complex robot system that requires:
- 5 sensor nodes (cameras, LIDAR, IMU)
- 3 control nodes (navigation, arm controller, gripper)
- 2 processing nodes (perception, planning)
- Various visualization and logging tools

Starting each node manually would be tedious and error-prone. **Launch files** solve this by:

- Starting multiple nodes with a single command
- Configuring node parameters
- Setting up node remappings and namespaces
- Defining node dependencies and startup order
- Making systems reproducible and shareable

## Python Launch File Basics

ROS 2 supports Python launch files, which offer programmatic flexibility.

### Simple Launch File Example

Create `launch/simple_launch.py` in your package:

```python
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    """
    Launch a publisher and subscriber node.
    """
    return LaunchDescription([
        Node(
            package='my_robot_package',
            executable='velocity_publisher',
            name='velocity_pub',
            output='screen'
        ),
        Node(
            package='my_robot_package',
            executable='laser_subscriber',
            name='laser_sub',
            output='screen'
        ),
    ])
```

### Launch File Structure

Every launch file must:
1. Import `LaunchDescription` and `Node`
2. Define a `generate_launch_description()` function
3. Return a `LaunchDescription` containing a list of actions

### Running Launch Files

```bash
# From workspace root
ros2 launch my_robot_package simple_launch.py
```

## Complete Multi-Node Launch Example

This example launches a robot control system with multiple nodes:

```python
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    """
    Launch a complete robot control system with:
    - Velocity controller
    - Laser scanner processor
    - Obstacle avoidance node
    - State publisher
    """

    # Declare launch arguments
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation clock if true'
    )

    robot_name_arg = DeclareLaunchArgument(
        'robot_name',
        default_value='my_robot',
        description='Name of the robot'
    )

    # Get launch arguments
    use_sim_time = LaunchConfiguration('use_sim_time')
    robot_name = LaunchConfiguration('robot_name')

    # Define nodes
    velocity_controller = Node(
        package='my_robot_package',
        executable='velocity_publisher',
        name='velocity_controller',
        namespace=robot_name,
        parameters=[{
            'use_sim_time': use_sim_time,
            'publish_frequency': 10.0,
            'max_linear_velocity': 0.5,
            'max_angular_velocity': 1.0
        }],
        output='screen',
        emulate_tty=True
    )

    laser_processor = Node(
        package='my_robot_package',
        executable='laser_subscriber',
        name='laser_processor',
        namespace=robot_name,
        parameters=[{
            'use_sim_time': use_sim_time,
            'min_range': 0.1,
            'max_range': 10.0
        }],
        output='screen',
        emulate_tty=True
    )

    obstacle_avoider = Node(
        package='my_robot_package',
        executable='controller_node',
        name='obstacle_avoider',
        namespace=robot_name,
        parameters=[{
            'use_sim_time': use_sim_time,
            'safe_distance': 0.5,
            'rotation_speed': 0.3
        }],
        remappings=[
            ('/cmd_vel', '/cmd_vel_nav'),
            ('/scan', '/laser/scan')
        ],
        output='screen',
        emulate_tty=True
    )

    # Log info
    startup_msg = LogInfo(
        msg=['Launching robot control system for: ', robot_name]
    )

    return LaunchDescription([
        use_sim_time_arg,
        robot_name_arg,
        startup_msg,
        velocity_controller,
        laser_processor,
        obstacle_avoider,
    ])
```

### Key Features

- **Launch Arguments**: `use_sim_time`, `robot_name` can be set at runtime
- **Namespaces**: All nodes under `robot_name` namespace
- **Parameters**: Configured inline for each node
- **Remappings**: Topic names can be changed
- **Output**: `screen` shows node output in terminal

### Running with Arguments

```bash
# Use default arguments
ros2 launch my_robot_package robot_control.launch.py

# Override arguments
ros2 launch my_robot_package robot_control.launch.py robot_name:=robot1 use_sim_time:=true
```

## Parameters in Detail

Parameters allow runtime configuration of nodes without code changes.

### Declaring Parameters in Nodes

```python
import rclpy
from rclpy.node import Node


class ConfigurableNode(Node):
    """
    Node that demonstrates parameter declaration and usage.
    """

    def __init__(self):
        super().__init__('configurable_node')

        # Declare parameters with default values
        self.declare_parameter('max_speed', 1.0)
        self.declare_parameter('min_distance', 0.5)
        self.declare_parameter('robot_name', 'default_robot')
        self.declare_parameter('enable_safety', True)

        # Get parameter values
        self.max_speed = self.get_parameter('max_speed').value
        self.min_distance = self.get_parameter('min_distance').value
        self.robot_name = self.get_parameter('robot_name').value
        self.enable_safety = self.get_parameter('enable_safety').value

        # Log parameter values
        self.get_logger().info(f'Max speed: {self.max_speed}')
        self.get_logger().info(f'Min distance: {self.min_distance}')
        self.get_logger().info(f'Robot name: {self.robot_name}')
        self.get_logger().info(f'Safety enabled: {self.enable_safety}')

        # Set up parameter callback for runtime changes
        self.add_on_set_parameters_callback(self.parameter_callback)

    def parameter_callback(self, params):
        """
        Called when parameters are changed at runtime.
        """
        for param in params:
            if param.name == 'max_speed':
                self.max_speed = param.value
                self.get_logger().info(f'Updated max_speed to {self.max_speed}')
            elif param.name == 'min_distance':
                self.min_distance = param.value
                self.get_logger().info(f'Updated min_distance to {self.min_distance}')

        return rclpy.parameter.SetParametersResult(successful=True)


def main(args=None):
    rclpy.init(args=args)
    node = ConfigurableNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Setting Parameters from Command Line

```bash
# Set parameters when starting node
ros2 run my_robot_package configurable_node --ros-args -p max_speed:=2.0 -p robot_name:=robot1

# Change parameters at runtime
ros2 param set /configurable_node max_speed 1.5

# Get current parameter value
ros2 param get /configurable_node max_speed

# List all parameters
ros2 param list /configurable_node
```

## YAML Parameter Files

For complex configurations, use YAML files to organize parameters.

### Create Parameter File

Create `config/robot_params.yaml`:

```yaml
# Robot control parameters
/robot_controller:
  ros__parameters:
    max_linear_velocity: 0.5
    max_angular_velocity: 1.0
    publish_frequency: 10.0
    enable_safety: true
    safe_distance: 0.5

    # PID controller gains
    pid:
      kp: 1.0
      ki: 0.1
      kd: 0.05

/laser_processor:
  ros__parameters:
    min_range: 0.1
    max_range: 10.0
    angle_min: -3.14159
    angle_max: 3.14159
    filter_window_size: 5

/obstacle_avoider:
  ros__parameters:
    safe_distance: 0.5
    rotation_speed: 0.3
    max_retries: 3
```

### Load Parameters in Launch File

```python
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    """
    Launch nodes with parameters loaded from YAML file.
    """

    # Get package directory
    pkg_dir = get_package_share_directory('my_robot_package')

    # Path to parameter file
    params_file = os.path.join(pkg_dir, 'config', 'robot_params.yaml')

    # Launch nodes with parameter file
    robot_controller = Node(
        package='my_robot_package',
        executable='velocity_publisher',
        name='robot_controller',
        parameters=[params_file],
        output='screen'
    )

    laser_processor = Node(
        package='my_robot_package',
        executable='laser_subscriber',
        name='laser_processor',
        parameters=[params_file],
        output='screen'
    )

    obstacle_avoider = Node(
        package='my_robot_package',
        executable='controller_node',
        name='obstacle_avoider',
        parameters=[params_file],
        output='screen'
    )

    return LaunchDescription([
        robot_controller,
        laser_processor,
        obstacle_avoider,
    ])
```

### Install Parameter Files

Add to `setup.py`:

```python
import os
from glob import glob

setup(
    # ... other setup parameters ...

    data_files=[
        # ... existing data files ...

        # Install launch files
        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.py')),

        # Install config files
        (os.path.join('share', package_name, 'config'),
            glob('config/*.yaml')),
    ],

    # ... rest of setup ...
)
```

Rebuild after adding:

```bash
colcon build --packages-select my_robot_package
source install/setup.bash
```

## Launch File Advanced Features

### Conditional Node Launch

```python
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration

# Only launch if use_rviz is true
rviz_node = Node(
    package='rviz2',
    executable='rviz2',
    name='rviz2',
    condition=IfCondition(LaunchConfiguration('use_rviz'))
)
```

### Include Other Launch Files

```python
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

# Include another launch file
gazebo_launch = IncludeLaunchDescription(
    PythonLaunchDescriptionSource([
        os.path.join(get_package_share_directory('gazebo_ros'), 'launch'),
        '/gazebo.launch.py'
    ]),
    launch_arguments={'world': 'my_world.world'}.items()
)
```

## Testing Launch Files

```bash
# List available launch files in package
ros2 launch my_robot_package --show-args robot_control.launch.py

# Test with verbose output
ros2 launch my_robot_package robot_control.launch.py --debug

# Monitor nodes after launch
ros2 node list
ros2 topic list
ros2 param list
```

## Best Practices

1. **Use parameters for configuration**: Never hardcode values that might change
2. **Group related parameters**: Use YAML files for complex configurations
3. **Document launch arguments**: Use clear descriptions
4. **Namespace your nodes**: Avoid topic name conflicts in multi-robot systems
5. **Use meaningful names**: Node names should describe their function
6. **Test launch files**: Verify all nodes start correctly

## Summary

In this chapter, you learned:

- The purpose and structure of ROS 2 launch files
- How to create Python launch files to start multiple nodes
- How to declare and use parameters in nodes
- How to load parameters from YAML configuration files
- Advanced launch file features like arguments, conditions, and includes

## Next Steps

In the next chapter, we'll dive into URDF (Unified Robot Description Format) to model robot kinematics and create robot descriptions.

---

[← Chapter 3: Packages](./chapter-3.md) | [Chapter 5: URDF →](./chapter-5.md)
