# Quickstart Guide: Physical AI & Humanoid Robotics Textbook Development

**Date**: 2025-12-06

This guide provides instructions for setting up your development environment and contributing to the Physical AI & Humanoid Robotics Textbook.

## 1. Prerequisites

Before you begin, ensure you have the following installed:

*   **Git**: For version control.
*   **Node.js (LTS)**: Required for Docusaurus.
*   **Yarn**: Package manager for Docusaurus (recommended over npm).
*   **Python 3.10+**: For ROS 2 code examples and scripting.
*   **ROS 2 Humble (Ubuntu 22.04 LTS)**: For robotics development and examples.
*   **Docker (Optional but Recommended)**: For containerized development environments.

## 2. Environment Setup

1.  **Clone the Repository**:
    ```bash
    git clone <repository-url>
    cd book-writing-hackathon
    ```

2.  **Install Docusaurus Dependencies**:
    Navigate to the `book-site` directory and install dependencies:
    ```bash
    cd book-site
    yarn install
    ```

3.  **Install ROS 2 Dependencies**:
    Follow the official ROS 2 Humble installation guide for Ubuntu 22.04 if you haven't already.
    Ensure your ROS 2 environment is sourced:
    ```bash
    source /opt/ros/humble/setup.bash
    ```

## 3. Running the Development Server

To start the Docusaurus development server and preview your changes:

```bash
cd book-site
yarn start
```

This will open the site in your browser at `http://localhost:3000` (or another available port).

## 4. Building the Static Site

To build the production-ready static site:

```bash
cd book-site
yarn build
```

The generated static files will be placed in the `book-site/build/` directory.

## 5. Adding New Content

*   **Modules**: Create new directories under `book-site/docs/` (e.g., `book-site/docs/module-X/`).
*   **Chapters**: Create Markdown (`.md`) files within module directories (e.g., `book-site/docs/module-X/architecture.md`, `book-site/docs/module-X/communication.md`, etc.).
*   **Sidebar**: Update `book-site/sidebars.ts` to include new modules and chapters with specific names: "Architecture", "Communication", "Packages", "Launch", "URDF", "Controllers".

## 6. Deployment

The site is configured for deployment to GitHub Pages. Ensure your repository settings and `docusaurus.config.ts` are correctly configured. The deployment workflow from `001-docusaurus-book-layout` feature should be used.

## 7. Agent Context Update (for AI Assistants)

For AI assistants like Claude, ensure the internal knowledge base is updated with the following technologies and their relevance to robotics and textbook content generation:

*   Gazebo
*   Unity
*   NVIDIA Isaac Sim
*   Isaac ROS
*   Whisper
*   LLM (for task planning in robotics)

This helps the AI assistant provide accurate guidance and generate relevant content.