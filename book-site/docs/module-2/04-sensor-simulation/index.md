# Sensor Simulation

## Overview of Sensor Simulation in Digital Twins

Sensor simulation is a critical component of digital twin technology, enabling realistic sensor data generation for robotics algorithms. In this module, you'll learn how to configure and integrate various sensors (LiDAR, IMU, depth cameras) with ROS 2 for your humanoid robot.

## Types of Sensors

### LiDAR (Light Detection and Ranging)
- **Purpose**: Provides 2D/3D distance measurements for mapping and navigation
- **Configuration**: 360-degree horizontal scan with 10Hz update rate
- **Output**: `sensor_msgs/LaserScan` messages on `/scan` topic
- **Range**: 0.1m to 10.0m detection range

### IMU (Inertial Measurement Unit)
- **Purpose**: Measures orientation, angular velocity, and linear acceleration
- **Configuration**: 100Hz update rate with noise modeling
- **Output**: `sensor_msgs/Imu` messages on `/imu/data` topic
- **Frame**: Mounted on `base_link` for robot body measurements

### Depth Camera
- **Purpose**: Provides RGB and depth information for 3D perception
- **Configuration**: 640x480 resolution at 30Hz
- **Output**: Multiple topics for RGB image, depth image, and point cloud
- **Frame**: Mounted on robot head for forward-facing view

## Sensor Integration with ROS 2

### Topic Configuration
All sensors publish data to standardized ROS 2 topics following REP-103 conventions:

```yaml
sensors:
  lidar:
    topic: "/scan"
    frame_id: "head"
    update_rate: 10
    type: "laser_scan"

  imu:
    topic: "/imu/data"
    frame_id: "base_link"
    update_rate: 100
    type: "imu"

  depth_camera:
    rgb_topic: "/depth_cam/rgb/image_raw"
    depth_topic: "/depth_cam/depth/image_raw"
    points_topic: "/depth_cam/depth/points"
    camera_info_topic: "/depth_cam/rgb/camera_info"
    frame_id: "head_depth_frame"
    update_rate: 30
    type: "depth_camera"
```

### Quality of Service Settings
Sensors use appropriate QoS settings for real-time performance:

```yaml
qos:
  sensor_data:
    reliability: "best_effort"
    durability: "volatile"
    history: "keep_last"
    depth: 5
```

## Sensor Verification

### Testing Sensor Data
Use the sensor verification script to ensure all sensors are publishing correctly:

```bash
ros2 run digital_twin_examples sensor_verification.py
```

This script verifies:
- Data ranges match sensor specifications
- Update rates are within expected bounds
- Sensor values are physically reasonable

### Calibration and Validation
Sensor data is calibrated against theoretical physics calculations to ensure accuracy in the simulation environment.

## Performance Considerations

- LiDAR simulation: 10Hz provides adequate navigation data while maintaining performance
- IMU simulation: 100Hz captures fast dynamics while avoiding excessive data
- Depth camera: 30Hz matches visual perception requirements with computational limits

## Next Steps

Continue to learn about ROS 2 control integration for commanding your simulated robot.