---
id: 003
title: Physical AI Architecture Plan
stage: plan
date: 2025-12-06
surface: agent
model: claude-opus-4-5-20251101
feature: 001-docusaurus-book-layout
branch: 001-docusaurus-book-layout
user: architect
command: /sp.plan
labels: ["physical-ai", "ros2", "isaac", "gazebo", "vla", "architecture"]
links:
  spec: specs/001-docusaurus-book-layout/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-docusaurus-book-layout/plan.md
  - specs/001-docusaurus-book-layout/research.md
  - specs/001-docusaurus-book-layout/data-model.md
  - specs/001-docusaurus-book-layout/quickstart.md
  - specs/001-docusaurus-book-layout/contracts/modules-schema.json
  - specs/001-docusaurus-book-layout/contracts/modules.json
tests:
  - Constitution check passed for all 7 principles
  - JSON schema validates module data structure
---

## Prompt

Create:
- Architecture sketch for the Physical AI system (ROS 2, Gazebo/Unity, NVIDIA Isaac, VLA pipelines)
- Section structure for the technical book, aligned with modules and chapters
- Research approach: applied robotics, embodied AI, simulation-to-real workflows
- Quality validation methods for ROS 2 packages, simulations, and autonomous humanoid tasks

Decisions needing documentation:
- Hardware options: On-Premise RTX Workstation vs Cloud (AWS/Omniverse)
- Edge deployment: Jetson Orin Nano vs Orin NX
- Simulation tools: Gazebo vs Unity for digital twin visualization
- Sensor integration: LiDAR, Depth Cameras, IMUs selection and tradeoffs
- ROS 2 package architecture: Python agent integration and launch strategies

Testing strategy:
- Module-wise validation: ROS 2 nodes & topics, Gazebo physics accuracy, Isaac perception pipelines
- Simulation-to-Real tests: transferring models from Isaac Sim to Jetson Edge Kit
- Capstone validation: autonomous humanoid completing voice-command tasks
- Reproducibility checks: Docusaurus book instructions for demo replication

Technical details:
- Follow research-concurrent approach: implement, test, and document iteratively
- APA citation style for technical references
- Organize planning by phases:
    1. Research → Physical AI & humanoid robotics foundations
    2. Foundation → ROS 2, Gazebo/Unity, Isaac setup
    3. Analysis → Simulation, perception, control workflows
    4. Synthesis → Capstone integration & VLA pipelines
create plan.md from sp.plan.toml

## Response snapshot

Generated comprehensive implementation plan for Physical AI & Humanoid Robotics textbook with:

**Architecture Sketch**: 4-layer system architecture diagram showing:
- Module 4 (VLA): Whisper → LLM Intent → Action Map → Execute
- Module 3 (Isaac): Isaac Sim → Synthetic Data → TensorRT → Isaac ROS
- Module 2 (Digital Twin): Gazebo/Unity → Physics → Sensors → ros2_control
- Module 1 (ROS 2): Nodes ↔ Topics ↔ Services ↔ Actions

**Book Structure**: 4 modules, 21 chapters aligned with research-concurrent phases:
- Module 1: ROS 2 (5 chapters, Weeks 3-5)
- Module 2: Gazebo/Unity (6 chapters, Weeks 6-8)
- Module 3: NVIDIA Isaac (5 chapters, Weeks 9-11)
- Module 4: VLA Pipelines (5 chapters, Weeks 12-14)

**Key Decisions Documented**:
1. Simulation: Gazebo primary (ROS 2 native), Unity optional
2. Edge: Jetson Orin Nano ($199-299, student accessible)
3. VLA: Local inference (Whisper tiny/base, CLIP/YOLO small)
4. ROS 2: Standard package structure with rclpy

**Validation Methods**: 4-level testing strategy defined (module, sim-to-real, capstone, reproducibility)

## Outcome

- ✅ Impact: Complete planning artifacts generated for Physical AI textbook architecture
- 🧪 Tests: Constitution check passed (7/7 principles), JSON schema validated
- 📁 Files: 6 artifacts created (plan.md, research.md, data-model.md, quickstart.md, contracts/)
- 🔁 Next prompts: `/sp.tasks` to generate implementation tasks, `/sp.adr` for architectural decisions
- 🧠 Reflection: Comprehensive research phase resolved all technical unknowns; architecture aligns with free-tier accessibility and student-focused clarity principles

## Evaluation notes (flywheel)

- Failure modes observed: None - all research agents completed successfully
- Graders run and results (PASS/FAIL): Constitution check PASS (7/7)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Validate module data contract against Docusaurus TypeScript types during implementation
