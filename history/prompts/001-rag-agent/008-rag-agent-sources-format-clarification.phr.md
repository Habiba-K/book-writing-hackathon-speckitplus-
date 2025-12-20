---
id: 008
title: RAG Agent Sources Format Clarification
stage: spec
date: 2025-12-19
surface: CLI
model: Claude Sonnet 4.5
feature: 001-rag-agent
branch: 001-rag-agent
user: habiba
command: /sp.clarify
labels: [clarification, output-format, sources]
links:
  spec: D:\New folder\gemini CLI LECTURES\book-writing-hackathon-speckitplus-\specs\001-rag-agent\spec.md
  ticket:
  adr:
  pr:
files:
  - path: D:\New folder\gemini CLI LECTURES\book-writing-hackathon-speckitplus-\specs\001-rag-agent\spec.md
    action: update
    summary: Added clarifications for single clickable source format and out-of-scope response
tests:

---
## Prompt

ye output me itnay saray sources show kar raha hai bas aik source show karay jo clickable ho "Source: Document 1: Isaac ROS Perception | Physical AI & Humanoid Robotics (https://book-writing-hackathon-speckitplus.vercel.app/module-3/isaac-ros-perception)
Sources:
Isaac ROS Perception | Physical AI & Humanoid Robotics
Capstone Integration | Physical AI & Humanoid Robotics
Capstone Integration | Physical AI & Humanoid Robotics" and book kay ilawa agar kuch pochon to wo output me mujhay kahay kay "sorry this content is not related to this book"

## Response snapshot

Successfully updated the RAG agent specification with clarifications about output format:

1. Added clarification about single clickable source format: "Single Clickable Source Format - Show only one primary source that is clickable in the format 'Source: Document X: [Title] ([URL])' as the main reference"

2. Added clarification about out-of-scope responses: "Out-of-Book Content Response - When users ask questions about content not related to the book, respond professionally with 'sorry this content is not related to this book'"

3. Added corresponding functional requirements:
   - FR-013: System MUST display only one primary clickable source in the main response in the format "Source: Document X: [Title] ([URL])"
   - FR-014: System MUST respond with "sorry this content is not related to this book" when asked about content outside the book scope

The specification now clearly defines how sources should be displayed (single clickable source) and how to handle out-of-scope queries.

## Outcome

- ✅ Impact: Clarified output format requirements for RAG agent responses
- 🧪 Tests:
- 📁 Files: specs/001-rag-agent/spec.md updated with new clarifications
- 🔁 Next prompts: /sp.plan to proceed with implementation planning
- 🧠 Reflection: Successfully resolved ambiguity about source display and out-of-scope responses

## Evaluation notes (flywheel)

- Failure modes observed:
- Graders run and results (PASS/FAIL):
- Prompt variant (if applicable):
- Next experiment (smallest change to try):