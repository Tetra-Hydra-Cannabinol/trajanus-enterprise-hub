# Code Repository - November 24, 2025

## Session Code Production

### 1. Command Center Button CSS (Green 3D Style)
```css
.session-btn {
    padding: 20px 40px;
    background: linear-gradient(145deg, #2d7a4f, #1e5c3a);
    color: #e0f0e8;
    border: none;
    border-radius: 15px;
    cursor: pointer;
    font-size: 1.1rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    transition: all 0.2s ease;
    box-shadow: 
        0 6px 20px rgba(0, 0, 0, 0.4),
        inset 0 1px 0 rgba(255, 255, 255, 0.1),
        inset 0 -2px 5px rgba(0, 0, 0, 0.2);
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
    min-width: 220px;
}

.session-btn:hover {
    background: linear-gradient(145deg, #3a9963, #2d7a4f);
    color: #ffffff;
    box-shadow: 
        0 8px 25px rgba(0, 0, 0, 0.5),
        inset 0 1px 0 rgba(255, 255, 255, 0.2),
        inset 0 -2px 5px rgba(0, 0, 0, 0.2),
        0 0 15px rgba(60, 180, 100, 0.4);
    transform: translateY(-2px);
}

.session-btn:active {
    background: linear-gradient(145deg, #1e5c3a, #15442b);
    transform: translateY(1px);
    box-shadow: 
        0 2px 10px rgba(0, 0, 0, 0.4),
        inset 0 2px 5px rgba(0, 0, 0, 0.3);
}
```

### 2. JavaScript - runConvertMD() with File Picker
```javascript
function runConvertMD() {
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = '.md';
    fileInput.multiple = true;
    fileInput.onchange = function(e) {
        const files = Array.from(e.target.files).map(f => f.name).join(', ');
        const batchContent = `@echo off
title TRAJANUS USA - Convert MD to Google Docs
color 0B
cd "G:\\My Drive\\00 - Trajanus USA\\00-Command-Center"
echo.
echo  =====================================================
echo   TRAJANUS USA - CONVERT MD TO GOOGLE DOCS
echo  =====================================================
echo.
echo  Files to convert: ${files}
echo.
python convert_md_to_gdocs.py ${files.replace(/, /g, ' ')}
pause`;

        const blob = new Blob([batchContent], { type: 'text/plain' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'convert_md_to_gdocs.bat';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
        
        alert('Batch file downloaded for: ' + files);
    };
    fileInput.click();
}
```

### 3. JavaScript - runConvertDOCX() with File Picker
```javascript
function runConvertDOCX() {
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = '.md';
    fileInput.multiple = true;
    fileInput.onchange = function(e) {
        const files = Array.from(e.target.files).map(f => f.name).join(', ');
        const batchContent = `@echo off
title TRAJANUS USA - Convert MD to Word DOCX
color 0E
cd "G:\\My Drive\\00 - Trajanus USA\\00-Command-Center"
echo.
echo  =====================================================
echo   TRAJANUS USA - CONVERT MD TO WORD DOCX
echo  =====================================================
echo.
echo  Files to convert: ${files}
echo.
python convert_md_to_docx.py ${files.replace(/, /g, ' ')}
pause`;

        const blob = new Blob([batchContent], { type: 'text/plain' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'convert_md_to_docx.bat';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
        
        alert('Batch file downloaded for: ' + files);
    };
    fileInput.click();
}
```

### 4. Python - convert_md_to_docx.py (Full Script)
```python
from docx import Document
from docx.shared import Inches, Pt
import os, sys, glob, re

def md_to_docx(filepath):
    filename = os.path.basename(filepath)
    docx_name = filename.replace('.md', '.docx')
    
    with open(filepath, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    doc = Document()
    lines = md_content.split('\n')
    
    for line in lines:
        if line.startswith('# '):
            doc.add_heading(line[2:], level=1)
        elif line.startswith('## '):
            doc.add_heading(line[3:], level=2)
        elif line.startswith('### '):
            doc.add_heading(line[4:], level=3)
        elif line.startswith('- ') or line.startswith('* '):
            doc.add_paragraph(line[2:], style='List Bullet')
        elif re.match(r'^\d+\. ', line):
            text = re.sub(r'^\d+\. ', '', line)
            doc.add_paragraph(text, style='List Number')
        elif line.strip():
            clean = line.replace('**', '').replace('*', '').replace('`', '')
            doc.add_paragraph(clean)
    
    doc.save(docx_name)
    return docx_name

def main():
    files = sys.argv[1:] if len(sys.argv) > 1 else glob.glob('*.md')
    for f in files:
        if os.path.exists(f):
            md_to_docx(f)

if __name__ == "__main__":
    main()
```

### 5. MASTER_DOC_IDS Configuration
```python
MASTER_DOC_IDS = {
    'Technical_Journal': '1iPZAmi2bYBRmDnsgwZK3UZFCsB_YHj9RvRtKWJqDb2Q',
    'Personal_Diary': '1HKOisNN8A5rf9YdFJnJSdgH326bdJTun2rDqObNvrM8',
    'Operational_Journal': None,  # NEEDS CORRECT ID
    'Session_Summary': None,      # NEEDS CORRECT ID
    'Code_Repository': None,      # NEW
    'Website_Development': None   # NEW
}
```

## Files Modified
- Trajanus_Command_Center_ELEGANT.html (CSS, HTML, JavaScript)

## Files Created
- convert_md_to_docx.py
- NEXT_SESSION_PROMPT.md

## Notes
Code_Repository structure needs improvement - should auto-capture all code changes with version tracking and change detection.
