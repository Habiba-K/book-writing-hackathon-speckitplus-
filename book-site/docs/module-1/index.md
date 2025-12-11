---
id: index
title: "Module 1: Robotic Nervous System (ROS 2)"
sidebar_label: Overview
sidebar_position: 0
---

# Module 1: Robotic Nervous System (ROS 2)

**Timeframe:** Weeks 3-5

Master the middleware layer that enables robot communication and control through ROS 2, the industry-standard framework for robotics software development.

## Learning Outcomes

By the end of this module, you will be able to:

- Create and manage ROS 2 nodes
- Implement publisher-subscriber communication
- Build action servers for robot tasks
- Model humanoid robots using URDF

## Prerequisites

Before starting this module, ensure you have:

- Python programming basics
- Linux command line familiarity
- Basic networking concepts

## Chapters

### [Chapter 1: ROS 2 Architecture and Installation](./architecture.md)
- ROS 2 Architecture Overview
- ROS 2 vs ROS 1 Differences
- Installing ROS 2 Humble on Ubuntu 22.04
- Your First Publisher and Subscriber Nodes

### [Chapter 2: ROS 2 Communication Patterns](./communication.md)
- Topics, Services, and Actions
- Publisher-Subscriber Implementation
- Service Server and Client Examples
- Quality of Service (QoS) Configuration

### [Chapter 3: ROS 2 Packages and Build System](./packages.md)
- Understanding Package Structure
- Creating Packages with ros2 pkg create
- Configuring package.xml and setup.py
- Building with Colcon

### [Chapter 4: Launch Files and Parameters](./launch.md)
- Python Launch Files
- Multi-Node Launch Examples
- Parameter Declaration and Usage
- YAML Configuration Files

### [Chapter 5: URDF - Robot Modeling](./urdf.md)
- URDF Structure and Syntax
- Links with Visual, Collision, and Inertial Properties
- Joint Types (Revolute, Prismatic, Fixed, Continuous)
- Complete Humanoid Arm URDF Example

### [Chapter 6: Robot Controllers](./controllers.md)
- Controller Architecture
- ROS 2 Timer API for Control Loops
- Velocity and Position Controllers
- PID Control Implementation
- Feedback Control with Sensors

---

**Ready to Start?** Begin with [Chapter 1: ROS 2 Architecture and Installation](./architecture.md)

[Return to Homepage](/)
