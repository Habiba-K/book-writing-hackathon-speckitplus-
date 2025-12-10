# ROS 2 Interface Contracts: Digital Twin

## Overview

This document specifies the ROS 2 interfaces (topics, services, actions) for the Digital Twin simulation system. These interfaces enable communication between Gazebo simulation, ROS 2 control nodes, and Unity visualization components.

## Message Types

### Sensor Data Messages

#### LaserScan (sensor_msgs/msg/LaserScan)
**Purpose**: LiDAR sensor data from simulated robot
**Topic**: `/digital_twin/laser_scan`

**Fields**:
- header (std_msgs/Header): Timestamp and frame ID
- angle_min (float32): Minimum angle in radians
- angle_max (float32): Maximum angle in radians
- angle_increment (float32): Angle increment between measurements
- time_increment (float32): Time increment between measurements
- scan_time (float32): Time between scans
- range_min (float32): Minimum range value
- range_max (float32): Maximum range value
- ranges (float32[]): Distance measurements
- intensities (float32[]): Intensity measurements

#### Imu (sensor_msgs/msg/Imu)
**Purpose**: IMU sensor data from simulated robot
**Topic**: `/digital_twin/imu`

**Fields**:
- header (std_msgs/Header): Timestamp and frame ID
- orientation (geometry_msgs/Quaternion): Orientation estimate
- orientation_covariance (float64[9]): Covariance matrix for orientation
- angular_velocity (geometry_msgs/Vector3): Angular velocity
- angular_velocity_covariance (float64[9]): Covariance matrix for angular velocity
- linear_acceleration (geometry_msgs/Vector3): Linear acceleration
- linear_acceleration_covariance (float64[9]): Covariance matrix for linear acceleration

#### JointState (sensor_msgs/msg/JointState)
**Purpose**: Current state of all joints in the robot
**Topic**: `/digital_twin/joint_states`

**Fields**:
- header (std_msgs/Header): Timestamp and frame ID
- name (string[]): Joint names
- position (float64[]): Joint positions (radians for revolute, meters for prismatic)
- velocity (float64[]): Joint velocities
- effort (float64[]): Joint efforts (applied torques/forces)

## Publisher Topics

### Sensor Data Publishers

| Topic | Message Type | Description | Frequency |
|-------|--------------|-------------|-----------|
| `/digital_twin/laser_scan` | sensor_msgs/LaserScan | Simulated LiDAR data | 10-20 Hz |
| `/digital_twin/imu` | sensor_msgs/Imu | Simulated IMU data | 100-200 Hz |
| `/digital_twin/joint_states` | sensor_msgs/JointState | Current joint positions, velocities, efforts | 50 Hz |
| `/digital_twin/depth_camera/depth/image_raw` | sensor_msgs/Image | Depth camera data | 30 Hz |
| `/digital_twin/rgb_camera/image_raw` | sensor_msgs/Image | RGB camera data | 30 Hz |

### Visualization Publishers

| Topic | Message Type | Description | Frequency |
|-------|--------------|-------------|-----------|
| `/digital_twin/robot_description` | std_msgs/String | URDF robot model definition | Once at startup |
| `/digital_twin/tf` | tf2_msgs/TFMessage | Transform tree for visualization | 30 Hz |
| `/digital_twin/tf_static` | tf2_msgs/TFMessage | Static transforms | Once at startup |

## Subscriber Topics

### Control Command Subscribers

| Topic | Message Type | Description | Expected Frequency |
|-------|--------------|-------------|-------------------|
| `/digital_twin/joint_commands` | trajectory_msgs/JointTrajectory | Joint position/velocity/effort commands | As needed |
| `/digital_twin/cmd_vel` | geometry_msgs/Twist | Base velocity commands | 10-50 Hz |
| `/digital_twin/gripper_cmd` | control_msgs/GripperCommand | Gripper control commands | As needed |

## Services

### Simulation Control Services

| Service Name | Service Type | Description | Request | Response |
|--------------|--------------|-------------|---------|----------|
| `/digital_twin/reset_simulation` | std_srvs/Empty | Reset simulation to initial state | Empty | Empty |
| `/digital_twin/pause_simulation` | std_srvs/SetBool | Pause/resume simulation | data: true to pause, false to resume | success: bool, message: string |
| `/digital_twin/set_physics_properties` | gazebo_msgs/SetPhysicsProperties | Configure physics parameters | time_step, max_update_rate, gravity, ode_config | success: bool, message: string |

### Model Services

| Service Name | Service Type | Description | Request | Response |
|--------------|--------------|-------------|---------|----------|
| `/digital_twin/spawn_entity` | gazebo_msgs/SpawnEntity | Spawn a new entity in simulation | name, xml, initial_pose, reference_frame | status_message: string, success: bool |
| `/digital_twin/delete_entity` | gazebo_msgs/DeleteEntity | Remove an entity from simulation | name | success: bool, status_message: string |

## Actions

### Trajectory Execution Actions

| Action Name | Action Type | Description |
|-------------|-------------|-------------|
| `/digital_twin/follow_joint_trajectory` | control_msgs/FollowJointTrajectory | Execute joint trajectory with feedback |


## Action Definition: FollowJointTrajectory

**Goal**:
- trajectory (trajectory_msgs/JointTrajectory): The trajectory to follow
- path_tolerance (control_msgs/JointTolerance[]): Tolerances for path following
- goal_tolerance (control_msgs/JointTolerance[]): Tolerances for goal achievement
- goal_time_tolerance (builtin_interfaces/Duration): Allowed time after goal point

**Result**:
- error_code (int8): Error code if execution failed
- error_string (string): Error description if applicable

**Feedback**:
- joint_names (string[]): Joint names
- desired (trajectory_msgs/JointTrajectoryPoint): Desired trajectory point
- actual (trajectory_msgs/JointTrajectoryPoint): Actual trajectory point
- error (trajectory_msgs/JointTrajectoryPoint): Error trajectory point

## Frame Conventions

### Coordinate Frames

- `world`: Fixed world frame, origin of simulation
- `base_link`: Robot base frame, attached to main body
- `camera_link`, `lidar_link`, `imu_link`: Sensor frames
- `joint_frame_{n}`: Individual joint frames
- `end_effector`: Tool or end effector frame

### Transform Convention
- Right-handed coordinate system
- X forward, Y left, Z up (ROS standard)
- All transforms published to `/digital_twin/tf` topic

## Quality of Service Settings

### Sensor Topics (High Frequency)
- Reliability: Reliable
- Durability: Volatile
- History: Keep last 1
- Depth: 1

### Control Topics (Medium Frequency)
- Reliability: Reliable
- Durability: Volatile
- History: Keep last 10
- Depth: 10

### Configuration Services
- Reliability: Reliable
- Durability: Volatile
- History: Keep last 1
- Depth: 1