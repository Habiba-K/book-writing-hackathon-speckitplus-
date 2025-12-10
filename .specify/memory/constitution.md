<!--
Sync Impact Report - Constitution v1.0.0
================================================================================
Version Change: Template → 1.0.0 (Initial ratification)
Date: 2025-12-05

Modified Principles:
  - Created 7 new principles (Simplicity, Accuracy, Minimalism, Free-Tier Friendly,
    Student-Focused Clarity, Documentation-Based, Consistency)

Added Sections:
  - Core Principles (7 principles defined)
  - Content Standards (chapter and module requirements)
  - Technical Requirements (Docusaurus, GitHub Pages, deployment)
  - Governance (amendment process, compliance)

Removed Sections:
  - Generic template placeholders

Templates Requiring Updates:
  ✅ plan-template.md - Reviewed, aligns with constitution
  ✅ spec-template.md - Reviewed, aligns with constitution
  ✅ tasks-template.md - Reviewed, aligns with constitution
  ⚠️  No command files found in .specify/templates/commands/ - none to update

Follow-up TODOs:
  - None - all placeholders filled
================================================================================
-->

# Physical AI & Humanoid Robotics Textbook Constitution

## Core Principles

### I. Simplicity

All content, code examples, and instructions MUST prioritize clarity over complexity. Every chapter, example, and command MUST be understandable by students with basic programming knowledge. Complex concepts MUST be broken down into incremental steps with clear explanations at each stage.

**Rationale**: Students learning robotics face inherent complexity in the domain itself. The textbook must not add unnecessary cognitive load through unclear writing, overly technical jargon without explanation, or poorly structured content.

### II. Accuracy

All technical content MUST be based on official documentation sources. Commands, code examples, and configuration steps MUST be validated in a real development environment before inclusion. No speculative or assumed solutions are permitted.

**Official Documentation Sources**:
- Docusaurus: https://docusaurus.io/docs
- ROS 2 official documentation
- NVIDIA Isaac documentation
- Gazebo and Unity official documentation
- GitHub Pages official guides

**Rationale**: Inaccurate technical instructions lead to student frustration, wasted time debugging errors that stem from the textbook itself, and erosion of trust in the learning material.

### III. Minimalism

Content MUST include only what is necessary to achieve learning objectives. Avoid feature creep, excessive configuration options, or tangential topics that distract from core concepts.

**Rationale**: Students have limited time and attention. Every additional feature or option multiplies the testing burden and increases the chance of confusion or errors.

### IV. Free-Tier Friendly Architecture

All tools, platforms, and services used MUST have free-tier options suitable for student use. Examples and exercises MUST NOT require expensive GPU resources, paid API access, or premium subscriptions.

**Constraints**:
- No heavy GPU usage requirements
- Minimal embeddings and computational overhead
- All cloud services must have functional free tiers
- Local development must be possible on standard student hardware

**Rationale**: Accessibility is critical. Students should not face financial barriers to learning. Projects requiring expensive resources exclude students from lower-income backgrounds.

### V. Student-Focused Clarity

All writing MUST use clear, simple English. Technical terms MUST be defined on first use. Chapters MUST follow a consistent structure that aids comprehension and navigation.

**Standard Chapter Layout**:
1. Introduction (what and why)
2. Core Concepts (foundational knowledge)
3. Step-by-Step Instructions (numbered, testable)
4. Code Examples (annotated, runnable)
5. Checklist (self-verification)

**Rationale**: Consistent structure reduces cognitive load, helps students know what to expect, and enables them to find information quickly when reviewing material.

### VI. Documentation-Based Development

All content creation and technical implementation MUST reference official documentation. Use official CLI commands, official API references, and official best practices. Do not invent approaches or rely solely on AI-generated knowledge.

**Sources of Truth**:
- Docusaurus official docs for site architecture
- Spec-Kit Plus methodology for project structure
- GitHub Pages official deployment guides
- Official robotics framework documentation (ROS 2, Isaac, etc.)

**Rationale**: Official documentation represents tested, maintained, and community-validated approaches. Deviating from official guidance leads to maintenance issues, compatibility problems, and student confusion when seeking help.

### VII. Consistency in Formatting and Terminology

Use consistent formatting conventions throughout the textbook. Technical terms MUST use the same spelling, capitalization, and phrasing across all chapters. Code formatting MUST follow language-specific best practices.

**Standards**:
- Markdown headings: Title Case for major headings, Sentence case for subheadings
- Code blocks: Language-tagged fenced blocks with syntax highlighting
- Commands: Presented in separate code blocks with expected output shown
- File paths: Use monospace formatting
- Emphasis: Bold for important terms on first use, italics for clarification

**Rationale**: Consistency aids pattern recognition and comprehension. Inconsistent terminology causes confusion about whether two terms refer to the same concept or different ones.

## Content Standards

### Chapter Requirements

Each chapter MUST include:

1. **Specification**: Clear statement of what the chapter covers and learning objectives
2. **Objectives**: Bulleted list of specific, measurable learning outcomes
3. **Examples**: At least one worked example demonstrating core concepts
4. **Steps**: Numbered, sequential instructions that are independently testable
5. **Code**: Annotated code examples with comments explaining key lines
6. **Final Exercise**: Hands-on task that tests comprehension of chapter material

**Validation**: Before marking a chapter complete, verify that all six elements are present and meet quality standards.

### Module Requirements

Each of the 4 modules MUST include:

1. **Inputs**: Clear specification of prerequisites (prior knowledge, installed software, configuration)
2. **Outputs**: Explicit description of what students will be able to do after completing the module
3. **Architecture**: High-level diagram or explanation of how components fit together
4. **Code Failure Modes**: Common errors students may encounter with troubleshooting guidance
5. **Safety Rules**: Critical warnings about operations that could damage systems or data

**Module Structure**:
- **Module 1**: ROS 2 – The Robotic Nervous System (Middleware, nodes, topics, services, Python agents via rclpy, URDF for humanoids)
- **Module 2**: Digital Twin – Gazebo & Unity (Physics simulation, gravity, collisions, dynamics, Unity visualization, simulated sensors)
- **Module 3**: NVIDIA Isaac – The AI-Robot Brain (Isaac Sim, synthetic data, Isaac ROS VSLAM, perception, Nav2 path planning)
- **Module 4**: Vision-Language-Action (VLA) (LLM + Robotics, Whisper Voice-to-Action, natural language to ROS 2 actions, capstone autonomous humanoid)

## Technical Requirements

### Docusaurus Implementation

All Docusaurus configuration and code MUST follow TypeScript best practices as documented in the official Docusaurus guides.

**Requirements**:
- Clean, modern UI using official Docusaurus themes
- Mobile-responsive design (test on multiple screen sizes)
- Fast build times (optimize images, minimize dependencies)
- Successful local development server (`npm start` or `yarn start`)
- Successful production build (`npm run build` or `yarn build`)

### GitHub Pages Deployment

Deployment instructions MUST be 100% correct and reproducible. Every command MUST be tested in a real repository environment.

**Deployment Checklist**:
- [ ] Repository configured for GitHub Pages
- [ ] Build output directory configured correctly
- [ ] Base URL configured for repository name
- [ ] Deploy script tested and working
- [ ] Published site accessible and renders correctly
- [ ] All links functional (no 404 errors)

### Build Validation

Before considering content complete, ALL of the following MUST pass:

- [ ] `npm run build` or `yarn build` completes without errors
- [ ] No TypeScript compilation errors
- [ ] No broken internal links (run link checker)
- [ ] All code examples have been tested in appropriate environments
- [ ] All commands have been validated on target platform (Windows/Linux/macOS as applicable)

## Governance

### Constitution Authority

This constitution supersedes all other practices and guidelines. When conflicts arise between this constitution and other documentation, the constitution takes precedence.

### Amendments

Amendments to this constitution require:

1. **Documentation**: Proposal with rationale explaining why change is needed
2. **Approval**: Consensus from project stakeholders (faculty, lead developers)
3. **Migration Plan**: If changes affect existing content, provide plan to update affected chapters
4. **Version Update**: Increment constitution version using semantic versioning

**Semantic Versioning for Constitution**:
- **MAJOR**: Backward-incompatible changes (removing principles, changing fundamental approach)
- **MINOR**: New principles or sections added, material expansion of guidance
- **PATCH**: Clarifications, typo fixes, wording improvements

### Compliance Verification

All pull requests and content reviews MUST verify compliance with this constitution. Reviewers MUST:

- Check that content follows the 7 core principles
- Verify chapter and module requirements are met
- Confirm all technical requirements pass
- Flag any complexity that is not justified by learning value

### Complexity Justification

Any violation of the Simplicity or Minimalism principles MUST be explicitly justified with:

1. **Why Needed**: Specific learning objective that requires this complexity
2. **Simpler Alternative Rejected**: Explanation of why simpler approach is insufficient
3. **Mitigation**: Steps taken to minimize the complexity impact on students

**Version**: 1.0.0 | **Ratified**: 2025-12-05 | **Last Amended**: 2025-12-05
