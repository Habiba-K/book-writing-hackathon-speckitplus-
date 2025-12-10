# Data Model: Isaac Simulation Module

## Overview
This document defines the data model for Module 3: NVIDIA Isaac (AI-Robot Brain). The module is structured as educational content focused on Isaac Sim, synthetic data generation, Isaac ROS perception, VSLAM & navigation, and sim-to-real transfer.

## Entity: Chapter

### Attributes
- `id` (string): Unique identifier for the chapter (e.g., "chapter-12-isaac-sim-introduction")
- `title` (string): Full title of the chapter (e.g., "Chapter 12: Isaac Sim Introduction")
- `sidebar_label` (string): Label displayed in sidebar navigation
- `sidebar_position` (integer): Position in sidebar navigation (1-5 for this module)
- `content` (string): Markdown content of the chapter
- `learning_objectives` (array of strings): List of learning objectives for the chapter
- `prerequisites` (array of strings): List of prerequisite knowledge required
- `next_chapter` (string): Link to the next chapter

### Validation Rules
- `id` must be unique within the module
- `title` must follow format "Chapter X: Title" where X is 12-16
- `sidebar_position` must be between 1 and 5
- `content` must be in Markdown format
- `learning_objectives` must contain at least 1 item
- `prerequisites` may be empty but must be an array

### State Transitions
- `draft` → `review` → `published`: Content development lifecycle

## Entity: Module

### Attributes
- `id` (string): Unique identifier for the module ("module-3-isaac-sim")
- `title` (string): Module title ("Module 3: NVIDIA Isaac")
- `chapters` (array of Chapter entities): List of chapters in the module
- `learning_outcomes` (array of strings): Overall learning outcomes for the module
- `target_audience` (string): Description of target audience
- `timeframe` (string): Timeframe for completion (e.g., "Weeks 9-11")

### Validation Rules
- `id` must be "module-3-isaac-sim"
- `chapters` must contain exactly 5 chapters with positions 1-5
- `chapters` positions must be sequential (1, 2, 3, 4, 5)
- `learning_outcomes` must align with individual chapter objectives
- `target_audience` must match specification requirements

## Entity: IsaacSimEnvironment

### Attributes
- `name` (string): Name of the simulation environment
- `description` (string): Description of the environment
- `robots` (array of strings): List of robot models in the environment
- `sensors` (array of strings): List of sensors configured in the environment
- `physics_properties` (object): Physics properties of the environment

### Validation Rules
- `name` must be unique within the context
- `robots` must reference valid URDF/mesh files
- `sensors` must be compatible with Isaac Sim
- `physics_properties` must conform to Isaac Sim specifications

## Entity: SyntheticDataset

### Attributes
- `name` (string): Name of the dataset
- `description` (string): Description of the dataset
- `sensor_config` (object): Configuration of sensors used for generation
- `domain_randomization` (object): Domain randomization parameters
- `size` (integer): Number of samples in the dataset
- `labels` (object): Ground truth labels for the dataset

### Validation Rules
- `size` must be positive
- `sensor_config` must reference valid Isaac Sim sensors
- `labels` must be consistent with sensor data
- `domain_randomization` must be properly configured

## Entity: IsaacRosNode

### Attributes
- `name` (string): Name of the Isaac ROS node
- `type` (string): Type of processing (e.g., "object_detection", "segmentation", "depth")
- `input_topics` (array of strings): Input ROS topics
- `output_topics` (array of strings): Output ROS topics
- `parameters` (object): Configuration parameters
- `ros_version` (string): Compatible ROS version

### Validation Rules
- `name` must be unique within the context
- `type` must be one of predefined types
- `input_topics` and `output_topics` must be valid ROS topic names
- `ros_version` must be "humble" or compatible version

## Entity: VslamPipeline

### Attributes
- `name` (string): Name of the VSLAM pipeline
- `algorithm` (string): VSLAM algorithm type (e.g., "ORB-SLAM", "LSD-SLAM")
- `input_sources` (array of strings): Input data sources (e.g., "camera", "lidar")
- `output` (string): Output type (e.g., "map", "pose")
- `parameters` (object): Algorithm-specific parameters

### Validation Rules
- `algorithm` must be a valid VSLAM algorithm
- `input_sources` must be compatible with Isaac Sim
- `output` must be a valid SLAM output type

## Entity: SimToRealTransfer

### Attributes
- `method` (string): Transfer method (e.g., "domain_randomization", "system_id")
- `physics_consistency` (object): Physics consistency parameters
- `sensor_calibration` (object): Sensor calibration parameters
- `policy_adaptation` (object): Policy adaptation techniques
- `validation_metrics` (array of strings): Metrics for validation

### Validation Rules
- `method` must be a valid transfer method
- `physics_consistency` must include necessary parameters
- `sensor_calibration` must specify calibration procedures
- `validation_metrics` must be measurable

## Relationships

### Chapter to Module
- One Module contains 5 Chapters (1-to-many)
- Each Chapter belongs to exactly one Module

### IsaacSimEnvironment to Chapter
- One Chapter may reference multiple IsaacSimEnvironments (many-to-many)
- Used in Chapters 12 and 13

### SyntheticDataset to Chapter
- One Chapter may generate multiple SyntheticDatasets (1-to-many)
- Used in Chapter 13

### IsaacRosNode to Chapter
- One Chapter may use multiple IsaacRosNodes (1-to-many)
- Used in Chapter 14

### VslamPipeline to Chapter
- One Chapter may implement multiple VslamPipelines (1-to-many)
- Used in Chapter 15

### SimToRealTransfer to Chapter
- One Chapter may apply multiple SimToRealTransfer methods (1-to-many)
- Used in Chapter 16

## Constraints

### Content Constraints
- All content must be theory-focused with minimal examples
- No implementation details (APIs, frameworks) in specification
- All chapters must be single files (no sub-folders)
- Content must follow accessibility standards

### Performance Constraints
- Chapter pages must load within 2 seconds on 3G
- Total site build must remain under 10 seconds
- Code blocks must support horizontal scrolling on mobile
- Code font size must be readable on mobile (≥14px)

### Technical Constraints
- Content must be in Markdown format with minimal images
- All Python code examples must conform to PEP 8
- Search indexing must include all content body text
- Content must be accessible to screen readers using semantic HTML