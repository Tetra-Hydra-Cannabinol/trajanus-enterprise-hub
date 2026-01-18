# Tool Addition Template

## Tool Information
- **Tool Name:** [Name]
- **Type:** [Python Script/External App/Web Tool/Tauri Command]
- **Workspace(s):** [Where it will appear]
- **Button Type:** [ext-btn/script-btn]

---

## Tool Specification

### Purpose
[What does this tool do? What problem does it solve?]

### Input
- [Input 1]: [Description]
- [Input 2]: [Description]

### Output
- [Output format and location]

### Dependencies
- [Required software/libraries]
- [Required API keys]
- [Required file paths]

---

## Implementation Checklist

### Pre-Implementation
- [ ] Verify tool doesn't already exist in 05-Scripts
- [ ] Check for similar functionality to reuse
- [ ] Confirm dependencies available

### Script Creation (if Python)
Location: `G:\My Drive\00 - Trajanus USA\00-Command-Center\05-Scripts\`

```python
#!/usr/bin/env python3
"""
Tool Name: [NAME]
Purpose: [DESCRIPTION]
Author: Trajanus Systems
Date: [DATE]
"""

import sys
import os

def main():
    # Tool logic here
    pass

if __name__ == "__main__":
    main()
```

### UI Integration

#### Button HTML
```html
<!-- For script-btn (160x50) -->
<button class="script-btn" data-script="tool_name.py">
    <img src="assets/ai-generated-7986803_1280.jpg" class="script-btn-icon" alt="">
    Tool Name
</button>

<!-- For ext-btn (120x44) -->
<button class="ext-btn" data-launch="toolkey">
    <svg class="ext-btn-icon">...</svg>
    Tool Name
</button>
```

#### JavaScript Registration
```javascript
// For Scripts object
Scripts.scripts['tool-name'] = {
    name: 'Tool Name',
    file: 'tool_name.py'
};

// For Apps object
Apps.commands['toolkey'] = 'path/to/tool';
Apps.webUrls['toolkey'] = 'https://fallback.url';
```

#### Event Binding
```javascript
// In DOMContentLoaded
document.querySelectorAll('[data-script]').forEach(el => {
    el.addEventListener('click', () => Scripts.run(el.dataset.script));
});
```

### Tauri Command (if needed)
```rust
// In lib.rs
#[tauri::command]
fn tool_command(param: String) -> Result<String, String> {
    // Implementation
}
```

---

## File Locations

### Script
```
G:\My Drive\00 - Trajanus USA\00-Command-Center\05-Scripts\tool_name.py
```

### UI Integration
```
src/toolkits/[workspace].html  (button + JS)
```

### Documentation
```
[workspace]/.claude.md  (update with new tool)
```

---

## Acceptance Criteria

### Tool Functionality
```
[ ] Script executes without errors
[ ] Input validation works
[ ] Output is correct format
[ ] Error handling implemented
```

### UI Integration
```
[ ] Button displays correctly
[ ] Button follows style guide (size, colors, glow)
[ ] Click triggers tool execution
[ ] Terminal shows execution status
```

### Tauri Integration
```
[ ] invoke() call works
[ ] Browser fallback shows appropriate message
[ ] Results display in UI
```

### Documentation
```
[ ] Tool documented in workspace .claude.md
[ ] Script has docstring/comments
[ ] Added to 05-Scripts if new Python tool
```

---

## Testing

### Manual Tests
- [ ] Click button - tool launches
- [ ] Valid input - correct output
- [ ] Invalid input - graceful error
- [ ] Cancel/interrupt - handled

### Browser Mode
- [ ] Appropriate fallback message
- [ ] No JavaScript errors

---

## Rollback Plan

If tool causes issues:
1. Remove button from HTML
2. Remove JS registration
3. Keep script (don't delete, just disconnect)
4. Document issue in CHANGELOG.md

---

## Notes
[Design decisions, alternatives considered, known limitations]
