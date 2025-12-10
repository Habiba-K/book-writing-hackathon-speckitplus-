# ROS 2 Control Integration

## Overview of ROS 2 Control for Digital Twins

ROS 2 Control provides a standardized framework for controlling robotic systems, enabling real-time control of simulated and physical robots. In this module, you'll learn how to configure and use ROS 2 controllers for your humanoid robot in the digital twin simulation.

## Controller Architecture

### Joint State Broadcaster
- **Purpose**: Publishes current joint positions, velocities, and efforts
- **Topic**: `/joint_states`
- **Rate**: 50Hz for real-time feedback
- **Interface**: Standard ROS 2 message types

### Joint Trajectory Controller
- **Purpose**: Executes smooth trajectories for coordinated multi-joint movements
- **Interface**: `JointTrajectoryController`
- **Joints**: All robot joints (arms, legs, head)
- **Commands**: Position, velocity, and effort control

### Position Controllers
- **Purpose**: Direct position control for individual joint groups
- **Types**: Left arm, right arm controllers
- **Interface**: Position command interface
- **Use case**: Simple joint positioning tasks

## Configuration

### Controller Manager Setup
The controller manager orchestrates all controllers with a 100Hz update rate:

```yaml
controller_manager:
  ros__parameters:
    update_rate: 100  # Hz
    joint_state_broadcaster:
      type: joint_state_broadcaster/JointStateBroadcaster
    joint_trajectory_controller:
      type: joint_trajectory_controller/JointTrajectoryController
```

### Joint Trajectory Controller
Configured for all robot joints with position interfaces:

```yaml
joint_trajectory_controller:
  ros__parameters:
    joints:
      - left_shoulder_joint
      - left_elbow_joint
      - right_shoulder_joint
      - right_elbow_joint
      - left_hip_joint
      - left_knee_joint
      - left_ankle_joint
      - right_hip_joint
      - right_knee_joint
      - right_ankle_joint

    command_interfaces:
      - position

    state_interfaces:
      - position
      - velocity
```

## Control Commands

### Sending Joint Trajectories
Use the standard ROS 2 action interface to send trajectories:

```bash
# Example command to send a trajectory goal
ros2 action send_goal /joint_trajectory_controller/follow_joint_trajectory \
  control_msgs/action/FollowJointTrajectory \
  '{trajectory: {joint_names: ["left_shoulder_joint"], points: [{positions: [0.5], time_from_start: {sec: 2, nanosec: 0}}]}}'
```

### Position Control
For simple position commands to joint groups:

```bash
# Command left arm to specific positions
ros2 topic pub /left_arm_controller/commands std_msgs/Float64MultiArray '{data: [0.5, -0.3]}'
```

## Integration with Simulation

### Gazebo ros2_control Plugin
The simulation uses the `libgazebo_ros2_control.so` plugin to interface with Gazebo physics:

```xml
<gazebo>
  <plugin filename="libgazebo_ros2_control.so" name="gazebo_ros2_control">
    <parameters>$(find digital_twin_control)/config/controllers.yaml</parameters>
  </plugin>
</gazebo>
```

This plugin ensures that control commands are properly translated to physics simulation forces and that sensor feedback is accurately reported.

## Launching Control Systems

### Complete Launch File
The integrated system launches all components together:

```bash
# Launch robot with controllers and simulation
ros2 launch digital_twin_gazebo digital_twin_complete.launch.py
```

This includes:
- Robot model loading
- Gazebo simulation
- Controller spawning
- RViz2 visualization (optional)

## Testing and Verification

### Controller Status
Check controller status using ROS 2 tools:

```bash
# List active controllers
ros2 control list_controllers

# Check specific controller state
ros2 control list_controller_types
```

### Control Performance
Monitor control performance and ensure real-time capabilities are maintained during simulation.

## Best Practices

- Use trajectory controllers for smooth, coordinated movements
- Implement proper joint limits and velocity constraints
- Monitor control loop timing for real-time performance
- Validate control commands before execution to prevent unsafe movements

## Next Steps

Continue to learn about Unity visualization for enhanced robot representation and human-robot interaction.