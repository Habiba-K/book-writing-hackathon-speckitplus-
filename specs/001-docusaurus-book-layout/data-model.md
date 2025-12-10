# Data Model: Physical AI & Humanoid Robotics Textbook

**Feature**: 001-docusaurus-book-layout
**Date**: 2025-12-06

## Core Entities

### 1. Module

Represents one of the 4 course modules in the textbook.

```typescript
interface Module {
  moduleNumber: 1 | 2 | 3 | 4;
  title: string;
  subtitle: string;
  timeframe: string;  // e.g., "Weeks 3-5"
  description: string;
  chapters: Chapter[];
  prerequisites: string[];
  learningOutcomes: string[];
  navigationPath: string;  // e.g., "/module-1"
}
```

**Validation Rules**:
- `moduleNumber` must be unique (1-4)
- `title` must be non-empty, max 100 characters
- `chapters` array must contain at least 1 chapter
- `navigationPath` must start with `/`

### 2. Chapter

Represents a chapter within a module.

```typescript
interface Chapter {
  chapterNumber: number;
  title: string;
  slug: string;  // URL-friendly identifier
  estimatedTime: string;  // e.g., "2-3 hours"
  objectives: string[];
  topics: Topic[];
  hasCodeExamples: boolean;
  hasLabExercise: boolean;
}
```

**Validation Rules**:
- `chapterNumber` must be positive integer
- `slug` must be lowercase, hyphenated, unique within module
- `objectives` array must have 2-5 items

### 3. Topic

Represents a subtopic or section within a chapter.

```typescript
interface Topic {
  title: string;
  description: string;
  conceptType: 'theory' | 'hands-on' | 'reference';
}
```

### 4. ModuleCard (UI Component Data)

Data structure for homepage module overview cards.

```typescript
interface ModuleCard {
  module: Module;
  icon: string;  // Icon identifier or path
  accentColor: string;  // CSS color for card styling
  status: 'available' | 'coming-soon' | 'in-progress';
}
```

---

## Module Content Definition

### Module 1: Robotic Nervous System (ROS 2)

```json
{
  "moduleNumber": 1,
  "title": "Robotic Nervous System",
  "subtitle": "ROS 2",
  "timeframe": "Weeks 3-5",
  "description": "Master the middleware layer that enables robot communication and control",
  "chapters": [
    {
      "chapterNumber": 1,
      "title": "ROS 2 Fundamentals",
      "slug": "ros2-fundamentals",
      "topics": [
        "Introduction to Robot Operating System",
        "ROS 2 vs ROS 1 Architecture",
        "Installation and Environment Setup",
        "First ROS 2 Program"
      ]
    },
    {
      "chapterNumber": 2,
      "title": "Nodes, Topics, and Services",
      "slug": "nodes-topics-services",
      "topics": [
        "Node Lifecycle Management",
        "Publisher-Subscriber Pattern",
        "Service Request-Response",
        "Quality of Service (QoS) Policies"
      ]
    },
    {
      "chapterNumber": 3,
      "title": "Actions and Python Agents",
      "slug": "actions-python-agents",
      "topics": [
        "Action Server Architecture",
        "rclpy Client Library",
        "Async Programming for Robotics",
        "Building Control Agents"
      ]
    },
    {
      "chapterNumber": 4,
      "title": "URDF for Humanoids",
      "slug": "urdf-humanoids",
      "topics": [
        "Robot Description Format",
        "Links, Joints, and Kinematics",
        "Humanoid Skeleton Modeling",
        "Visualization in RViz"
      ]
    },
    {
      "chapterNumber": 5,
      "title": "Launch Files and Packages",
      "slug": "launch-packages",
      "topics": [
        "Python Launch System",
        "Package Structure Best Practices",
        "Parameter Management",
        "Composition and Executors"
      ]
    }
  ],
  "prerequisites": [
    "Python programming basics",
    "Linux command line familiarity",
    "Basic networking concepts"
  ],
  "learningOutcomes": [
    "Create and manage ROS 2 nodes",
    "Implement publisher-subscriber communication",
    "Build action servers for robot tasks",
    "Model humanoid robots using URDF"
  ],
  "navigationPath": "/module-1"
}
```

### Module 2: Digital Twin (Gazebo & Unity)

```json
{
  "moduleNumber": 2,
  "title": "Digital Twin",
  "subtitle": "Gazebo & Unity",
  "timeframe": "Weeks 6-8",
  "description": "Build realistic simulations for testing and validation",
  "chapters": [
    {
      "chapterNumber": 6,
      "title": "Digital Twin Concepts",
      "slug": "digital-twin-concepts",
      "topics": [
        "What is a Digital Twin?",
        "Simulation vs Emulation",
        "Sim-to-Real Gap Analysis",
        "Use Cases in Robotics"
      ]
    },
    {
      "chapterNumber": 7,
      "title": "Gazebo Fundamentals",
      "slug": "gazebo-fundamentals",
      "topics": [
        "Gazebo Ignition Architecture",
        "SDF (Simulation Description Format)",
        "World Building Basics",
        "Model Import and Export"
      ]
    },
    {
      "chapterNumber": 8,
      "title": "Physics Simulation",
      "slug": "physics-simulation",
      "topics": [
        "DART Physics Engine",
        "Gravity and Collision Dynamics",
        "Joint Controllers (PID)",
        "Contact and Friction Modeling"
      ]
    },
    {
      "chapterNumber": 9,
      "title": "Sensor Simulation",
      "slug": "sensor-simulation",
      "topics": [
        "LiDAR Ray Casting",
        "RGB-D Camera Simulation",
        "IMU Noise Models",
        "Sensor Data Pipelines"
      ]
    },
    {
      "chapterNumber": 10,
      "title": "ROS 2 Control Integration",
      "slug": "ros2-control-integration",
      "topics": [
        "gz-ros2-control Bridge",
        "Hardware Interface Abstraction",
        "Controller Manager",
        "Real-Time Control Loops"
      ]
    },
    {
      "chapterNumber": 11,
      "title": "Unity Visualization",
      "slug": "unity-visualization",
      "topics": [
        "Unity Robotics Hub Setup",
        "ROS 2 TCP Bridge",
        "Advanced Rendering",
        "Demo Presentation"
      ]
    }
  ],
  "prerequisites": [
    "Module 1 completion",
    "Basic 3D geometry concepts"
  ],
  "learningOutcomes": [
    "Create realistic robot simulations in Gazebo",
    "Configure physics parameters for humanoids",
    "Simulate sensors with noise models",
    "Integrate simulation with ROS 2 control"
  ],
  "navigationPath": "/module-2"
}
```

### Module 3: NVIDIA Isaac (AI-Robot Brain)

```json
{
  "moduleNumber": 3,
  "title": "NVIDIA Isaac",
  "subtitle": "The AI-Robot Brain",
  "timeframe": "Weeks 9-11",
  "description": "Leverage GPU-accelerated perception and AI for intelligent robotics",
  "chapters": [
    {
      "chapterNumber": 12,
      "title": "Isaac Sim Introduction",
      "slug": "isaac-sim-intro",
      "topics": [
        "Omniverse Platform Overview",
        "USD (Universal Scene Description)",
        "Isaac Sim Interface",
        "Robot Import Workflow"
      ]
    },
    {
      "chapterNumber": 13,
      "title": "Synthetic Data Generation",
      "slug": "synthetic-data",
      "topics": [
        "Domain Randomization",
        "Automated Labeling",
        "Dataset Export Formats",
        "Training Data Pipelines"
      ]
    },
    {
      "chapterNumber": 14,
      "title": "Isaac ROS Perception",
      "slug": "isaac-ros-perception",
      "topics": [
        "isaac_ros_image_proc",
        "Object Detection with TensorRT",
        "Pose Estimation",
        "GPU-Accelerated Processing"
      ]
    },
    {
      "chapterNumber": 15,
      "title": "Visual SLAM and Navigation",
      "slug": "vslam-navigation",
      "topics": [
        "isaac_ros_visual_slam",
        "isaac_ros_nvblox",
        "Nav2 Integration",
        "Path Planning for Humanoids"
      ]
    },
    {
      "chapterNumber": 16,
      "title": "Sim-to-Real Transfer",
      "slug": "sim-to-real",
      "topics": [
        "Model Quantization (TensorRT)",
        "Jetson Deployment",
        "Domain Gap Mitigation",
        "Performance Validation"
      ]
    }
  ],
  "prerequisites": [
    "Module 1 and 2 completion",
    "NVIDIA GPU (RTX 3060+ recommended)",
    "Basic machine learning concepts"
  ],
  "learningOutcomes": [
    "Generate synthetic training data",
    "Deploy GPU-accelerated perception",
    "Implement visual SLAM for navigation",
    "Transfer models from simulation to real hardware"
  ],
  "navigationPath": "/module-3"
}
```

### Module 4: Vision-Language-Action (VLA)

```json
{
  "moduleNumber": 4,
  "title": "Vision-Language-Action",
  "subtitle": "VLA Pipelines",
  "timeframe": "Weeks 12-14",
  "description": "Build intelligent robots that understand and execute natural language commands",
  "chapters": [
    {
      "chapterNumber": 17,
      "title": "Voice to Intent",
      "slug": "voice-to-intent",
      "topics": [
        "OpenAI Whisper Integration",
        "Speech-to-Text Pipeline",
        "Intent Classification",
        "Command Validation"
      ]
    },
    {
      "chapterNumber": 18,
      "title": "Natural Language to ROS 2 Actions",
      "slug": "nl-to-actions",
      "topics": [
        "Semantic Action Mapping",
        "Parameter Extraction",
        "Action Schema Design",
        "Error Handling Patterns"
      ]
    },
    {
      "chapterNumber": 19,
      "title": "Multi-Modal Perception",
      "slug": "multimodal-perception",
      "topics": [
        "CLIP for Object Detection",
        "Scene Graph Representation",
        "Perception Fusion",
        "Grounding Language in Vision"
      ]
    },
    {
      "chapterNumber": 20,
      "title": "Autonomous Task Execution",
      "slug": "autonomous-execution",
      "topics": [
        "State Machine Design",
        "Multi-Step Task Planning",
        "Error Recovery Patterns",
        "Real-Time Feedback"
      ]
    },
    {
      "chapterNumber": 21,
      "title": "Capstone Integration",
      "slug": "capstone",
      "topics": [
        "Full VLA Pipeline Assembly",
        "Humanoid Task Demonstration",
        "Performance Optimization",
        "Future Directions"
      ]
    }
  ],
  "prerequisites": [
    "Modules 1-3 completion",
    "Basic NLP concepts",
    "Python async programming"
  ],
  "learningOutcomes": [
    "Convert voice commands to robot actions",
    "Integrate vision with language understanding",
    "Build autonomous task execution systems",
    "Complete a full VLA robotics project"
  ],
  "navigationPath": "/module-4"
}
```

---

## State Transitions

### Module Status Flow

```
COMING_SOON → IN_PROGRESS → AVAILABLE
```

For Iteration 1, all modules start as `COMING_SOON` with placeholder pages.

### Chapter Completion Flow (Student Progress)

```
NOT_STARTED → IN_PROGRESS → COMPLETED
```

(Note: Progress tracking is out of scope for Iteration 1)

---

## Data Storage Location

### Docusaurus Configuration
- Module data: `src/data/modules.json`
- Chapter content: `docs/module-X/chapter-Y.md`
- Homepage: `src/pages/index.tsx` or `src/pages/index.mdx`

### File Structure
```
book-site/
├── docusaurus.config.js
├── src/
│   ├── data/
│   │   └── modules.json       # Module definitions
│   ├── components/
│   │   └── ModuleCard.tsx     # Card component
│   └── pages/
│       └── index.tsx          # Homepage with cards
├── docs/
│   ├── module-1/
│   │   ├── _category_.json
│   │   └── *.md               # Chapter content
│   ├── module-2/
│   ├── module-3/
│   └── module-4/
└── static/
    └── img/                   # Module icons
```

---

## Relationships

```
┌─────────────┐
│   Module    │
│  (1 of 4)   │
└──────┬──────┘
       │ has many
       ▼
┌─────────────┐
│   Chapter   │
│  (5-6 each) │
└──────┬──────┘
       │ has many
       ▼
┌─────────────┐
│    Topic    │
│  (3-5 each) │
└─────────────┘
```

- Each Module has 5-6 Chapters
- Each Chapter has 3-5 Topics
- ModuleCard is a UI wrapper around Module
- Navigation paths link to Docusaurus doc pages
