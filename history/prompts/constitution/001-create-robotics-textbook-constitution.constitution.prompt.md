---
id: 001
title: Create Robotics Textbook Constitution
stage: constitution
date: 2025-12-05
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: system
command: /sp.constitution
labels: ["constitution", "setup", "project-initialization", "robotics", "education"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A (constitution document)
---

## Prompt

Project Name: Physical AI & Humanoid Robotics

Purpose:
Create a short, clean, professional AI-Native textbook for the Physical AI & Humanoid Robotics course using a modern Docusaurus UI.

Scope (4 Modules)

Module 1: ROS 2 – The Robotic Nervous System

	Middleware for robot control

	Nodes, Topics, Services
	Python Agents → ROS via rclpy

	High-level URDF for humanoids

Module 2: Digital Twin – Gazebo & Unity

	Physics simulation and environments

	Gravity, collisions, dynamics

	Unity visualization

	Simulated sensors: LiDAR, Depth, IMU

Module 3: NVIDIA Isaac – The AI-Robot Brain

	Photorealistic Isaac Sim

	Synthetic data generation

	Isaac ROS VSLAM + perception

	Nav2 path planning for humanoids

Module 4: Vision-Language-Action (VLA)

	LLM + Robotics integration

	Whisper Voice-to-Action

	Natural language → ROS 2 action planning

	Capstone: Autonomous humanoid robot (plan → navigate → detect → manipulate)

Core Principles

	Simplicity

	Accuracy

	Minimalism

	Fast builds

	Free-tier friendly architecture

	Student-focused clarity

	Based on official documentation (Docusaurus(https://docusaurus.io/docs), GitHub Pages, Spec-Kit Plus, Claude Code, Panaverse)

	Consistency in formatting and terminology

Key Features

	Docusaurus textbook

	Optional Urdu / personalization features

Constraints

	No heavy GPU usage

	Minimal embeddings

Success Criteria

	Successful Docusaurus build

	Clean UI

	Accurate chatbot

	Smooth GitHub Pages deployment

	Steps easy for beginners

	Validated by Spec-Kit Plus

	Claude Code understands constitution + specs

	Complete book published and readable online

Key Standards

	All instructions testable and reproducible

	Commands validated in real environment

	TypeScript best practices for Docusaurus

	Follows Spec-Kit Plus formats (specs, workflows, drafts, iterations)

	Clear, simple English

	Use headings, bullets, numbered sequences, code blocks

	Standard chapter layout: Introduction → Concepts → Steps → Code  → examples → Checklist

	GitHub Pages steps must be 100% correct

Structure

	Each chapter must include:

		Specification

		Objectives

		Examples

		Steps

		Code

		Final exercise

	Each module must include:

		Inputs

		Outputs

		Architecture

		Code failure modes

		Safety rules

## Response snapshot

Created constitution v1.0.0 for Physical AI & Humanoid Robotics Textbook project.

Key outputs:
- Defined 7 core principles: Simplicity, Accuracy, Minimalism, Free-Tier Friendly Architecture, Student-Focused Clarity, Documentation-Based Development, Consistency
- Established content standards for chapters (6 required elements) and modules (5 required elements)
- Specified technical requirements for Docusaurus implementation and GitHub Pages deployment
- Created governance structure with amendment process and compliance verification
- Added sync impact report documenting version change and template compatibility

All template placeholders replaced with concrete values specific to robotics education context.

## Outcome

- ✅ Impact: Constitution v1.0.0 ratified, establishing foundational governance for Physical AI & Humanoid Robotics textbook project
- 🧪 Tests: N/A (governance document, not executable code)
- 📁 Files: 1 created (.specify/memory/constitution.md)
- 🔁 Next prompts: Create feature specifications for each of the 4 modules, establish Docusaurus project structure, define content templates
- 🧠 Reflection: Constitution successfully captures educational priorities (student accessibility, clarity, accuracy) while maintaining alignment with Spec-Kit Plus methodology. Free-tier constraints and testability requirements will guide all subsequent technical decisions.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Manual review - PASS (all placeholders filled, principles clearly defined, governance structure complete)
- Prompt variant (if applicable): N/A (initial constitution creation)
- Next experiment (smallest change to try): Create first feature specification for Module 1 (ROS 2) to validate that constitution principles translate into actionable spec guidance
