# QCM SUBMITTAL REVIEW WORKSPACE - DESIGN SPECIFICATION
**Date:** December 1, 2025
**Version:** v3.4.0
**Feature:** Interactive workspace for submittal review with Claude integration

## OVERVIEW

Transform the terminal into a 3-panel workspace for managing submittal reviews. Bill can browse files, select documents, write review instructions, and send everything to Claude for analysis.

## DESIGN VISION

### Problem Being Solved
- Need to review submittals (shop drawings, product data, specs) against project requirements
- Documents scattered across Google Drive folders
- Review process needs structure and documentation
- Want Claude to perform detailed technical review
- Need to track what's been reviewed and save review instructions

### Solution
Interactive workspace in terminal with file browsing, instruction writing, and Claude integration.

---

## 3-PANEL WORKSPACE LAYOUT

### LEFT PANEL: Document Browser
**Purpose:** Navigate and select files from Google Drive

**Features:**
- Folder navigation (breadcrumb trail)
- File list with icons (PDF, DWG, DOCX, etc.)
- Checkbox selection (multi-select)
- Preview thumbnails on hover
- Quick filters (by type: PDFs only, Drawings only, etc.)
- Search within current folder
- Favorite folders (quick access to common locations)

**Navigation:**
- Start at project root folder
- Click folder name to open
- Breadcrumb trail for navigation back
- "Up One Level" button

**File Display:**
```
☐ 📄 Submittal_001_Shop_Drawings.pdf (2.3 MB)
☐ 📄 Product_Data_Concrete_Mix.pdf (1.1 MB)
☐ 📐 Structural_Details_Sheet_S-101.dwg (5.6 MB)
☐ 📄 Spec_Section_03300_Concrete.pdf (890 KB)
```

### CENTER PANEL: Review Instructions
**Purpose:** Write directions for Claude's review

**Features:**
- Large text area for instructions
- Character count
- Instruction templates dropdown:
  - "Shop Drawing Review"
  - "Product Data Review"
  - "Specification Compliance"
  - "Structural Review"
  - "MEP Coordination Review"
  - "Custom..."

**Template Example (Shop Drawing Review):**
```
Review the selected shop drawings for:
1. Compliance with contract specifications
2. Dimensional accuracy against contract drawings
3. Material specifications match approved submittals
4. Fabrication details are constructible
5. Connection details are adequate
6. Any deviations from contract requirements

Flag any issues requiring clarification or correction.
Provide specific references to spec sections and drawing numbers.
```

**User can:**
- Select template (auto-fills instructions)
- Edit/customize instructions
- Save custom templates
- Clear and start fresh

### RIGHT PANEL: Selected Documents Queue
**Purpose:** Show selected files ready for review

**Features:**
- List of checked files from left panel
- Drag to reorder (review order)
- Remove button (×) for each file
- File metadata: name, size, type, date modified
- Total file count
- Total size

**Display:**
```
SELECTED DOCUMENTS (3)
━━━━━━━━━━━━━━━━━━━━━━━━
1. 📄 Submittal_001_Shop_Drawings.pdf
   2.3 MB | Modified: Nov 28, 2025
   [×] Remove
   
2. 📄 Product_Data_Concrete_Mix.pdf
   1.1 MB | Modified: Nov 25, 2025
   [×] Remove
   
3. 📄 Spec_Section_03300_Concrete.pdf
   890 KB | Modified: Oct 15, 2025
   [×] Remove

Total: 4.3 MB
```

---

## ACTION BUTTONS (Bottom Bar)

**Primary Actions:**
1. **🚀 Send to Claude for Review**
   - Uploads all selected files
   - Includes review instructions
   - Opens Claude chat interface with context loaded
   - Logs submission in terminal

2. **💾 Save Setup**
   - Saves file selection + instructions
   - Prompts for setup name: "Submittal 001 - Structural Steel"
   - Stores in localStorage or Google Drive
   - Can be recalled later

3. **📂 Load Saved Setup**
   - Shows list of saved setups
   - Click to load
   - Restores file selection + instructions
   - Ready to send or modify

4. **🗑️ Clear Workspace**
   - Clears all selections
   - Clears instructions
   - Resets to empty state
   - Confirms before clearing

**Secondary Actions:**
5. **📋 Copy File List** - Copies selected files to clipboard
6. **📊 View Review History** - Shows past reviews for this project

---

## EXAMPLE WORKFLOW

### Scenario: Review Structural Steel Shop Drawings

**Step 1: Access Workspace**
- Bill clicks "Submittal Review" button in QCM Toolkit
- Terminal transforms into 3-panel workspace
- Left panel shows project folder structure

**Step 2: Navigate to Documents**
```
My Drive > Guatemala SOUTHCOM > Submittals > Structural Steel
```
- Bill clicks through folders in left panel
- Breadcrumb trail shows path
- Files appear in list

**Step 3: Select Documents**
Bill checks:
- ☑ Shop_Drawings_Steel_Beams.pdf
- ☑ Product_Data_W18x50_Beams.pdf
- ☑ Spec_Section_05120_Structural_Steel.pdf
- ☑ Contract_Drawings_S-201_to_S-205.pdf

**Step 4: Write Instructions (or use template)**
- Bill selects "Shop Drawing Review" template
- Template auto-fills center panel
- Bill adds: "Pay special attention to connection details at columns B-3 and C-4. These were flagged in RFI #027."

**Step 5: Review Queue**
Right panel shows 4 selected files:
- Total size: 12.8 MB
- Bill can reorder if needed
- Bill verifies all files are correct

**Step 6: Send to Claude**
- Bill clicks "🚀 Send to Claude for Review"
- System uploads files
- Opens Claude interface with context:
  ```
  SUBMITTAL REVIEW REQUEST
  Project: Guatemala SOUTHCOM
  Date: December 1, 2025
  Reviewer: Claude AI
  
  Documents for Review (4):
  - Shop_Drawings_Steel_Beams.pdf
  - Product_Data_W18x50_Beams.pdf
  - Spec_Section_05120_Structural_Steel.pdf
  - Contract_Drawings_S-201_to_S-205.pdf
  
  Review Instructions:
  [Bill's instructions here]
  ```

**Step 7: Claude Reviews**
Claude analyzes all documents and responds with:
- Compliance findings
- Dimensional checks
- Material verification
- Connection detail analysis
- List of deficiencies or clarifications needed
- Specific references to spec sections and drawing numbers
- Recommendation: Approve, Approve as Noted, Revise and Resubmit

**Step 8: Save Results**
- Bill clicks "💾 Save Setup"
- Names it: "Submittal 001 - Structural Steel - Rev A"
- Saves file list + instructions + Claude's response
- Can recall later for Rev B review

---

## TECHNICAL IMPLEMENTATION

### HTML Structure

**Terminal Body for QCM Workspace:**
```html
<div class="terminal-body" id="terminal-qcm-submittal" data-tab="qcm-submittal">
    <div class="qcm-workspace">
        <!-- Left Panel: File Browser -->
        <div class="qcm-panel qcm-file-browser">
            <div class="panel-header">Document Browser</div>
            <div class="breadcrumb" id="qcmBreadcrumb">
                My Drive > Guatemala SOUTHCOM > Submittals
            </div>
            <div class="folder-list" id="qcmFolders">
                <!-- Folder items populate here -->
            </div>
            <div class="file-list" id="qcmFiles">
                <!-- File items with checkboxes populate here -->
            </div>
        </div>
        
        <!-- Center Panel: Instructions -->
        <div class="qcm-panel qcm-instructions">
            <div class="panel-header">Review Instructions</div>
            <select id="qcmTemplateSelect" class="template-select">
                <option value="">Select template...</option>
                <option value="shop-drawing">Shop Drawing Review</option>
                <option value="product-data">Product Data Review</option>
                <option value="spec-compliance">Specification Compliance</option>
                <option value="structural">Structural Review</option>
                <option value="custom">Custom...</option>
            </select>
            <textarea id="qcmInstructions" class="instructions-area" placeholder="Write review instructions for Claude..."></textarea>
            <div class="char-count">
                <span id="qcmCharCount">0</span> characters
            </div>
        </div>
        
        <!-- Right Panel: Selected Queue -->
        <div class="qcm-panel qcm-selected-queue">
            <div class="panel-header">
                Selected Documents (<span id="qcmSelectedCount">0</span>)
            </div>
            <div class="selected-list" id="qcmSelectedList">
                <!-- Selected files populate here -->
            </div>
            <div class="queue-summary">
                Total Size: <span id="qcmTotalSize">0 MB</span>
            </div>
        </div>
    </div>
    
    <!-- Action Buttons -->
    <div class="qcm-actions">
        <button class="session-btn primary" onclick="sendToClaudeReview()">
            🚀 Send to Claude for Review
        </button>
        <button class="session-btn" onclick="saveQCMSetup()">
            💾 Save Setup
        </button>
        <button class="session-btn" onclick="loadQCMSetup()">
            📂 Load Saved Setup
        </button>
        <button class="session-btn" onclick="clearQCMWorkspace()">
            🗑️ Clear Workspace
        </button>
    </div>
</div>
```

### CSS Styling

**3-Panel Layout:**
```css
.qcm-workspace {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 15px;
    height: calc(100% - 80px); /* Leave room for action buttons */
    padding: 15px;
}

.qcm-panel {
    background: rgba(45, 24, 16, 0.6);
    border: 1px solid rgba(204, 110, 31, 0.3);
    border-radius: 6px;
    padding: 15px;
    overflow-y: auto;
}

.panel-header {
    font-weight: bold;
    color: var(--orange-light);
    margin-bottom: 15px;
    font-size: 1.1rem;
    border-bottom: 1px solid rgba(204, 110, 31, 0.3);
    padding-bottom: 8px;
}

.qcm-actions {
    display: flex;
    gap: 10px;
    padding: 15px;
    border-top: 1px solid rgba(204, 110, 31, 0.3);
    background: rgba(45, 24, 16, 0.8);
}

.instructions-area {
    width: 100%;
    height: calc(100% - 120px);
    background: rgba(31, 20, 16, 0.8);
    color: var(--cream);
    border: 1px solid rgba(204, 110, 31, 0.3);
    border-radius: 4px;
    padding: 10px;
    font-family: monospace;
    font-size: 0.9rem;
    resize: none;
}
```

### JavaScript Functions

**Key Functions to Implement:**

1. **loadQCMFileBrowser(folderId)** - Load files from Google Drive folder
2. **selectQCMFile(fileId)** - Add file to selected queue
3. **removeQCMFile(fileId)** - Remove file from queue
4. **loadQCMTemplate(templateName)** - Load instruction template
5. **sendToClaudeReview()** - Upload files + instructions to Claude
6. **saveQCMSetup()** - Save configuration to localStorage
7. **loadQCMSetup()** - Load saved configuration
8. **clearQCMWorkspace()** - Reset workspace

### Integration with Google Drive API

**File Browser:**
- Use existing `google_drive_search` tool
- List folders and files
- Get file metadata (name, size, type, date)
- Download URLs for preview

**File Upload to Claude:**
- Use Google Drive fetch to get file contents
- Convert to base64 if needed
- Send via Claude API or upload mechanism
- Include in context with instructions

---

## INSTRUCTION TEMPLATES

### Template 1: Shop Drawing Review
```
Review the selected shop drawings for:

1. COMPLIANCE
   - Contract specifications compliance
   - Design intent maintained
   - Material specifications match approved submittals

2. TECHNICAL ACCURACY
   - Dimensional accuracy against contract drawings
   - Fabrication details are constructible
   - Connection details are adequate
   - Load paths are clear and correct

3. COORDINATION
   - No conflicts with other trades
   - Field conditions accommodated
   - Proper clearances maintained

4. DEVIATIONS
   - Flag any deviations from contract requirements
   - Note substitutions or alternatives proposed
   - Identify items requiring clarification

Provide specific references to:
- Specification sections
- Drawing numbers and detail references
- Contract requirements

Recommendation: [Approve / Approve as Noted / Revise and Resubmit]
```

### Template 2: Product Data Review
```
Review the selected product data submittals for:

1. PRODUCT SPECIFICATIONS
   - Manufacturer and model match specified
   - Performance characteristics meet requirements
   - Physical properties comply with specs
   - Certifications and testing documentation included

2. MATERIALS & FINISHES
   - Materials match specification requirements
   - Finishes and colors as specified
   - Warranty information provided

3. INSTALLATION
   - Installation instructions included
   - Special requirements noted
   - Maintenance requirements documented

4. COMPLIANCE
   - Building code compliance verified
   - Industry standards met
   - Environmental requirements satisfied

Flag any:
- Non-compliant items
- Missing information
- Substitutions requiring approval

Recommendation: [Approve / Approve as Noted / Revise and Resubmit]
```

### Template 3: Specification Compliance
```
Compare submitted documents against specification requirements:

SPECIFICATION SECTION: [Section number and title]

Review for:
1. Materials compliance
2. Performance criteria met
3. Testing requirements satisfied
4. Installation methods conform
5. Quality standards achieved

For each requirement in the specification:
- State if compliant or non-compliant
- Provide specific page/section references
- Note any deviations or substitutions
- Identify missing information

Summary:
- Total requirements: [count]
- Compliant: [count]
- Non-compliant: [count]
- Clarifications needed: [count]

Recommendation: [Approve / Approve as Noted / Revise and Resubmit]
```

---

## DATA STORAGE

### LocalStorage Schema

**Saved Setups:**
```javascript
{
  "qcm_setups": {
    "submittal_001_structural_steel": {
      "name": "Submittal 001 - Structural Steel - Rev A",
      "date_created": "2025-12-01T14:30:00Z",
      "project": "Guatemala SOUTHCOM",
      "files": [
        {
          "id": "1abc...",
          "name": "Shop_Drawings_Steel_Beams.pdf",
          "path": "My Drive/Guatemala SOUTHCOM/Submittals/Structural Steel",
          "size": 2457600,
          "type": "application/pdf"
        }
      ],
      "instructions": "Review the selected shop drawings for...",
      "template_used": "shop-drawing",
      "claude_response": "REVIEW COMPLETED: ...",
      "status": "completed",
      "recommendation": "Approve as Noted"
    }
  }
}
```

### Review History
```javascript
{
  "qcm_review_history": [
    {
      "id": "rev_001",
      "setup_name": "Submittal 001 - Structural Steel - Rev A",
      "date_submitted": "2025-12-01T14:35:00Z",
      "reviewer": "Claude AI",
      "files_count": 4,
      "status": "completed",
      "recommendation": "Approve as Noted",
      "deficiencies_count": 3
    }
  ]
}
```

---

## USER EXPERIENCE FLOW

### Opening Workspace
1. Bill clicks "Submittal Review" button
2. Terminal switches to QCM workspace layout
3. Left panel shows project root folder
4. Center panel is empty (ready for instructions)
5. Right panel shows "No documents selected"
6. Action buttons enabled/disabled appropriately

### Selecting Files
1. Bill navigates folders in left panel
2. Clicks checkboxes next to files
3. Selected files appear in right panel immediately
4. File count updates
5. Total size updates
6. Files can be unchecked to remove

### Writing Instructions
1. Bill clicks template dropdown (optional)
2. Selects template (e.g., "Shop Drawing Review")
3. Instructions auto-fill in textarea
4. Bill edits/customizes as needed
5. Character count updates live

### Sending to Claude
1. Bill clicks "🚀 Send to Claude for Review"
2. System validates:
   - At least 1 file selected ✓
   - Instructions not empty ✓
3. Shows progress: "Uploading files... (1 of 4)"
4. Creates Claude prompt with context
5. Opens interface or shows response in workspace
6. Logs submission to terminal

### Saving Setup
1. Bill clicks "💾 Save Setup"
2. Modal prompts for name
3. Saves to localStorage
4. Confirms: "Setup saved: Submittal 001..."
5. Available in "Load Saved Setup" list

---

## SUCCESS METRICS

**Workspace is successful if:**
- ✓ Bill can navigate to project folders easily
- ✓ Bill can select multiple documents quickly
- ✓ Templates speed up instruction writing
- ✓ Claude receives all files and instructions correctly
- ✓ Reviews are saved and can be recalled
- ✓ Workflow is faster than manual process
- ✓ Review quality is high and consistent

---

## PHASE 1 IMPLEMENTATION (MVP)

**Build first:**
1. 3-panel layout in terminal
2. Hardcoded file browser (mock data for testing)
3. Instruction templates (dropdown + textarea)
4. Selected files queue (right panel)
5. Send button (logs to terminal for now)

**Test thoroughly before adding:**
- Google Drive integration
- Actual file uploads to Claude
- Save/load functionality
- Review history tracking

---

## FUTURE ENHANCEMENTS

**Phase 2:**
- Photo uploads (for site conditions)
- Markup tools (annotate PDFs)
- Comparison view (side-by-side documents)
- Submittal log integration
- Email notification when review complete
- Multiple reviewer workflow (sequential approvals)

**Phase 3:**
- AI-powered pre-review (flag obvious issues)
- Automated spec compliance checking
- Integration with Procore/RMS submittal logs
- Mobile app for field reviews
- Voice-to-text for instructions
- OCR for handwritten notes on drawings

---

## FILES TO BE MODIFIED
- index_NO_PASSWORD.html (add QCM workspace)
- CSS for 3-panel layout
- JavaScript for workspace functions
- Integration with existing Google Drive tools

## FILES TO BE CREATED
- None (all in single HTML file for now)

## BACKUP
- index_BACKUP_2025-12-01_BeforeQCMWorkspace.html

---

**READY TO BUILD - AWAITING IMPLEMENTATION**
