# Gazebo Installation Guide

This guide will help you set up the Gazebo simulation environment for digital twin development.

## Prerequisites

- Ubuntu 22.04 LTS
- At least 4GB RAM (8GB+ recommended)
- Compatible GPU (NVIDIA recommended for visualization)
- Internet connection for package downloads

## Installing ROS 2 Humble

First, set up your ROS 2 environment:

```bash
# Set locale
locale  # check for UTF-8
sudo apt update && sudo apt install locales
sudo locale-gen en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8

# Add ROS 2 apt repository
sudo apt install software-properties-common
sudo add-apt-repository universe

# Add the ROS 2 GPG key and repository
curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key | sudo gpg --dearmor -o /usr/share/keyrings/ros-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# Update and install ROS 2 Humble
sudo apt update
sudo apt install ros-humble-desktop
sudo apt install ros-humble-gazebo-ros-pkgs
sudo apt install ros-humble-ros-gz
```

## Environment Setup

Source the ROS 2 environment:

```bash
source /opt/ros/humble/setup.bash
```

For persistent setup, add this to your `.bashrc`:

```bash
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
```

## Install Additional Dependencies

```bash
sudo apt install python3-colcon-common-extensions
sudo apt install python3-rosdep
sudo apt install ros-humble-ros2-control
sudo apt install ros-humble-ros2-controllers
sudo apt install ros-humble-gazebo-dev
sudo apt install ros-humble-joint-state-publisher
sudo apt install ros-humble-robot-state-publisher
```

## Verify Installation

Test that Gazebo launches correctly:

```bash
gz sim
```

You should see the Gazebo interface with a default environment.

## Troubleshooting

### Common Issues

**Gazebo fails to start:**
- Check that your GPU drivers are properly installed
- Run `nvidia-smi` (for NVIDIA) to verify GPU detection
- Ensure you have sufficient RAM and disk space

**Missing packages:**
- Make sure your apt repositories are updated
- Check your Ubuntu version is 22.04 LTS
- Verify ROS 2 repository configuration

## Next Steps

Once your environment is set up, proceed to the Gazebo simulation basics tutorial to learn how to create your first digital twin simulation.