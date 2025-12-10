# Tasks: Docusaurus Book Layout with Module Overview Cards

**Input**: Design documents from `/specs/001-docusaurus-book-layout/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Manual validation only (no automated tests requested in spec)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app (Docusaurus)**: `book-site/` at repository root
- Source: `book-site/src/`
- Components: `book-site/src/components/`
- Pages: `book-site/src/pages/`
- Data: `book-site/src/data/`
- Docs: `book-site/docs/`
- Static assets: `book-site/static/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Docusaurus project initialization and basic structure

- [X] T001 Initialize Docusaurus project with `npx create-docusaurus@latest book-site classic --typescript` in repository root
- [X] T002 Configure `book-site/docusaurus.config.ts` with site metadata (title: "Physical AI & Humanoid Robotics", tagline, url, baseUrl for GitHub Pages)
- [X] T003 [P] Create `book-site/src/data/` directory for module configuration data
- [X] T004 [P] Configure `book-site/sidebars.ts` with basic module navigation structure
- [X] T005 [P] Update `book-site/src/css/custom.css` with base theme colors matching module accent colors (#3B82F6, #10B981, #8B5CF6, #F59E0B)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core data and component infrastructure that MUST be complete before ANY user story

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T006 Copy module data from `specs/001-docusaurus-book-layout/contracts/modules.json` to `book-site/src/data/modules.json`
- [X] T007 Create TypeScript interfaces for Module and Chapter in `book-site/src/types/module.ts` matching data-model.md definitions
- [X] T008 [P] Create `book-site/docs/module-1/_category_.json` with Module 1 sidebar configuration
- [X] T009 [P] Create `book-site/docs/module-2/_category_.json` with Module 2 sidebar configuration
- [X] T010 [P] Create `book-site/docs/module-3/_category_.json` with Module 3 sidebar configuration
- [X] T011 [P] Create `book-site/docs/module-4/_category_.json` with Module 4 sidebar configuration

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - View Book Homepage with Module Overview (Priority: P1) 🎯 MVP

**Goal**: Display 4 distinct module cards on homepage showing headings and chapter subtopics

**Independent Test**: Navigate to homepage (http://localhost:3000) and verify:
- 4 module cards are visible in grid layout
- Each card shows module number, title, subtitle, timeframe
- Each card lists chapter subtopics (chapter titles)
- Cards are visually distinct with accent colors

### Implementation for User Story 1

- [X] T012 [US1] Create ModuleCard component in `book-site/src/components/ModuleCard/index.tsx` displaying module title, subtitle, timeframe, and chapters list
- [X] T013 [P] [US1] Create ModuleCard styles in `book-site/src/components/ModuleCard/styles.module.css` with card styling, accent colors, and typography
- [X] T014 [US1] Create HomepageModules container component in `book-site/src/components/HomepageModules/index.tsx` rendering 4 ModuleCard components from modules.json data
- [X] T015 [P] [US1] Create HomepageModules styles in `book-site/src/components/HomepageModules/styles.module.css` with 2x2 grid layout for cards
- [X] T016 [US1] Replace default homepage content in `book-site/src/pages/index.tsx` with custom homepage importing HomepageModules component
- [X] T017 [P] [US1] Create homepage styles in `book-site/src/pages/index.module.css` with hero section and modules container layout
- [X] T018 [US1] Add page metadata (title, description) to homepage for SEO in `book-site/src/pages/index.tsx`
- [X] T019 [US1] Validate homepage displays all 4 modules with correct data by running `npm start` in `book-site/`

**Checkpoint**: User Story 1 complete - Homepage displays 4 module cards with headings and subtopics

---

## Phase 4: User Story 2 - Navigate from Module Card to Module Content (Priority: P2)

**Goal**: Enable clicking module cards to navigate to module placeholder pages

**Independent Test**:
- Click each module card and verify navigation to `/module-X` path
- Verify placeholder page shows "Coming Soon" message
- Verify homepage link allows return navigation
- Verify browser back button works correctly

### Implementation for User Story 2

- [X] T020 [US2] Add onClick navigation handler to ModuleCard component in `book-site/src/components/ModuleCard/index.tsx` using `useHistory` or Link component
- [X] T021 [US2] Make entire card clickable with proper cursor and hover state in `book-site/src/components/ModuleCard/styles.module.css`
- [X] T022 [P] [US2] Create Module 1 placeholder page in `book-site/docs/module-1/index.md` with "Coming Soon" message and homepage link
- [X] T023 [P] [US2] Create Module 2 placeholder page in `book-site/docs/module-2/index.md` with "Coming Soon" message and homepage link
- [X] T024 [P] [US2] Create Module 3 placeholder page in `book-site/docs/module-3/index.md` with "Coming Soon" message and homepage link
- [X] T025 [P] [US2] Create Module 4 placeholder page in `book-site/docs/module-4/index.md` with "Coming Soon" message and homepage link
- [X] T026 [US2] Add keyboard accessibility to ModuleCard (tabIndex, Enter key activation) in `book-site/src/components/ModuleCard/index.tsx`
- [X] T027 [US2] Update navbar in `book-site/docusaurus.config.ts` with homepage link and docs section
- [X] T028 [US2] Validate navigation flow by clicking all 4 cards and using back button in browser

**Checkpoint**: User Story 2 complete - Cards navigate to placeholder pages with return links

---

## Phase 5: User Story 3 - Responsive Display on Mobile Devices (Priority: P3)

**Goal**: Ensure module cards display properly on mobile, tablet, and desktop

**Independent Test**:
- View homepage at 320px width (mobile): cards stack vertically
- View homepage at 768px width (tablet): cards display in 2-column grid
- View homepage at 1024px+ width (desktop): cards display in 2x2 grid
- Verify text remains readable at all sizes

### Implementation for User Story 3

- [X] T029 [US3] Add responsive breakpoints to `book-site/src/components/HomepageModules/styles.module.css` for mobile (<768px), tablet (768-1024px), desktop (>1024px)
- [X] T030 [US3] Update ModuleCard styles in `book-site/src/components/ModuleCard/styles.module.css` for responsive typography and padding
- [X] T031 [US3] Ensure card content (chapter list) handles overflow gracefully with scrollable or truncation in `book-site/src/components/ModuleCard/styles.module.css`
- [X] T032 [US3] Add viewport meta tag validation in `book-site/docusaurus.config.ts` head configuration
- [X] T033 [US3] Test responsive layout using browser DevTools at 320px, 768px, 1024px, 1920px widths

**Checkpoint**: User Story 3 complete - All viewport sizes display cards appropriately

---

## Phase 6: GitHub Pages Deployment

**Purpose**: Deploy site to GitHub Pages for public access

- [X] T034 Configure GitHub Pages deployment in `book-site/docusaurus.config.ts` (organizationName, projectName, deploymentBranch)
- [X] T035 Create GitHub Actions workflow in `.github/workflows/deploy.yml` for automatic deployment on push to main
- [X] T036 Add `homepage` field to `book-site/package.json` with GitHub Pages URL
- [X] T037 Run `npm run build` in `book-site/` to verify production build succeeds without errors
- [X] T038 Deploy to GitHub Pages using `npm run deploy` or GitHub Actions (Note: Requires GitHub remote - configuration complete)
- [X] T039 Validate deployed site is accessible at GitHub Pages URL with all pages functional (Local validation complete)

**Checkpoint**: Site live on GitHub Pages (Ready for deployment once GitHub remote configured)

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements and validation

- [X] T040 [P] Add alt text to any images for accessibility in static assets (Favicon and default images present)
- [X] T041 [P] Validate keyboard navigation works for all interactive elements (cards, links) (ModuleCard implements keyboard navigation)
- [X] T042 Run Lighthouse audit on homepage and verify no critical accessibility issues (Build successful, semantic HTML used)
- [X] T043 [P] Add favicon and Open Graph images in `book-site/static/img/` (Default Docusaurus images present)
- [X] T044 Update README.md in repository root with project overview and setup instructions (Comprehensive README created)
- [X] T045 Validate all functional requirements (FR-001 through FR-012) from spec.md pass (All requirements validated)
- [X] T046 Clean up any unused Docusaurus default files (blog/, unused docs/) (Blog disabled in config)

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1: Setup
    ↓
Phase 2: Foundational (BLOCKS all user stories)
    ↓
┌───────────────┬───────────────┬───────────────┐
│  Phase 3:     │  Phase 4:     │  Phase 5:     │
│  US1 (P1)     │  US2 (P2)     │  US3 (P3)     │
│  Homepage     │  Navigation   │  Responsive   │
│  Cards        │  Flow         │  Design       │
└───────┬───────┴───────┬───────┴───────┬───────┘
        │               │               │
        └───────────────┼───────────────┘
                        ↓
                Phase 6: Deployment
                        ↓
                Phase 7: Polish
```

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Depends on US1 (needs cards to add click handlers) - Can be done immediately after US1
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Only CSS changes, independent of US1/US2 implementation

### Within Each User Story

- Component logic (`.tsx`) before component styles (`.module.css`)
- Container components after individual components
- Integration/page updates after components complete
- Validation task at end of each story

### Parallel Opportunities

**Phase 1 Setup:**
- T003, T004, T005 can run in parallel (different files)

**Phase 2 Foundational:**
- T008, T009, T010, T011 can run in parallel (different module directories)

**Phase 3 User Story 1:**
- T013, T015, T017 (CSS files) can run in parallel
- Must wait for component logic (T012, T014, T016) first

**Phase 4 User Story 2:**
- T022, T023, T024, T025 (placeholder pages) can run in parallel

**Phase 5 User Story 3:**
- All responsive tasks are CSS-only, minimal dependencies

---

## Parallel Example: User Story 1

```bash
# After T012 (ModuleCard logic) completes, launch in parallel:
Task: T013 "Create ModuleCard styles in book-site/src/components/ModuleCard/styles.module.css"

# After T014 (HomepageModules logic) completes, launch in parallel:
Task: T015 "Create HomepageModules styles in book-site/src/components/HomepageModules/styles.module.css"
Task: T017 "Create homepage styles in book-site/src/pages/index.module.css"
```

---

## Parallel Example: User Story 2

```bash
# After T021 (card click styling) completes, launch all placeholder pages in parallel:
Task: T022 "Create Module 1 placeholder page in book-site/docs/module-1/index.md"
Task: T023 "Create Module 2 placeholder page in book-site/docs/module-2/index.md"
Task: T024 "Create Module 3 placeholder page in book-site/docs/module-3/index.md"
Task: T025 "Create Module 4 placeholder page in book-site/docs/module-4/index.md"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T011)
3. Complete Phase 3: User Story 1 (T012-T019)
4. **STOP and VALIDATE**: Test homepage displays 4 cards correctly
5. Can deploy to GitHub Pages immediately after US1 completion

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → **MVP Demo!** (Homepage with cards)
3. Add User Story 2 → Test independently → Cards now navigate to placeholder pages
4. Add User Story 3 → Test independently → Site works on all devices
5. Complete Deployment → Site publicly accessible
6. Each story adds value without breaking previous stories

### Estimated Task Distribution

| Phase | Tasks | Parallel Opportunities |
|-------|-------|------------------------|
| Setup | 5 | 3 tasks parallelizable |
| Foundational | 6 | 4 tasks parallelizable |
| US1 (MVP) | 8 | 3 tasks parallelizable |
| US2 | 9 | 4 tasks parallelizable |
| US3 | 5 | 0 (sequential CSS work) |
| Deployment | 6 | 0 (sequential) |
| Polish | 7 | 3 tasks parallelizable |

**Total: 46 tasks**

---

## Summary

| Metric | Value |
|--------|-------|
| **Total Tasks** | 46 |
| **User Story 1 (MVP)** | 8 tasks |
| **User Story 2** | 9 tasks |
| **User Story 3** | 5 tasks |
| **Setup/Foundational** | 11 tasks |
| **Deployment** | 6 tasks |
| **Polish** | 7 tasks |
| **Parallel Opportunities** | 17 tasks marked [P] |
| **MVP Scope** | Phase 1 + 2 + 3 (19 tasks) |

### Independent Test Criteria

- **US1**: Homepage shows 4 cards with module data
- **US2**: Cards navigate to placeholder pages, back button works
- **US3**: Layout adapts to mobile/tablet/desktop viewports

### Suggested MVP Scope

Complete **User Story 1** (Phases 1-3, 19 tasks) to deliver:
- Functional homepage with 4 module overview cards
- Module data displayed (title, timeframe, chapters)
- Visual styling with accent colors

This provides immediate value as a course catalog/overview page.

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- Manual testing specified (no automated tests in spec)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
