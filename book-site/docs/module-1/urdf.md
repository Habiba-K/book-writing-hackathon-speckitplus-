---
id: urdf
title: "URDF"
sidebar_label: "URDF"
sidebar_position: 5
---

# Chapter 5: URDF - Unified Robot Description Format

## Learning Objectives

By the end of this chapter, you will be able to:

- Understand the structure and syntax of URDF files
- Define robot links with visual, collision, and inertial properties
- Create kinematic chains using different joint types
- Model a humanoid robot arm with multiple degrees of freedom
- Visualize URDF models in RViz

## Prerequisites

- Chapters 1-4 completion
- Basic understanding of coordinate systems
- Familiarity with XML syntax

## What is URDF?

**URDF (Unified Robot Description Format)** is an XML-based format for describing robot kinematics, dynamics, and visual representation. It's the standard way to model robots in ROS 2.

A URDF model defines:
- **Links**: Rigid bodies (robot parts like arms, legs, chassis)
- **Joints**: Connections between links (how parts move relative to each other)
- **Sensors**: Cameras, LIDAR, IMU, etc.
- **Physical properties**: Mass, inertia, friction

## URDF Structure

A URDF file contains a tree structure of links connected by joints:

```text
Base Link (torso)
    ├── Joint 1 (shoulder)
    │   └── Link 1 (upper_arm)
    │       ├── Joint 2 (elbow)
    │       │   └── Link 2 (forearm)
    │       │       └── Joint 3 (wrist)
    │       │           └── Link 3 (hand)
```

## XML Syntax Basics

URDF uses XML tags with attributes:

```xml
<tag_name attribute1="value1" attribute2="value2">
    <child_tag>content</child_tag>
</tag_name>
```

## Link Elements

A link represents a rigid body with three key components:

### 1. Visual - How it looks

```xml
<visual>
    <origin xyz="0 0 0" rpy="0 0 0"/>
    <geometry>
        <box size="0.1 0.05 0.02"/>
    </geometry>
    <material name="blue">
        <color rgba="0 0 1 1"/>
    </material>
</visual>
```

### 2. Collision - For physics simulation

```xml
<collision>
    <origin xyz="0 0 0" rpy="0 0 0"/>
    <geometry>
        <box size="0.1 0.05 0.02"/>
    </geometry>
</collision>
```

### 3. Inertial - Mass and inertia properties

```xml
<inertial>
    <origin xyz="0 0 0" rpy="0 0 0"/>
    <mass value="0.5"/>
    <inertia ixx="0.01" ixy="0" ixz="0"
             iyy="0.01" iyz="0"
             izz="0.01"/>
</inertial>
```

### Complete Link Example

```xml
<link name="upper_arm">
    <!-- Visual representation -->
    <visual>
        <origin xyz="0 0 0.15" rpy="0 0 0"/>
        <geometry>
            <cylinder radius="0.04" length="0.3"/>
        </geometry>
        <material name="grey">
            <color rgba="0.5 0.5 0.5 1"/>
        </material>
    </visual>

    <!-- Collision model (can be simplified for performance) -->
    <collision>
        <origin xyz="0 0 0.15" rpy="0 0 0"/>
        <geometry>
            <cylinder radius="0.04" length="0.3"/>
        </geometry>
    </collision>

    <!-- Physical properties -->
    <inertial>
        <origin xyz="0 0 0.15" rpy="0 0 0"/>
        <mass value="1.5"/>
        <inertia ixx="0.0113" ixy="0" ixz="0"
                 iyy="0.0113" iyz="0"
                 izz="0.0024"/>
    </inertial>
</link>
```

## Joint Types

Joints connect links and define how they can move relative to each other.

### 1. Fixed Joint

No movement - rigidly attached:

```xml
<joint name="base_to_torso" type="fixed">
    <parent link="base_link"/>
    <child link="torso"/>
    <origin xyz="0 0 0.1" rpy="0 0 0"/>
</joint>
```

### 2. Revolute Joint

Rotation around an axis with limits:

```xml
<joint name="shoulder_joint" type="revolute">
    <parent link="torso"/>
    <child link="upper_arm"/>
    <origin xyz="0 0.2 0.5" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>  <!-- Rotate around Y-axis -->
    <limit lower="-1.57" upper="1.57" effort="100" velocity="1.0"/>
</joint>
```

### 3. Continuous Joint

Unlimited rotation (like a wheel):

```xml
<joint name="wheel_joint" type="continuous">
    <parent link="base_link"/>
    <child link="wheel"/>
    <origin xyz="0.2 0 0" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>  <!-- Rotate around Z-axis -->
</joint>
```

### 4. Prismatic Joint

Linear sliding motion:

```xml
<joint name="slider_joint" type="prismatic">
    <parent link="base"/>
    <child link="platform"/>
    <origin xyz="0 0 0" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>  <!-- Slide along Z-axis -->
    <limit lower="0" upper="0.5" effort="1000" velocity="0.5"/>
</joint>
```

## Complete Humanoid Arm URDF

Here's a complete URDF model for a humanoid robot arm with shoulder, elbow, and wrist joints:

```xml
<?xml version="1.0"?>
<robot name="humanoid_arm">

    <!-- Base Link (Torso) -->
    <link name="torso">
        <visual>
            <origin xyz="0 0 0.25" rpy="0 0 0"/>
            <geometry>
                <box size="0.3 0.4 0.5"/>
            </geometry>
            <material name="grey">
                <color rgba="0.5 0.5 0.5 1"/>
            </material>
        </visual>
        <collision>
            <origin xyz="0 0 0.25" rpy="0 0 0"/>
            <geometry>
                <box size="0.3 0.4 0.5"/>
            </geometry>
        </collision>
        <inertial>
            <origin xyz="0 0 0.25" rpy="0 0 0"/>
            <mass value="10.0"/>
            <inertia ixx="0.42" ixy="0" ixz="0"
                     iyy="0.33" iyz="0"
                     izz="0.25"/>
        </inertial>
    </link>

    <!-- Upper Arm Link -->
    <link name="upper_arm">
        <visual>
            <origin xyz="0 0 -0.15" rpy="0 0 0"/>
            <geometry>
                <cylinder radius="0.04" length="0.3"/>
            </geometry>
            <material name="blue">
                <color rgba="0 0 1 1"/>
            </material>
        </visual>
        <collision>
            <origin xyz="0 0 -0.15" rpy="0 0 0"/>
            <geometry>
                <cylinder radius="0.04" length="0.3"/>
            </geometry>
        </collision>
        <inertial>
            <origin xyz="0 0 -0.15" rpy="0 0 0"/>
            <mass value="1.5"/>
            <inertia ixx="0.0113" ixy="0" ixz="0"
                     iyy="0.0113" iyz="0"
                     izz="0.0024"/>
        </inertial>
    </link>

    <!-- Shoulder Joint (Revolute) -->
    <joint name="shoulder_joint" type="revolute">
        <parent link="torso"/>
        <child link="upper_arm"/>
        <origin xyz="0 0.2 0.5" rpy="0 0 0"/>
        <axis xyz="0 1 0"/>  <!-- Y-axis rotation (pitch) -->
        <limit lower="-1.57" upper="1.57" effort="100" velocity="2.0"/>
        <dynamics damping="0.7" friction="0.5"/>
    </joint>

    <!-- Forearm Link -->
    <link name="forearm">
        <visual>
            <origin xyz="0 0 -0.125" rpy="0 0 0"/>
            <geometry>
                <cylinder radius="0.035" length="0.25"/>
            </geometry>
            <material name="green">
                <color rgba="0 1 0 1"/>
            </material>
        </visual>
        <collision>
            <origin xyz="0 0 -0.125" rpy="0 0 0"/>
            <geometry>
                <cylinder radius="0.035" length="0.25"/>
            </geometry>
        </collision>
        <inertial>
            <origin xyz="0 0 -0.125" rpy="0 0 0"/>
            <mass value="1.0"/>
            <inertia ixx="0.0052" ixy="0" ixz="0"
                     iyy="0.0052" iyz="0"
                     izz="0.0012"/>
        </inertial>
    </link>

    <!-- Elbow Joint (Revolute) -->
    <joint name="elbow_joint" type="revolute">
        <parent link="upper_arm"/>
        <child link="forearm"/>
        <origin xyz="0 0 -0.3" rpy="0 0 0"/>
        <axis xyz="0 1 0"/>  <!-- Y-axis rotation (pitch) -->
        <limit lower="0" upper="2.35" effort="50" velocity="2.0"/>
        <dynamics damping="0.5" friction="0.3"/>
    </joint>

    <!-- Hand Link -->
    <link name="hand">
        <visual>
            <origin xyz="0 0 -0.05" rpy="0 0 0"/>
            <geometry>
                <box size="0.08 0.12 0.1"/>
            </geometry>
            <material name="red">
                <color rgba="1 0 0 1"/>
            </material>
        </visual>
        <collision>
            <origin xyz="0 0 -0.05" rpy="0 0 0"/>
            <geometry>
                <box size="0.08 0.12 0.1"/>
            </geometry>
        </collision>
        <inertial>
            <origin xyz="0 0 -0.05" rpy="0 0 0"/>
            <mass value="0.5"/>
            <inertia ixx="0.0008" ixy="0" ixz="0"
                     iyy="0.0005" iyz="0"
                     izz="0.0008"/>
        </inertial>
    </link>

    <!-- Wrist Joint (Revolute) -->
    <joint name="wrist_joint" type="revolute">
        <parent link="forearm"/>
        <child link="hand"/>
        <origin xyz="0 0 -0.25" rpy="0 0 0"/>
        <axis xyz="1 0 0"/>  <!-- X-axis rotation (roll) -->
        <limit lower="-1.57" upper="1.57" effort="20" velocity="2.0"/>
        <dynamics damping="0.3" friction="0.1"/>
    </joint>

</robot>
```

### URDF Explanation

**Links**:
- `torso`: Base of the arm (grey box)
- `upper_arm`: Shoulder to elbow (blue cylinder)
- `forearm`: Elbow to wrist (green cylinder)
- `hand`: End effector (red box)

**Joints**:
- `shoulder_joint`: Pitch rotation (-90° to +90°)
- `elbow_joint`: Pitch rotation (0° to 135°)
- `wrist_joint`: Roll rotation (-90° to +90°)

**Coordinate Frames**:
- `origin xyz="0 0.2 0.5"`: Position offset from parent
- `rpy="0 0 0"`: Roll-Pitch-Yaw orientation (in radians)

**Joint Limits**:
- `lower`/`upper`: Joint angle limits (radians)
- `effort`: Maximum torque (N⋅m)
- `velocity`: Maximum angular velocity (rad/s)

## Visualizing URDF in RViz

### Create Display Launch File

Save as `launch/view_arm.launch.py`:

```python
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    """
    Launch robot_state_publisher and RViz to view URDF model.
    """

    # Get URDF file path
    pkg_dir = get_package_share_directory('my_robot_package')
    urdf_file = os.path.join(pkg_dir, 'urdf', 'humanoid_arm.urdf')

    # Read URDF file
    with open(urdf_file, 'r') as f:
        robot_description = f.read()

    # Robot State Publisher - publishes TF tree
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[{
            'robot_description': robot_description
        }],
        output='screen'
    )

    # Joint State Publisher GUI - control joints interactively
    joint_state_publisher_gui = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        output='screen'
    )

    # RViz - visualization tool
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen'
    )

    return LaunchDescription([
        robot_state_publisher,
        joint_state_publisher_gui,
        rviz,
    ])
```

### Install URDF File

Add to `setup.py`:

```python
# Install URDF files
(os.path.join('share', package_name, 'urdf'),
    glob('urdf/*.urdf')),
```

### Launch and Visualize

```bash
# Install joint state publisher GUI
sudo apt install ros-humble-joint-state-publisher-gui

# Build and source
colcon build --packages-select my_robot_package
source install/setup.bash

# Launch visualization
ros2 launch my_robot_package view_arm.launch.py
```

In RViz:
1. Click "Add" → "RobotModel"
2. Set "Fixed Frame" to "torso"
3. Use the GUI sliders to move joints

## Checking URDF Validity

```bash
# Install URDF tools
sudo apt install ros-humble-urdf-tutorial

# Check URDF syntax
check_urdf humanoid_arm.urdf

# View URDF tree structure
urdf_to_graphiz humanoid_arm.urdf
```

## Best Practices

1. **Use consistent units**: Meters for length, kilograms for mass, radians for angles
2. **Define realistic inertias**: Use physics calculators or CAD software
3. **Keep collision simple**: Use primitive shapes for performance
4. **Name links clearly**: Use descriptive names like `left_shoulder`, not `link1`
5. **Test in RViz**: Visualize before using in simulation
6. **Document joint limits**: Comment why limits are set to specific values

## Summary

In this chapter, you learned:

- The structure and syntax of URDF files
- How to define links with visual, collision, and inertial properties
- Different joint types: fixed, revolute, continuous, and prismatic
- How to create a complete humanoid arm model with multiple joints
- How to visualize and test URDF models using RViz

## Next Steps

In the next chapter, we'll learn about controllers - nodes that read sensor data and send commands to actuators to control robot behavior.

---

[← Chapter 4: Launch Files](./chapter-4.md) | [Chapter 6: Controllers →](./chapter-6.md)
