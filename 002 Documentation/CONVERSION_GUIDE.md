# How to Find & Convert All Unconverted Files

## Step 1: Scan for Unconverted Files

```powershell
cd "G:\My Drive\00 - Trajanus USA"
.\scan_for_unconverted.ps1
```

**This shows:**
- How many .docx and .md files remain
- Which folders have the most files
- Total count

## Step 2: Convert Everything Recursively

```powershell
cd "G:\My Drive\00 - Trajanus USA"
.\convert_all_recursive.ps1
```

**This will:**
- Process ALL folders (not just top level)
- Convert all .md files to Google Docs
- Skip folders like Credentials, .git, node_modules
- Show progress for each folder
- Give final count

## For .docx Files (Separate Process)

The batch script only handles .md files. For .docx:

```powershell
cd "G:\My Drive\00 - Trajanus USA"
Get-ChildItem -Recurse -Filter "*.docx" | ForEach-Object {
    python ".\08-EOS-Files\convert_to_google_docs.py" $_.FullName
}
```

**This converts ALL .docx files across all folders.**

## Quick Status Check

To see how many files are left:

```powershell
$md = (Get-ChildItem -Recurse -Filter "*.md").Count
$docx = (Get-ChildItem -Recurse -Filter "*.docx").Count
Write-Host "Markdown: $md files"
Write-Host "Word Docs: $docx files"
Write-Host "Total: $($md + $docx) files"
```

---

**Bottom line:** 
1. Download both .ps1 files
2. Put in `G:\My Drive\00 - Trajanus USA\`
3. Run scan first to see what you have
4. Run recursive converter to get them all
