# Content Structure Contract: Docusaurus Multi-Module Textbook

**Date**: 2025-12-06

## 1. File System Structure

All module and chapter content MUST adhere to the following file system structure within the `book-site/docs/` directory:

```
book-site/
├── docs/
│   ├── module-1/
│   │   ├── _category_.json   # Docusaurus category metadata for Module 1
│   │   ├── index.md         # Module 1 overview page
│   │   ├── chapter-1.md     # Chapter 1 content
│   │   ├── chapter-2.md     # Chapter 2 content
│   │   └── ...              # Additional chapters for Module 1
│   ├── module-2/
│   │   ├── _category_.json   # Docusaurus category metadata for Module 2
│   │   ├── index.md         # Module 2 overview page
│   │   ├── chapter-6.md     # Chapter 6 content (e.g., Gazebo Setup)
│   │   └── ...              # Additional chapters for Module 2
│   ├── module-3/
│   │   ├── _category_.json   # Docusaurus category metadata for Module 3
│   │   ├── index.md         # Module 3 overview page
│   │   ├── chapter-12.md    # Chapter 12 content (e.g., Isaac Sim Introduction)
│   │   └── ...              # Additional chapters for Module 3
│   └── module-4/
│       ├── _category_.json   # Docusaurus category metadata for Module 4
│       ├── index.md         # Module 4 overview page
│       ├── chapter-17.md    # Chapter 17 content (e.g., Whisper for Voice Commands)
│       └── ...              # Additional chapters for Module 4
└── sidebars.ts              # Docusaurus sidebar configuration file
```

### Requirements:

*   Each module (`module-X/`) MUST contain an `_category_.json` file for sidebar metadata.
*   Each module (`module-X/`) MUST contain an `index.md` file serving as the module's overview page.
*   Each chapter MUST be a separate Markdown (`.md`) file named predictably (e.g., `chapter-X.md`).
*   All Markdown files MUST adhere to the [GitHub Flavored Markdown (GFM)](https://github.github.com/gfm/) specification.

## 2. Docusaurus Sidebar Configuration (`sidebars.ts`)

The `sidebars.ts` file MUST be updated to reflect the multi-module structure, enabling nested navigation for all chapters within their respective modules.

### Example Structure (Conceptual):

```typescript
module.exports = {
  mainSidebar: [
    {
      type: 'category',
      label: 'Module 1: ROS 2 Fundamentals',
      link: { type: 'doc', id: 'module-1/index' },
      items: [
        'module-1/chapter-1',
        'module-1/chapter-2',
        // ... other Module 1 chapters
      ],
    },
    {
      type: 'category',
      label: 'Module 2: Digital Twin (Gazebo & Unity)',
      link: { type: 'doc', id: 'module-2/index' },
      items: [
        'module-2/chapter-6',
        'module-2/chapter-7',
        // ... other Module 2 chapters
      ],
    },
    // ... similar entries for Module 3 and Module 4
  ],
};
```

### Requirements:

*   Each module MUST be represented as a `type: 'category'` entry.
*   Each category MUST have a `label` corresponding to the module title.
*   Each category MUST have a `link` pointing to its `index.md` overview page.
*   The `items` array within each category MUST list all chapters belonging to that module, using their file paths (without `.md` extension).
*   The sidebar MUST be consistent with the file system structure.

## 3. Inter-Chapter and Inter-Module Navigation

*   **Previous/Next Links**: Docusaurus's default previous/next navigation MUST function correctly between chapters within a module and (potentially) between modules.
*   **Module Overview Link**: Each chapter MUST provide a clear way to return to its module's overview page.
*   **Homepage Link**: A clear path back to the textbook's homepage MUST be maintained from any page.
