# Quickstart Guide: Physical AI & Humanoid Robotics Textbook

**Feature**: 001-docusaurus-book-layout
**Date**: 2025-12-06

## Prerequisites

Before starting, ensure you have:

- [ ] Node.js 18+ installed (`node --version`)
- [ ] npm or yarn package manager
- [ ] Git installed and configured
- [ ] GitHub account with repository access
- [ ] Text editor (VS Code recommended)

## Quick Setup (5 minutes)

### 1. Clone Repository

```bash
git clone https://github.com/<org>/physical-ai-textbook.git
cd physical-ai-textbook
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Start Development Server

```bash
npm start
```

Visit `http://localhost:3000` to see the site.

### 4. Build for Production

```bash
npm run build
```

### 5. Deploy to GitHub Pages

```bash
npm run deploy
```

---

## Project Structure

```
physical-ai-textbook/
├── docusaurus.config.js     # Main configuration
├── sidebars.js              # Navigation structure
├── src/
│   ├── components/          # React components
│   │   └── ModuleCard.tsx   # Module overview card
│   ├── data/
│   │   └── modules.json     # Module definitions
│   ├── pages/
│   │   └── index.tsx        # Homepage with cards
│   └── css/
│       └── custom.css       # Custom styles
├── docs/
│   ├── module-1/            # ROS 2 chapters
│   ├── module-2/            # Gazebo/Unity chapters
│   ├── module-3/            # Isaac chapters
│   └── module-4/            # VLA chapters
└── static/
    └── img/                 # Images and icons
```

---

## Common Tasks

### Add a New Chapter

1. Create markdown file in appropriate module folder:
   ```bash
   touch docs/module-1/chapter-6-new-topic.md
   ```

2. Add frontmatter:
   ```markdown
   ---
   id: chapter-6
   title: New Topic Title
   sidebar_position: 6
   ---

   # Chapter content here
   ```

3. Update `sidebars.js` if needed.

### Update Module Data

Edit `src/data/modules.json`:
```json
{
  "modules": [
    {
      "moduleNumber": 1,
      "title": "...",
      "chapters": [...]
    }
  ]
}
```

### Add Custom Component

1. Create component in `src/components/`:
   ```tsx
   // src/components/MyComponent.tsx
   export default function MyComponent() {
     return <div>Content</div>;
   }
   ```

2. Import in MDX files:
   ```mdx
   import MyComponent from '@site/src/components/MyComponent';

   <MyComponent />
   ```

---

## Configuration Files

### docusaurus.config.js

Key settings:
```javascript
module.exports = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'From ROS 2 to Vision-Language-Action',
  url: 'https://<org>.github.io',
  baseUrl: '/physical-ai-textbook/',

  // Theme configuration
  themeConfig: {
    navbar: { /* ... */ },
    footer: { /* ... */ },
  },
};
```

### sidebars.js

Navigation structure:
```javascript
module.exports = {
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Module 1: ROS 2',
      items: ['module-1/chapter-1', 'module-1/chapter-2'],
    },
    // More modules...
  ],
};
```

---

## Development Workflow

### 1. Create Feature Branch

```bash
git checkout -b feature/chapter-X-topic
```

### 2. Make Changes

- Edit markdown files in `docs/`
- Update components in `src/`
- Test locally with `npm start`

### 3. Validate Build

```bash
npm run build
```

Ensure no errors before committing.

### 4. Commit and Push

```bash
git add .
git commit -m "Add Chapter X: Topic Name"
git push origin feature/chapter-X-topic
```

### 5. Create Pull Request

Open PR on GitHub for review.

---

## Testing Checklist

Before marking content complete:

- [ ] `npm run build` passes without errors
- [ ] No broken links (check browser console)
- [ ] Code examples tested and working
- [ ] Mobile responsive (test at 320px, 768px, 1024px)
- [ ] Keyboard navigation works
- [ ] All images have alt text

---

## Troubleshooting

### Build Fails

```bash
# Clear cache and rebuild
npm run clear
npm run build
```

### Port Already in Use

```bash
# Use different port
npm start -- --port 3001
```

### Dependency Issues

```bash
# Clean install
rm -rf node_modules package-lock.json
npm install
```

### GitHub Pages 404

Check `docusaurus.config.js`:
- `baseUrl` matches repository name
- `organizationName` and `projectName` are correct

---

## Resources

- [Docusaurus Documentation](https://docusaurus.io/docs)
- [GitHub Pages Guide](https://docs.github.com/en/pages)
- [MDX Documentation](https://mdxjs.com/)
- [React Documentation](https://react.dev/)

---

## Next Steps

After setup:

1. Review `modules.json` to understand module structure
2. Start with Module 1 chapter content
3. Follow the standard chapter template (see constitution)
4. Test all code examples before committing
5. Deploy incrementally after each module completion
