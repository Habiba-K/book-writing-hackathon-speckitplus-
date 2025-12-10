---
id: 010
title: Simplify Chapter Naming Convention
stage: tasks
date: 2025-12-10
surface: claude-code
model: claude-opus-4-5-20251101
feature: 002-module-1-ros2-content
branch: 002-isaac-sim
user: developer
command: /sp.clarify
labels: [naming-convention, tasks-update, simplification]
links:
  spec: specs/002-module-1-ros2-content/spec.md
  ticket:
  adr:
  pr:
files:
  - specs/002-module-1-ros2-content/tasks.md
tests:
  - Verify all file paths updated consistently
---

## Prompt

Update 002-module-1-ros2-content (tasks.md) - change chapter naming from "Chapter X: Topic" format to just topic names:
- Chapter 1: Architecture → Architecture
- Chapter 2: Communication → Communication
- Chapter 3: Packages → Packages
- Chapter 4: Launch → Launch
- Chapter 5: URDF → URDF
- Chapter 6: Controllers → Controllers

Also update file paths from `chapter-X-topic.md` to `topic.md` format.

## Response snapshot

Updated tasks.md with simplified chapter naming:

**Task descriptions updated (T012-T017):**
- `Create Chapter 1: ROS 2 Architecture in chapter-1-architecture.md` → `Create Architecture chapter in architecture.md`
- `Create Chapter 2: ROS 2 Communication in chapter-2-communication.md` → `Create Communication chapter in communication.md`
- etc.

**File path references updated (T018-T033):**
- All references to `chapter-X-topic.md` changed to `topic.md`
- Example: `book-site/docs/module-1/chapter-1-architecture.md` → `book-site/docs/module-1/architecture.md`

**Parallel example section updated:**
- Task descriptions simplified to match new naming convention

## Outcome

- ✅ Impact: Cleaner, simpler file naming that focuses on content rather than ordering
- 🧪 Tests: All file path references consistent throughout tasks.md
- 📁 Files: 1 file updated (specs/002-module-1-ros2-content/tasks.md)
- 🔁 Next prompts: Run /sp.implement to execute updated tasks
- 🧠 Reflection: Simpler naming convention improves readability and allows chapter reordering without renaming files

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A - text update
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
