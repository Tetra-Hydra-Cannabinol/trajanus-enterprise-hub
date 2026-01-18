# Troubleshooting Guide

## Common Issues & Solutions

---

## Build & Launch Issues

### App Won't Launch

**Symptoms:** `npm run dev` fails or hangs

**Solutions:**
1. Verify correct directory: `C:\Dev\trajanus-command-center`
2. Check Node.js installed: `node --version` (need 18+)
3. Reinstall dependencies:
   ```bash
   rm -rf node_modules
   npm install
   ```
4. Check Tauri CLI: `cargo tauri --version`

---

### Electron Binary Corrupted (Legacy)

**Symptoms:** Stub files in node_modules/electron/dist/

**Solution:**
```bash
rm -rf node_modules
npm install
```

---

### Port Already in Use

**Symptoms:** "Port 1420 is already in use"

**Solutions:**
1. Kill existing process:
   ```bash
   # Windows
   netstat -ano | findstr :1420
   taskkill /PID <PID> /F
   ```
2. Change port in tauri.conf.json

---

## UI Issues

### Layout Broken

**Symptoms:** Elements misaligned, overlapping

**Check:**
1. CSS `flex-wrap` settings
2. Container `overflow` properties
3. `min-width` constraints
4. Console for CSS errors

**Quick Fix:**
```css
/* Ensure flex containers wrap properly */
.container {
    flex-wrap: wrap;
    min-width: 0; /* Allow shrinking */
}
```

---

### Colors Wrong

**Symptoms:** Gold appears instead of blue, wrong colors

**Expected Colors:**
```css
Silver: #C0C0C0
Black: #1a1a1a
Blue: #00AAFF
```

**Check:**
1. CSS variable definitions in `:root`
2. Inline styles overriding
3. Class specificity issues

---

### Buttons Not Styled

**Symptoms:** Buttons missing 3D effect, wrong size

**Expected Sizes:**
- ext-btn: 120×44px
- script-btn: 160×50px
- nav-btn: 140×44px

**Check:**
1. Button class names correct
2. CSS loaded (not 404)
3. main.css imported properly

---

## JavaScript Issues

### Function Not Defined

**Symptoms:** "X is not defined" in console

**Solutions:**
1. Check script order (definition before use)
2. Verify CSP-compliant event binding
3. Check for typos in function names

---

### Event Listeners Not Working

**Symptoms:** Clicks don't trigger actions

**Check CSP Compliance:**
```javascript
// WRONG (inline handler)
<button onclick="doThing()">

// RIGHT (data attribute + listener)
<button data-action="thing">

document.querySelectorAll('[data-action]').forEach(el => {
    el.addEventListener('click', () => handleAction(el.dataset.action));
});
```

---

### GSAP Animations Not Playing

**Symptoms:** Elements static, no animation

**Check:**
1. GSAP loaded (check Network tab)
2. Element exists when animation runs
3. No CSS `visibility: hidden` or `display: none`

---

## Tauri Issues

### invoke() Returns Undefined

**Symptoms:** Tauri commands not working in browser

**Solution:** Check for Tauri environment
```javascript
function getInvoke() {
    if (window.__TAURI__?.core?.invoke) {
        return window.__TAURI__.core.invoke;
    }
    return null; // Browser fallback
}
```

---

### Command Not Found

**Symptoms:** "Command X not found"

**Check:**
1. Command registered in lib.rs
2. Tauri app rebuilt after adding command
3. Command name matches exactly

---

## Data Issues

### Supabase Connection Failed

**Symptoms:** KB queries fail

**Check:**
1. `.env` file exists with correct keys
2. SUPABASE_URL format correct
3. Network connectivity
4. RLS policies if using anon key

**Verify Schema:**
```sql
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'knowledge_base';
```

---

### Google Drive Sync Issues

**Symptoms:** Files not appearing, sync errors

**Solutions:**
1. Check Google Drive Desktop status
2. Wait for sync to complete
3. Restart Google Drive Desktop
4. **NEVER run npm on synced folders**

---

## Performance Issues

### Slow Page Load

**Check:**
1. Network tab for large files
2. Console for excessive logging
3. Inefficient animations (too many simultaneous)

**Optimize:**
- Lazy load heavy content
- Use `will-change` sparingly
- Reduce animation complexity

---

### Memory Leaks

**Symptoms:** App slows over time

**Check:**
1. Event listeners not removed
2. Timers not cleared
3. Growing DOM nodes

**Solution:**
```javascript
// Clean up on unmount
clearInterval(timerId);
element.removeEventListener('click', handler);
```

---

## Recovery Procedures

### Restore from Backup

**Location:** `G:\My Drive\00 - Trajanus USA\09-Backups\`

```bash
# Restore specific file
cp archive/index_YYYYMMDD_BACKUP.html src/index.html
```

---

### Git Recovery

```bash
# See recent changes
git diff

# Revert specific file
git checkout -- src/index.html

# Revert to last commit
git reset --hard HEAD
```

---

### Full Reset

**Nuclear option - use sparingly:**
```bash
cd C:\Dev\trajanus-command-center
rm -rf node_modules
git checkout .
npm install
npm run dev
```

---

## Getting Help

1. Check CHANGELOG.md for similar issues
2. Search .claude.md files for guidance
3. Use knowledge-retriever agent for KB search
4. Document new issues in CHANGELOG.md

---

**Last Updated:** 2026-01-17
