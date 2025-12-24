# LARGE FILE EDITING PROTOCOL - RESEARCH FINDINGS
**Date:** 2025-12-15
**Source:** Anthropic official documentation + Claude Code best practices

---

## THE ANSWER: STR_REPLACE TOOL WITH VIEW_RANGE

**This is Anthropic's official method, built into Claude and Claude Code.**

---

## HOW IT ACTUALLY WORKS:

### STEP 1: View Only What You Need

```python
# Instead of loading entire 7000-line file:
view(path="index.html")  # BAD - loads entire file

# Do this:
view(path="index.html", view_range=[1800, 1850])  # GOOD - loads only 50 lines
```

**The `view_range` parameter:**
- Takes [start_line, end_line]
- Line numbers are 1-indexed
- Use -1 for end_line to read to end of file
- **This prevents loading entire large files**

### STEP 2: Make Surgical Edit with str_replace

```python
str_replace(
    path="index.html",
    old_str="z-index: 3000;",
    new_str="z-index: 10000;"
)
```

**Requirements:**
- Exact string match required
- Must match exactly ONE occurrence
- If multiple matches → error
- If no match → error "String to replace not found in file"

### STEP 3: Other Commands Available

```python
# Insert at specific line
insert(
    path="index.html",
    line_number=1850,
    new_text="  display: flex;"
)

# Create new file
create(
    path="new_file.js",
    file_text="console.log('hello');"
)
```

---

## THE PROPER WORKFLOW:

### For index.html (7000+ lines):

**BAD approach (what we were doing):**
1. Open entire file in editor
2. Edit everything
3. Save whole file
4. Risk breaking other parts

**GOOD approach (official method):**
1. `view` with `view_range` to see only target section
   ```
   view(path="index.html", view_range=[1800, 1820])
   ```
2. Identify exact string to replace
3. Use `str_replace` with exact match
   ```
   str_replace(
       path="index.html",
       old_str="    z-index: 3000;",  # EXACT whitespace matters!
       new_str="    z-index: 10000;"
   )
   ```
4. File updated, rest unchanged

---

## WHY THIS IS BETTER:

**Advantages:**
- Never loads entire large file into memory
- Only touches the specific section
- Rest of file guaranteed unchanged
- Much faster for large files
- Reduces token usage
- Reduces errors

**Real-world proof:**
- Claude Code successfully edits 18,000-line React files
- Other tools (Cursor, etc.) fail on large files
- str_replace is the secret sauce

---

## COMMON ERRORS & FIXES:

###Error: "String to replace not found in file"

**Causes:**
- Whitespace doesn't match exactly
- String appears 0 times (typo)
- String appears multiple times

**Fix:**
1. Use `view` with `view_range` to see exact text
2. Copy exact string including whitespace
3. Verify only ONE occurrence exists

### Error: Multiple matches found

**Causes:**
- String is too generic
- Appears in multiple places

**Fix:**
- Include more context in search string
- Make string more specific
- Use larger unique block

---

## CLAUDE CODE SPECIFIC FEATURES:

**Commands Claude Code uses:**
- `/clear` - Reset context between tasks
- Extended thinking with "think hard"
- CLAUDE.md for project-specific instructions
- Custom hooks for automation

**For large files:**
- CC automatically uses str_replace methodology
- Can handle massive files (tested up to 18,000 lines)
- Uses strategic chunking
- Explore → Plan → Code → Commit workflow

---

## COMPLIANCE OFFICER CHECKPOINTS:

**CO must verify:**

1. ✓ CC used `view` command with `view_range` parameter
2. ✓ Only loaded necessary section (not entire file)
3. ✓ Used `str_replace` with exact string match
4. ✓ Created backup before edit
5. ✓ Tested after edit
6. ✓ Did NOT rewrite entire file

**RED FLAGS (reject immediately):**
- ❌ "Read entire file" in logs
- ❌ Full file rewrite
- ❌ No view_range parameter used
- ❌ Multiple str_replace attempts on same file (sign of problems)

---

## INTEGRATION WITH TRAJANUS WORKFLOW:

**For our z-index fix:**

```bash
# CORRECT METHOD:
1. view(path="index.html", view_range=[1800, 1820])
2. Identify: line 1807 has "z-index: 3000;"
3. str_replace(
      path="index.html",
      old_str="    z-index: 3000;",
      new_str="    z-index: 10000;"
   )
4. Verify change successful
5. Test app launch
```

**NOT acceptable:**
- Opening entire index.html
- Editing CSS section then saving
- Any method that touches more than the target line

---

## TOOLS REQUIRED:

**Claude Code has these built-in:**
- `view` command
- `str_replace` command
- `insert` command
- `create` command
- `bash` command (for testing)

**No additional tools needed** - this is native to Claude/CC.

---

## MAX_CHARACTERS PARAMETER:

**Optional optimization:**
```python
# Truncate view results to save tokens
view(path="large_file.html", max_characters=10000)
```

**When to use:**
- Very large files
- Just need to see structure
- Want to reduce token usage

---

## BACKUP STRATEGY:

```python
def backup_file(file_path):
    """Create backup before any edit"""
    backup_path = f"{file_path}.backup.{timestamp}"
    shutil.copy(file_path, backup_path)
```

**Compliance requirement:**
- ALWAYS backup before str_replace
- Timestamped backups
- Keep for rollback capability

---

## SOURCES:

1. https://docs.claude.com/en/docs/agents-and-tools/tool-use/text-editor-tool
2. https://www.anthropic.com/engineering/claude-code-best-practices  
3. https://www.builder.io/blog/claude-code (18,000-line file proof)
4. https://medium.com/@rquintino/replace-is-all-you-need
5. https://simonwillison.net/2025/Mar/13/anthropic-api-text-editor-tool/

---

## CONCLUSION:

**The industry standard for editing large files with Claude:**

1. **View only what you need** (view_range parameter)
2. **Edit only what you need** (str_replace with exact match)
3. **Never load entire large files**
4. **This is built into Claude - it's THE method**

**Compliance Officer must enforce this method.**

**No exceptions. No full-file rewrites. Ever.**
