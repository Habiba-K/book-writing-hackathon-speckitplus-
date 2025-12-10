# Implementation Plan: Docusaurus Book Layout with Physical AI Architecture

**Branch**: `001-docusaurus-book-layout` | **Date**: 2025-12-06 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-docusaurus-book-layout/spec.md`

## Summary

Create a Docusaurus-based technical textbook for Physical AI & Humanoid Robotics, featuring a homepage with 4 module overview cards and comprehensive architecture for ROS 2, Gazebo/Unity simulation, NVIDIA Isaac, and VLA pipelines. The book follows a research-concurrent approach with iterative implementation, testing, and documentation.

## Technical Context

**Language/Version**: TypeScript 5.x (Docusaurus), Python 3.11 (robotics code examples)
**Primary Dependencies**: Docusaurus 3.x, React 18, MDX 3.x
**Storage**: JSON configuration files for module data, Markdown/MDX for content
**Testing**: Manual validation, `npm run build` for Docusaurus, pytest for code examples
**Target Platform**: GitHub Pages (static site), cross-platform for robotics content
**Project Type**: Web (documentation/textbook site)
**Performance Goals**: < 3s page load, instant navigation between chapters
**Constraints**: Free-tier friendly (no GPU for site build), WCAG 2.1 AA accessibility
**Scale/Scope**: 4 modules, 21 chapters, ~50 pages total

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. Simplicity | ✅ PASS | Incremental chapter structure, standard Docusaurus patterns |
| II. Accuracy | ✅ PASS | All content based on official docs (ROS 2, NVIDIA, Gazebo) |
| III. Minimalism | ✅ PASS | Only essential features for Iteration 1 (cards + placeholders) |
| IV. Free-Tier Friendly | ✅ PASS | Docusaurus, GitHub Pages, Whisper local - all free |
| V. Student-Focused Clarity | ✅ PASS | Standard chapter layout defined in constitution |
| VI. Documentation-Based | ✅ PASS | Research.md references official sources |
| VII. Consistency | ✅ PASS | JSON schema for modules, Markdown standards |

**Gate Result**: PASS - No violations. Proceed with implementation.

## Project Structure

### Documentation (this feature)

```text
specs/001-docusaurus-book-layout/
├── plan.md              # This file
├── spec.md              # Feature requirements
├── research.md          # Phase 0 research findings
├── data-model.md        # Entity definitions
├── quickstart.md        # Developer setup guide
├── contracts/
│   ├── modules-schema.json   # JSON Schema for modules
│   └── modules.json          # Module data contract
└── tasks.md             # Phase 2 output (from /sp.tasks)
```

### Source Code (Docusaurus site)

```text
book-site/
├── docusaurus.config.js       # Site configuration
├── sidebars.js                # Navigation structure
├── package.json               # Dependencies
├── src/
│   ├── components/
│   │   ├── ModuleCard/
│   │   │   ├── index.tsx      # Card component
│   │   │   └── styles.module.css
│   │   └── HomepageModules/
│   │       ├── index.tsx      # Grid layout
│   │       └── styles.module.css
│   ├── data/
│   │   └── modules.json       # Module definitions
│   ├── pages/
│   │   ├── index.tsx          # Homepage
│   │   └── index.module.css
│   └── css/
│       └── custom.css         # Global styles
├── docs/
│   ├── module-1/
│   │   ├── _category_.json
│   │   ├── index.md           # Module 1 placeholder
│   │   └── ...chapters
│   ├── module-2/
│   ├── module-3/
│   └── module-4/
└── static/
    └── img/
        └── module-icons/      # SVG icons
```

**Structure Decision**: Web application pattern selected - Docusaurus generates static site with React components for dynamic features (module cards). Content stored as Markdown in `docs/` folder.

## Architecture Overview

### Physical AI System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     Physical AI System Architecture                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                    Module 4: VLA Pipeline                         │   │
│  │  ┌─────────┐   ┌─────────────┐   ┌──────────────┐   ┌─────────┐ │   │
│  │  │ Whisper │ → │ LLM Intent  │ → │ Action Map   │ → │ Execute │ │   │
│  │  │ (Voice) │   │ (Semantic)  │   │ (ROS 2 Goal) │   │ (State) │ │   │
│  │  └─────────┘   └─────────────┘   └──────────────┘   └─────────┘ │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                    ↓                                     │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                 Module 3: NVIDIA Isaac Perception                 │   │
│  │  ┌───────────┐   ┌────────────┐   ┌──────────┐   ┌────────────┐ │   │
│  │  │ Isaac Sim │ → │ Synthetic  │ → │ TensorRT │ → │ Isaac ROS  │ │   │
│  │  │ (USD)     │   │ Data Gen   │   │ (Quant)  │   │ (Percept)  │ │   │
│  │  └───────────┘   └────────────┘   └──────────┘   └────────────┘ │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                    ↓                                     │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                Module 2: Digital Twin Simulation                  │   │
│  │  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌───────────────┐ │   │
│  │  │ Gazebo   │ ← │ Physics  │ ← │ Sensors  │ ← │ ros2_control  │ │   │
│  │  │ (World)  │   │ (DART)   │   │ (Ray/IMU)│   │ (HW Bridge)   │ │   │
│  │  └──────────┘   └──────────┘   └──────────┘   └───────────────┘ │   │
│  │       ↑                                                          │   │
│  │  ┌──────────┐   (Optional visualization)                         │   │
│  │  │ Unity    │                                                    │   │
│  │  │ (Render) │                                                    │   │
│  │  └──────────┘                                                    │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                    ↓                                     │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                   Module 1: ROS 2 Middleware                      │   │
│  │  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌───────────────┐ │   │
│  │  │ Nodes    │ ↔ │ Topics   │ ↔ │ Services │ ↔ │ Actions       │ │   │
│  │  │ (rclpy)  │   │ (Pub/Sub)│   │ (Req/Res)│   │ (Goal/Feed)   │ │   │
│  │  └──────────┘   └──────────┘   └──────────┘   └───────────────┘ │   │
│  │       ↑                                                          │   │
│  │  ┌──────────┐   ┌──────────┐   ┌──────────┐                      │   │
│  │  │ URDF     │   │ Launch   │   │ Package  │                      │   │
│  │  │ (Model)  │   │ (Config) │   │ (Struct) │                      │   │
│  │  └──────────┘   └──────────┘   └──────────┘                      │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                    ↓                                     │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                      Hardware Layer                               │   │
│  │  ┌──────────────┐   ┌───────────────────┐   ┌─────────────────┐ │   │
│  │  │ RTX Workstation│  │ Jetson Orin Nano  │  │ Humanoid Robot  │ │   │
│  │  │ (Development)  │  │ (Edge Deploy)     │  │ (Real Hardware) │ │   │
│  │  └──────────────┘   └───────────────────┘   └─────────────────┘ │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Book Section Structure (aligned with modules)

```
Physical AI & Humanoid Robotics Textbook
│
├── Module 1: Robotic Nervous System (ROS 2) [Weeks 3-5]
│   ├── Chapter 1: ROS 2 Architecture and Installation
│   ├── Chapter 2: ROS 2 Communication Patterns
│   ├── Chapter 3: ROS 2 Packages and Build System
│   ├── Chapter 4: Launch Files and Parameters
│   └── Chapter 5: URDF - Unified Robot Description Format and Robot Controllers
│
├── Module 2: Digital Twin (Gazebo & Unity) [Weeks 6-8]
│   ├── Chapter 6: Digital Twin Concepts
│   ├── Chapter 7: Gazebo Fundamentals
│   ├── Chapter 8: Physics Simulation
│   ├── Chapter 9: Sensor Simulation
│   ├── Chapter 10: ROS 2 Control Integration
│   └── Chapter 11: Unity Visualization (Optional)
│
├── Module 3: NVIDIA Isaac (AI-Robot Brain) [Weeks 9-11]
│   ├── Chapter 12: Isaac Sim Introduction
│   ├── Chapter 13: Synthetic Data Generation
│   ├── Chapter 14: Isaac ROS Perception
│   ├── Chapter 15: Visual SLAM & Navigation
│   └── Chapter 16: Sim-to-Real Transfer
│
└── Module 4: Vision-Language-Action (VLA) [Weeks 12-14]
    ├── Chapter 17: Voice to Intent (Whisper)
    ├── Chapter 18: NL to ROS 2 Actions
    ├── Chapter 19: Multi-Modal Perception
    ├── Chapter 20: Autonomous Task Execution
    └── Chapter 21: Capstone Integration
```

## Research Approach

### Research-Concurrent Development Phases

```
Phase 1: Research (Weeks 1-2)
├── Physical AI & humanoid robotics foundations
├── Literature review of ROS 2, Isaac, VLA
├── Define chapter objectives and prerequisites
└── Output: research.md, module structure

Phase 2: Foundation (Weeks 3-8)
├── Module 1: ROS 2 implementation & testing
├── Module 2: Gazebo/Unity setup & validation
├── Document iteratively as building
└── Output: Chapters 1-11 with tested examples

Phase 3: Analysis (Weeks 9-11)
├── Module 3: Isaac simulation & perception
├── Sim-to-real transfer experiments
├── Performance benchmarking
└── Output: Chapters 12-16 with benchmarks

Phase 4: Synthesis (Weeks 12-14)
├── Module 4: VLA pipeline integration
├── Capstone project development
├── Full system validation
└── Output: Chapters 17-21, capstone demo
```

### APA Citation Style

All technical references follow APA 7th edition format:
- ROS 2 Documentation. (2024). https://docs.ros.org/en/humble/
- NVIDIA. (2024). Isaac Sim Documentation. https://docs.nvidia.com/isaac-sim/
- Open Robotics. (2024). Gazebo Documentation. https://gazebosim.org/docs

## Quality Validation Methods

### Level 1: Module-wise Validation

| Component | Validation Method | Acceptance Criteria |
|-----------|-------------------|---------------------|
| ROS 2 nodes & topics | `ros2 topic list`, `ros2 node list` | All nodes discoverable |
| Gazebo physics | Gravity drop test, collision checks | Objects fall at 9.81 m/s² |
| Isaac perception | Inference accuracy benchmark | >90% detection on test set |

### Level 2: Simulation-to-Real Tests

```bash
# Model export validation
trtexec --onnx=model.onnx --int8 --saveEngine=model.plan

# Jetson deployment check
ros2 launch humanoid_bringup jetson.launch.py

# Performance metrics
ros2 run tf2_ros buffer_server  # latency check
```

### Level 3: Capstone Validation

- [ ] Voice command recognized (Whisper accuracy >95%)
- [ ] Intent parsed correctly (JSON schema valid)
- [ ] Action executed (humanoid completes task)
- [ ] Error recovery works (retry on failure)

### Level 4: Reproducibility Checks

- [ ] Docusaurus `npm run build` passes
- [ ] All code examples copy-paste runnable
- [ ] Cross-platform tested (Linux, Windows WSL)
- [ ] Demo replication on fresh environment

## Key Decisions Requiring ADR

📋 **Architectural decisions detected that should be documented:**

1. **ADR-001: Simulation Platform Selection**
   - Decision: Gazebo primary, Unity optional for visualization
   - Rationale: Native ROS 2 integration, research-grade physics
   - Run: `/sp.adr simulation-platform-selection`

2. **ADR-002: Edge Hardware Selection**
   - Decision: Jetson Orin Nano primary, Orin NX for advanced
   - Rationale: Cost-accessibility for students ($199-299)
   - Run: `/sp.adr edge-hardware-selection`

3. **ADR-003: VLA Pipeline Architecture**
   - Decision: Local inference (Whisper tiny/base, CLIP/YOLO small)
   - Rationale: Free-tier friendly, no cloud API costs
   - Run: `/sp.adr vla-pipeline-architecture`

4. **ADR-004: ROS 2 Package Structure**
   - Decision: Standard package layout with rclpy, launch files
   - Rationale: Community best practices, maintainability
   - Run: `/sp.adr ros2-package-structure`

## Complexity Tracking

No constitution violations identified. All decisions align with:
- Simplicity: Standard Docusaurus, proven robotics patterns
- Minimalism: Iteration 1 delivers only homepage + placeholders
- Free-Tier: All tools accessible without cost

| Potential Complexity | Mitigation |
|---------------------|------------|
| Isaac Sim GPU requirement | Documented as Module 3 prerequisite, cloud alternative provided |
| VLA pipeline complexity | Broken into 5 chapters with incremental learning |
| Sim-to-real gap | Explicit chapter (16) on domain gap mitigation |

## Implementation Phases Summary

### Phase 0: Research ✅ COMPLETE
- Output: `research.md` with all decisions documented
- All NEEDS CLARIFICATION items resolved

### Phase 1: Design ✅ COMPLETE
- Output: `data-model.md`, `contracts/`, `quickstart.md`
- JSON schema for module configuration
- Module data contract with 4 modules, 21 chapters

### Phase 2: Tasks (Next Step)
- Run: `/sp.tasks` to generate implementation tasks
- Output: `tasks.md` with testable implementation steps

## Generated Artifacts

| Artifact | Path | Status |
|----------|------|--------|
| Research | `specs/001-docusaurus-book-layout/research.md` | ✅ Complete |
| Data Model | `specs/001-docusaurus-book-layout/data-model.md` | ✅ Complete |
| Module Schema | `specs/001-docusaurus-book-layout/contracts/modules-schema.json` | ✅ Complete |
| Module Data | `specs/001-docusaurus-book-layout/contracts/modules.json` | ✅ Complete |
| Quickstart | `specs/001-docusaurus-book-layout/quickstart.md` | ✅ Complete |
| Tasks | `specs/001-docusaurus-book-layout/tasks.md` | ⏳ Pending `/sp.tasks` |

---

**Next Steps**:
1. Run `/sp.tasks` to generate implementation task list
2. Run `/sp.adr <title>` for each architectural decision if desired
3. Begin Iteration 1 implementation (homepage + module cards)
