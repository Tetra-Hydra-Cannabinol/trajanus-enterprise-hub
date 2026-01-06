# Skill: File Editing & Management

## Name
file-editing

## Description
Edit, create, and manage files across the Trajanus project structure. Handles markdown, code, configuration, and documentation files with proper formatting and version awareness.

## When to Use
- Creating new documents, scripts, or configurations
- Editing existing files
- Managing project structure
- Converting between formats

## Project Paths

### Primary Locations
| Location | Path | Purpose |
|----------|------|---------|
| Source Code | `C:\Dev\trajanus-command-center\` | Tauri app development |
| Runtime | `G:\My Drive\00 - Trajanus USA\00-Command-Center\` | Production files |
| Scripts | `...\00-Command-Center\05-Scripts\` | Python, PS1, JS scripts |
| Learning | `...\00-Command-Center\07-Learning\` | Training materials |
| Skills | `...\00-Command-Center\Skills\` | Knowmad Agent skills |
| Session Archive | `...\00-Command-Center\Session_Archive\` | EOS files |

### File Types by Location
- **05-Scripts/**: `.py`, `.ps1`, `.js`, `.bat` only
- **Skills/**: `.md` Knowmad skill files
- **07-Learning/**: Training transcripts, tutorials
- **Session_Archive/**: Session summaries, handoffs

## Procedure

### Before Editing
1. **Always read first** - Use Read tool before Edit
2. **Verify path exists** - Check parent directory
3. **Note current state** - Understand what you're changing

### File Creation Rules
- NEVER create documentation unless explicitly requested
- PREFER editing existing files over creating new ones
- Use consistent naming: `YYYY-MM-DD_Description.md` for dated files
- No emojis unless user requests them

### Markdown Formatting
```markdown
# Title (H1 - one per file)

## Section (H2)

### Subsection (H3)

**Bold** for emphasis
`code` for inline code
```code blocks``` for multi-line

| Tables | For | Structured Data |
|--------|-----|-----------------|
```

### Code File Standards
- Include header comment with purpose
- Use consistent indentation (4 spaces for Python, 2 for JS)
- Add error handling for production code

## Color Theme (for UI files)
```
Gold: #d4a574
Charcoal: #2d2d2d
Dark BG: #1a1a1a
Text: #e0e0e0
```

## Git Awareness
- Check `git status` before major changes
- Never commit unless explicitly asked
- Use descriptive commit messages when asked

## Error Prevention
- Quote paths with spaces: `"path with spaces"`
- Use forward slashes in Python: `Path(r"G:/My Drive/...")`
- Escape backslashes in strings: `\\`
