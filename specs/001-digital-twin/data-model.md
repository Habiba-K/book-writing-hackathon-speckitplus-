# Data Model: Digital Twin (Gazebo & Unity)

## Core Entities

### Digital Twin
- **Attributes**:
  - id (string): Unique identifier for the digital twin instance
  - name (string): Human-readable name of the digital twin
  - robot_model (string): Reference to the URDF model used
  - simulation_state (object): Current state of the simulation (position, orientation, joint states)
  - sensors_config (array): List of sensor configurations attached to the twin
  - creation_date (datetime): When the digital twin was created
  - last_updated (datetime): Last modification timestamp

### Robot Model (URDF)
- **Attributes**:
  - model_id (string): Unique identifier for the robot model
  - name (string): Robot name (e.g., "humanoid_robot")
  - urdf_path (string): File path to the URDF definition
  - mesh_paths (array): Paths to 3D mesh files
  - joint_definitions (array): Joint properties (type, limits, dynamics)
  - link_definitions (array): Link properties (mass, inertia, visuals)
  - material_definitions (array): Visual material properties

### Sensor Configuration
- **Attributes**:
  - sensor_id (string): Unique identifier for the sensor
  - sensor_type (enum): Type of sensor (LIDAR, CAMERA, IMU, FORCE_TORQUE)
  - name (string): Sensor name for identification
  - parent_link (string): Link to which the sensor is attached
  - position (object): Position relative to parent link (x, y, z)
  - orientation (object): Orientation relative to parent link (roll, pitch, yaw)
  - parameters (object): Sensor-specific parameters (range, resolution, etc.)
  - ros_topic (string): ROS 2 topic name for sensor data output

### Simulation Environment
- **Attributes**:
  - env_id (string): Unique identifier for the environment
  - name (string): Environment name
  - world_file (string): Path to Gazebo world file
  - gravity (object): Gravity vector (x, y, z)
  - physics_engine (string): Physics engine configuration
  - lighting_config (object): Environment lighting settings
  - objects (array): Static objects in the environment

### Joint State
- **Attributes**:
  - joint_name (string): Name of the joint
  - position (float): Current joint position (radians for revolute, meters for prismatic)
  - velocity (float): Current joint velocity
  - effort (float): Current joint effort/torque
  - timestamp (datetime): When the state was recorded

### Control Command
- **Attributes**:
  - command_id (string): Unique identifier for the command
  - joint_names (array): Names of joints to control
  - positions (array): Target positions for position control
  - velocities (array): Target velocities for velocity control
  - efforts (array): Target efforts for effort control
  - duration (float): Time to reach target (for trajectory commands)

## Relationships

### Digital Twin → Robot Model
- One-to-One: Each digital twin uses exactly one robot model

### Digital Twin → Sensor Configuration
- One-to-Many: Each digital twin can have multiple sensor configurations

### Digital Twin → Simulation Environment
- One-to-One: Each digital twin exists in one simulation environment

### Simulation Environment → Objects
- One-to-Many: Each environment contains multiple static objects

### Digital Twin → Joint State
- One-to-Many: Each digital twin has multiple joint states over time

### Control Command → Digital Twin
- Many-to-One: Multiple control commands can target the same digital twin

## Validation Rules

1. **Digital Twin Validation**:
   - name must be 3-50 characters
   - robot_model must reference an existing Robot Model
   - sensors_config must be valid sensor configurations

2. **Robot Model Validation**:
   - urdf_path must exist and be a valid URDF file
   - joint_definitions must have valid types and limits
   - mesh_paths must reference existing files

3. **Sensor Configuration Validation**:
   - sensor_type must be one of the defined enum values
   - parent_link must reference a valid link in the robot model
   - ros_topic must follow ROS 2 naming conventions

4. **Joint State Validation**:
   - joint_name must exist in the robot model
   - position must be within joint limits
   - timestamp must be current or recent

## State Transitions

### Digital Twin States
- **CREATED**: Digital twin defined but not yet simulated
- **RUNNING**: Simulation is active and publishing data
- **PAUSED**: Simulation is paused but can be resumed
- **STOPPED**: Simulation has been stopped
- **ERROR**: Simulation encountered an error

### State Transition Rules
- CREATED → RUNNING: When simulation starts
- RUNNING → PAUSED: When user pauses simulation
- PAUSED → RUNNING: When user resumes simulation
- RUNNING → STOPPED: When user stops simulation
- PAUSED → STOPPED: When user stops simulation
- Any state → ERROR: When simulation encounters an unrecoverable error
- ERROR → CREATED: When error is resolved and simulation is reset