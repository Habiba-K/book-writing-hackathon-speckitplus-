#!/bin/bash

# Setup script for Digital Twin ROS 2 workspace
# This script creates the necessary directory structure and configuration files

echo "Setting up Digital Twin ROS 2 workspace..."

# Create the workspace structure
mkdir -p src/digital_twin_description/urdf
mkdir -p src/digital_twin_description/meshes
mkdir -p src/digital_twin_description/launch
mkdir -p src/digital_twin_description/rviz

mkdir -p src/digital_twin_gazebo/worlds
mkdir -p src/digital_twin_gazebo/launch
mkdir -p src/digital_twin_gazebo/config
mkdir -p src/digital_twin_gazebo/models

mkdir -p src/digital_twin_sensors/config
mkdir -p src/digital_twin_sensors/launch

mkdir -p src/digital_twin_control/config
mkdir -p src/digital_twin_control/launch

mkdir -p src/digital_twin_examples/launch
mkdir -p src/digital_twin_examples/config
mkdir -p src/digital_twin_examples/scripts

echo "Workspace structure created successfully!"

# Create colcon build configuration
cat > colcon.meta << EOF
{
    "names": {
        "digital_twin_description": {
            "install-base": "install"
        },
        "digital_twin_gazebo": {
            "install-base": "install"
        },
        "digital_twin_sensors": {
            "install-base": "install"
        },
        "digital_twin_control": {
            "install-base": "install"
        },
        "digital_twin_examples": {
            "install-base": "install"
        }
    }
}
EOF

echo "Colcon configuration created!"

# Create a basic .bashrc extension for the workspace
cat > setup.bash << EOF
#!/bin/bash
# Source ROS 2 environment
source /opt/ros/humble/setup.bash

# Source the local workspace if built
if [ -f install/setup.bash ]; then
    source install/setup.bash
fi

export GAZEBO_MODEL_PATH=\$GAZEBO_MODEL_PATH:~/digital_twin_ws/src/digital_twin_gazebo/models
export GAZEBO_RESOURCE_PATH=\$GAZEBO_RESOURCE_PATH:~/digital_twin_ws/src/digital_twin_gazebo/worlds
EOF

echo "Setup script created!"

# Make setup script executable
chmod +x setup.bash

echo "Digital Twin workspace setup complete!"
echo "To use the workspace:"
echo "1. Run: source setup.bash"
echo "2. Build with: colcon build"
echo "3. Source the install: source install/setup.bash"