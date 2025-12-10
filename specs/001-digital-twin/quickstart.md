# Quickstart: Digital Twin (Gazebo & Unity)

## Prerequisites

- Ubuntu 22.04 LTS (recommended) or Windows 10+
- ROS 2 Humble Hawksbill installed
- Gazebo (Garden or Classic) installed
- NVIDIA RTX 30+ series GPU (recommended for Unity visualization)
- 16GB+ RAM
- Git installed

## Installation Steps

### 1. Set up ROS 2 Environment

```bash
# Install ROS 2 Humble (if not already installed)
sudo apt update
sudo apt install ros-humble-desktop
sudo apt install ros-humble-gazebo-*
sudo apt install python3-rosdep2

# Source ROS 2 environment
source /opt/ros/humble/setup.bash

# Install ROS 2 dependencies
sudo apt install python3-colcon-common-extensions
sudo apt install python3-rosdep
sudo rosdep init
rosdep update
```

### 2. Create ROS 2 Workspace

```bash
# Create workspace directory
mkdir -p ~/digital_twin_ws/src
cd ~/digital_twin_ws

# Clone required packages
cd src
git clone https://github.com/ros-simulation/gazebo_ros_pkgs.git
git clone https://github.com/ros-controls/ros2_control.git
git clone https://github.com/ros-controls/ros2_controllers.git

# For humanoid robot simulation, you may need to create or obtain a robot model:
# Create a simple robot model package
cd ~/digital_twin_ws/src
ros2 pkg create --build-type ament_cmake digital_twin_description
```

### 3. Build the Workspace

```bash
cd ~/digital_twin_ws
source /opt/ros/humble/setup.bash
colcon build --packages-select gazebo_ros_pkgs ros2_control ros2_controllers
source install/setup.bash
```

### 4. Launch Basic Simulation

```bash
# Terminal 1: Launch Gazebo with a simple world
cd ~/digital_twin_ws
source install/setup.bash
ros2 launch gazebo_ros empty_world.launch.py

# Terminal 2: Spawn a simple robot (after Gazebo is running)
# This would typically involve spawning a URDF model
```

### 5. Verify ROS 2 Communication

```bash
# Check available topics
ros2 topic list

# Check available services
ros2 service list

# Verify that sensor data is being published (replace with actual topic names)
# ros2 topic echo /your_robot/laser_scan
# ros2 topic echo /your_robot/imu
```

## Running the Digital Twin Module

### Basic Robot Simulation

1. Launch Gazebo environment:
```bash
cd ~/digital_twin_ws
source install/setup.bash
ros2 launch digital_twin_gazebo digital_twin_world.launch.py
```

2. In another terminal, send control commands:
```bash
# Example: Publish joint states
ros2 topic pub /joint_states sensor_msgs/msg/JointState "name: ['joint1', 'joint2']
position: [1.0, -0.5]
velocity: [0.0, 0.0]
effort: [0.0, 0.0]"
```

### Sensor Data Verification

1. Check sensor topics:
```bash
# List all topics containing "sensor"
ros2 topic list | grep sensor

# Monitor LiDAR data
ros2 topic echo /digital_twin/laser_scan

# Monitor IMU data
ros2 topic echo /digital_twin/imu
```

### Unity Visualization (Optional)

1. Install Unity 2022.3 LTS
2. Import the Unity Robotics Simulation package
3. Configure ROS 2 connection settings to match your Gazebo instance
4. Run the Unity scene to visualize the simulation

## Troubleshooting

### Common Issues

**Gazebo fails to start:**
- Ensure NVIDIA drivers are properly installed
- Check that GPU is supported
- Try running `nvidia-smi` to verify GPU detection

**ROS 2 topics not appearing:**
- Verify ROS 2 environment is sourced: `source ~/digital_twin_ws/install/setup.bash`
- Check that ROS_DOMAIN_ID is consistent across terminals
- Confirm network configuration allows ROS 2 communication

**Performance issues:**
- Close unnecessary applications to free up RAM
- Reduce simulation complexity if needed
- Verify GPU drivers are up to date

## Next Steps

1. Follow the detailed chapters in the Digital Twin module to learn:
   - Chapter 6: Digital Twin Concepts
   - Chapter 7: Gazebo Fundamentals
   - Chapter 8: Physics Simulation
   - Chapter 9: Sensor Simulation
   - Chapter 10: ROS 2 Control Integration
   - Chapter 11: Unity Visualization (Optional)

2. Experiment with different robot models and environments

3. Develop custom control algorithms using the simulation environment