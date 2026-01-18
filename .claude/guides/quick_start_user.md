# Quick Start Guide - Hub Users

## Launching the Application

### From Development
```bash
cd C:\Dev\trajanus-command-center
npm run dev
```
Opens at: `http://localhost:1420`

### From Built App
Double-click the Trajanus Enterprise Hub executable.

---

## Main Hub

The main hub shows 5 platform cards:
- **QCM Toolkit** - Quality Control Management
- **PM Toolkit** - Project Management
- **Developer Toolkit** - Development Tools
- **Traffic Studies** - Traffic Engineering
- **Healthcare Platform** - Healthcare Management

Click any card to open that workspace.

---

## QCM Toolkit

### Purpose
Manage submittals for USACE Design-Build contracts.

### Categories
1. Submittal Management
2. Testing & Inspection
3. Documentation
4. Acceptance

### Workflow
1. Select submittal type
2. Fill required fields
3. Generate documentation
4. Track status

---

## PM Toolkit

### Purpose
Project management tools and dashboards.

### Features
- Schedule tracking (CPM)
- Cost analysis
- Resource management
- Progress reporting

---

## Developer Toolkit

### Purpose
Development tools, automation, and AI agents.

### Sections
- **External Apps** - Launch VS Code, Terminal, etc.
- **Trajanus Scripts** - Run automation scripts
- **Agents** - AI agents for research and review
- **Progress Tracker** - Visual task tracking
- **Claude.ai** - Embedded Claude interface

### Using Scripts
1. Navigate to Trajanus Scripts section
2. Click any script button
3. View output in terminal section

### Using Agents
1. Navigate to Agents section
2. Click "Activate" to load agent skill
3. Or "Deploy" to assign specific task

---

## Traffic Studies Toolkit

### Purpose
USACE traffic study requirements and TIA generation.

### 10-Step Workflow
1. Project Setup
2. Scope Definition
3. Data Collection
4. Existing Conditions
5. Trip Generation
6. Distribution
7. Assignment
8. Analysis
9. Mitigation
10. Documentation

---

## Navigation

### Return to Hub
Click "← Hub" button in any toolkit.

### Keyboard Shortcuts
- `F5` - Refresh current page
- `F12` - Open DevTools (debugging)

---

## Troubleshooting

### Page Not Loading
1. Check if app is running (`npm run dev`)
2. Verify URL is correct
3. Check console for errors (F12)

### Script Not Running
1. Ensure Tauri backend is active
2. Check script exists in 05-Scripts folder
3. View terminal for error messages

### Agent Not Responding
1. Check network connection (for Anthropic API)
2. Verify API key is configured
3. Check terminal for error details

---

## Getting Help

- **Documentation**: See README.md
- **Technical Issues**: Check CHANGELOG.md for known issues
- **Feature Requests**: Contact Bill King

---

**Last Updated:** 2026-01-17
