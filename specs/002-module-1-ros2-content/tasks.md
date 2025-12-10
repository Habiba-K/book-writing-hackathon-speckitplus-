---

description: "Task list for Module 1-4 ROS 2 Content with Installation and Code Examples"
---

# Tasks: Module 1-4 ROS 2 Content with Installation and Code Examples

**Input**: Design documents from `/specs/002-module-1-ros2-content/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: No specific test tasks are generated as per `spec.md` - students will verify examples manually.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description with file path`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- Paths assume Docusaurus project in `book-site/` at repository root.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic Docusaurus content structure for all modules.

- [ ] T001 Create `book-site/docs/module-1/` directory
- [ ] T002 Create `book-site/docs/module-2/` directory
- [ ] T003 Create `book-site/docs/module-3/` directory
- [ ] T004 Create `book-site/docs/module-4/` directory
- [ ] T005 Update `book-site/sidebars.ts` to include Module 1 in sidebar with chapters: "Architecture", "Communication", "Packages", "Launch", "URDF", "Controllers" (FR-022)
- [ ] T006 Update `book-site/sidebars.ts` to include Module 2 in sidebar
- [ ] T007 Update `book-site/sidebars.ts` to include Module 3 in sidebar
- [ ] T008 Update `book-site/sidebars.ts` to include Module 4 in sidebar

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core Docusaurus configuration to support the book layout and ensure basic build.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T009 Verify Docusaurus 3.x installation and configuration in `book-site/docusaurus.config.ts`
- [ ] T010 Run `npm install` in `book-site/` to ensure all Docusaurus dependencies are met
- [ ] T011 Run `npm run build` in `book-site/` to validate initial site build

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - View Chapter with Installation & Code (Priority: P1) 🎯 MVP

**Goal**: Students can read chapters with ROS 2 installation commands and complete runnable code examples, so they can learn ROS 2 fundamentals and set up their development environment.

**Independent Test**: Navigate to any of 6 chapters, verify content displays with code syntax highlighting and copy buttons functional.

### Implementation for User Story 1 (Module 1 Chapters)

- [ ] T012 [P] [US1] Create Architecture chapter in `book-site/docs/module-1/architecture.md`
- [ ] T013 [P] [US1] Create Communication chapter in `book-site/docs/module-1/communication.md`
- [ ] T014 [P] [US1] Create Packages chapter in `book-site/docs/module-1/packages.md`
- [ ] T015 [P] [US1] Create Launch chapter in `book-site/docs/module-1/launch.md`
- [ ] T016 [P] [US1] Create URDF chapter in `book-site/docs/module-1/urdf.md`
- [ ] T017 [P] [US1] Create Controllers chapter in `book-site/docs/module-1/controllers.md`
- [ ] T018 [US1] Add Ubuntu 22.04 ROS 2 Humble installation commands to `book-site/docs/module-1/architecture.md` (FR-003)
- [ ] T019 [US1] Add sample Python publisher/subscriber code with highlighting to `book-site/docs/module-1/architecture.md` (FR-004)
- [ ] T020 [US1] Add 4 runnable code examples (publisher, subscriber, service server, service client) to `book-site/docs/module-1/communication.md` (FR-005)
- [ ] T021 [US1] Add terminal commands for executing code examples to `book-site/docs/module-1/communication.md` (FR-006)
- [ ] T022 [US1] Describe ROS 2 package directory structure in `book-site/docs/module-1/packages.md` (FR-007)
- [ ] T023 [US1] Add annotated `setup.py` template to `book-site/docs/module-1/packages.md` (FR-008)
- [ ] T024 [US1] Add colcon build, install, source commands to `book-site/docs/module-1/packages.md` (FR-009)
- [ ] T025 [US1] Add complete Python launch file example that starts 2+ nodes to `book-site/docs/module-1/launch.md` (FR-010)
- [ ] T026 [US1] Add YAML parameter file example with node namespaces and parameter definitions to `book-site/docs/module-1/launch.md` (FR-011)
- [ ] T027 [US1] Demonstrate parameter declaration and retrieval in Python nodes in `book-site/docs/module-1/launch.md` (FR-012)
- [ ] T028 [US1] Explain URDF XML syntax for links in `book-site/docs/module-1/urdf.md` (FR-013)
- [ ] T029 [US1] Explain URDF joint types (revolute, prismatic, fixed) with axis definitions in `book-site/docs/module-1/urdf.md` (FR-014)
- [ ] T030 [US1] Include complete sample humanoid arm URDF with 3-4 joints (shoulder, elbow, wrist) in `book-site/docs/module-1/urdf.md` (FR-015)
- [ ] T031 [US1] Add complete controller node code that subscribes to sensor topics to `book-site/docs/module-1/controllers.md` (FR-016)
- [ ] T032 [US1] Demonstrate publishing velocity or torque commands to actuator topics in `book-site/docs/module-1/controllers.md` (FR-017)
- [ ] T033 [US1] Explain control loop timing using ROS 2 Timer API in `book-site/docs/module-1/controllers.md` (FR-018)
- [ ] T034 [US1] Ensure all Python code examples follow PEP 8 style guide conventions (FR-024)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Learn ROS 2 Fundamentals Sequentially (Priority: P1)

**Goal**: Students can progress through 6 chapters in order (architecture → communication → packages → launch → URDF → controllers), so they can build knowledge incrementally.

**Independent Test**: Navigate Chapter 1→2→3→4→5→6 using Next links, verify each chapter covers expected topic with code examples.

### Implementation for User Story 2

- [ ] T035 [US2] Verify Previous/Next navigation links for all chapters in `book-site/docs/module-1/` (FR-002)
- [ ] T036 [US2] Verify bidirectional navigation (Module 1 overview ← → Chapters) (FR-022)
- [ ] T037 [US2] Update `book-site/sidebars.ts` to ensure all 6 chapters for Module 1 are listed as "Architecture", "Communication", "Packages", "Launch", "URDF", "Controllers" with current highlighted (FR-022)
- [ ] T038 [US2] Verify sidebar displays exact chapter names: "Architecture", "Communication", "Packages", "Launch", "URDF", "Controllers" in browser (FR-022)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Search Chapter Content (Priority: P2)

**Goal**: Students can search for specific topics (like "publisher" or "URDF"), so they can quickly find relevant chapter sections.

**Independent Test**: Use Docusaurus search to find "publisher", "URDF", "launch file" - verify results link to correct chapters.

### Implementation for User Story 3

- [ ] T039 [US3] Verify all chapters in `book-site/docs/module-1/` are indexed by Docusaurus search functionality (FR-023)
- [ ] T040 [US3] Test Docusaurus search with keywords like "ROS 2 publisher", "URDF joints", or "colcon build"

**Checkpoint**: All user stories should now be independently functional

---

## Final Phase: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T041 Verify all code blocks use syntax highlighting for appropriate languages (Python, bash, XML, YAML) (FR-019)
- [ ] T042 Verify all code blocks include copy-to-clipboard button (provided by Docusaurus default features) (FR-020)
- [ ] T043 Verify chapters render correctly on mobile, tablet, and desktop viewports (FR-021, NFR-001, NFR-003, NFR-008)
- [ ] T044 Run `npm run build` in `book-site/` to ensure total site build time remains under 10 seconds (NFR-002)
- [ ] T045 Verify search indexing includes all chapter content body text and code block comments (NFR-005)
- [ ] T046 Verify page content is accessible to screen readers using semantic HTML (NFR-006)
- [ ] T047 Verify chapter navigation supports keyboard-only operation (Tab key navigation, Enter to activate) (NFR-007)
- [ ] T048 Verify sidebar displays exact chapter names: "Architecture", "Communication", "Packages", "Launch", "URDF", "Controllers" as specified in FR-022

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Content creation before verification.
- Models before services.
- Services before endpoints.
- Core implementation before integration.
- Story complete before moving to next priority.

### Parallel Opportunities

- All Setup tasks T001-T004 can run in parallel.
- All Setup tasks T005-T008 can run in parallel.
- Foundational tasks T009-T011 can run in parallel (if Docusaurus config verification and npm install/build are independent steps).
- Once Foundational phase completes, User Story 1, 2, and 3 can start in parallel (if team capacity allows, with focus on P1 first).
- Within User Story 1, tasks T012-T017 (chapter creation) can run in parallel.
- Different user stories can be worked on in parallel by different team members.

---

## Parallel Example: User Story 1

```bash
# Launch all chapter creation tasks for User Story 1 together:
Task: "Create Architecture chapter in book-site/docs/module-1/architecture.md"
Task: "Create Communication chapter in book-site/docs/module-1/communication.md"
Task: "Create Packages chapter in book-site/docs/module-1/packages.md"
Task: "Create Launch chapter in book-site/docs/module-1/launch.md"
Task: "Create URDF chapter in book-site/docs/module-1/urdf.md"
Task: "Create Controllers chapter in book-site/docs/module-1/controllers.md"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1.  Complete Phase 1: Setup
2.  Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3.  Complete Phase 3: User Story 1
4.  **STOP and VALIDATE**: Test User Story 1 independently
5.  Deploy/demo if ready

### Incremental Delivery

1.  Complete Setup + Foundational → Foundation ready
2.  Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3.  Add User Story 2 → Test independently → Deploy/Demo
4.  Add User Story 3 → Test independently → Deploy/Demo
5.  Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1.  Team completes Setup + Foundational together
2.  Once Foundational is done:
    -   Developer A: User Story 1 (P1)
    -   Developer B: User Story 2 (P1)
    -   Developer C: User Story 3 (P2)
3.  Stories complete and integrate independently

---

## Notes

-   [P] tasks = different files, no dependencies
-   [Story] label maps task to specific user story for traceability
-   Each user story should be independently completable and testable
-   Commit after each task or logical group
-   Stop at any checkpoint to validate story independently
-   Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
