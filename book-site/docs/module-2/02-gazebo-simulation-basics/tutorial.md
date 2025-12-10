# Gazebo Simulation Setup Tutorial

This tutorial will guide you through setting up your first digital twin simulation using Gazebo.

## Prerequisites

Before starting this tutorial, ensure you have:
- Completed the installation guide
- ROS 2 Humble sourced in your terminal
- Gazebo properly installed and tested

## Creating Your First Digital Twin Simulation

### Step 1: Launch the Empty World

First, let's launch Gazebo with an empty world to verify everything is working:

```bash
# Source ROS 2
source /opt/ros/humble/setup.bash

# Launch the empty world
ros2 launch digital_twin_gazebo empty_world.launch.py
```

You should see the Gazebo interface with a ground plane and a sky environment.

### Step 2: Spawn Your Robot

In a new terminal, source ROS 2 and launch the robot spawn file:

```bash
# Source ROS 2
source /opt/ros/humble/setup.bash

# Spawn the robot
ros2 launch digital_twin_gazebo spawn_robot.launch.py
```

You should see your humanoid robot appear in the Gazebo world.

### Step 3: Verify Robot State

Check that the robot's joint states are being published:

```bash
# List available topics
ros2 topic list | grep joint

# View joint states
ros2 topic echo /joint_states
```

You should see messages containing the positions, velocities, and efforts for all robot joints.

## Understanding the Simulation Components

### URDF Model
The Unified Robot Description Format (URDF) file contains the robot's physical properties including:
- Links (rigid bodies)
- Joints (connections between links)
- Visual and collision properties
- Inertial properties

### Gazebo Plugins
The `.gazebo` file contains plugin configurations that connect your URDF model to Gazebo's physics engine and ROS 2 control systems.

### Launch Files
Launch files coordinate the startup of multiple nodes and processes needed for the simulation:
- Gazebo server and client
- Robot state publisher
- Joint state publisher
- Controller manager

## Troubleshooting Common Issues

### Robot Not Appearing
- Check that the URDF file path is correct
- Verify that the robot model is valid
- Ensure Gazebo is running before spawning the robot

### Joint States Not Publishing
- Confirm the robot state publisher is running
- Check that the controller manager is active
- Verify ROS 2 network connectivity between nodes

## Next Steps

Now that you have successfully set up your basic simulation, you can:
- Configure physics properties for more realistic behavior
- Add sensors to your robot model
- Implement control algorithms to move the robot
- Integrate with Unity for enhanced visualization

Continue to the next section to learn about configuring physics simulation properties.