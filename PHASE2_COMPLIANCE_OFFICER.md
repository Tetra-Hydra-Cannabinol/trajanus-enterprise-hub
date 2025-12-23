# PHASE 2: COMPLIANCE OFFICER AGENT

**EXECUTE IMMEDIATELY AFTER PHASE 1 VERIFICATION**

---

## MISSION: CREATE AUTONOMOUS COMPLIANCE MONITORING

**Agent Name:** Compliance Officer (CO)
**Model:** Claude Sonnet 4.5
**Role:** Real-time protocol enforcement for CC and all sub-agents

---

## CO AGENT SPECIFICATION:

### Core Responsibilities:

1. **Monitor CC's proposed actions BEFORE execution**
   - Review str_replace commands for surgical edit compliance
   - Check file handling protocols
   - Verify testing procedures
   - Flag violations BEFORE code runs

2. **Monitor Claude Prime's instructions**
   - Check if instructions follow established protocols
   - Flag when Prime accepts non-compliant work
   - Ensure enforcement is happening

3. **Real-time intervention**
   - PAUSE workflow when violation detected
   - Require correction before proceeding
   - Log all violations for analysis

4. **Reporting**
   - Daily compliance summary
   - Violation patterns
   - Improvement recommendations

---

## TECHNICAL ARCHITECTURE:

### Option A: Pre-execution Review (Recommended)

```
User Request
    ↓
Claude Prime creates instruction
    ↓
CO reviews instruction ← CHECKPOINT 1
    ↓ (if compliant)
CC receives instruction
    ↓
CC proposes action
    ↓
CO reviews action ← CHECKPOINT 2
    ↓ (if compliant)
CC executes
    ↓
CO verifies result ← CHECKPOINT 3
```

### Option B: Parallel Monitoring

```
CC working → CO watching in parallel
    ↓
Violation detected → CO pauses CC
    ↓
Correction required → CC redoes
    ↓
CO approves → Workflow continues
```

---

## IMPLEMENTATION STEPS:

### STEP 1: Create CO System Prompt

**File:** `compliance_officer_prompt.md`

**Content:**
```markdown
You are the Compliance Officer for Trajanus USA development.

Your ONLY job: Enforce protocols.

Protocols to enforce:
1. Surgical edits only (str_replace for small changes)
2. No rewriting entire files
3. Test after each change
4. Provide evidence of testing
5. Follow Question Mark Protocol
6. Backup before edits

When you detect violation:
1. PAUSE workflow
2. Explain violation
3. Reference protocol
4. Require correction
5. Do NOT allow proceeding until fixed

You can override anyone - including Claude Prime.
```

### STEP 2: Create CO Integration Script

**File:** `scripts/compliance_officer.py`

```python
# CO runs as separate Claude instance
# Monitors CC's output
# Approves/rejects/pauses based on protocol compliance

import anthropic
import sys

class ComplianceOfficer:
    def __init__(self):
        self.client = anthropic.Client()
        self.violations = []
    
    def review_action(self, proposed_action):
        """Review CC's proposed action before execution"""
        # Check for protocol violations
        # Return APPROVED / REJECTED / PAUSED
        pass
    
    def pause_workflow(self, reason):
        """Halt CC until violation corrected"""
        print(f"⚠️ WORKFLOW PAUSED: {reason}")
        # Require correction
        pass
    
    def log_violation(self, violation):
        """Track violations for analysis"""
        self.violations.append(violation)
```

### STEP 3: Integrate CO into CC Workflow

**Modify CC startup to include CO:**
```bash
# In CC terminal
python scripts/compliance_officer.py &  # Run in background

# CC checks with CO before each action
```

### STEP 4: Test CO with Simple Task

**Test scenario:**
1. Give CC task to edit index.html
2. CC attempts full file rewrite
3. CO detects violation
4. CO pauses workflow
5. CC must redo with str_replace
6. CO approves
7. Workflow continues

---

## DELIVERABLES:

1. ✓ CO system prompt created
2. ✓ CO integration script written
3. ✓ CO tested with violation scenario
4. ✓ CO integrated into CC workflow
5. ✓ Compliance report template created

---

## SUCCESS CRITERIA:

- CO catches surgical edit violations
- CO pauses non-compliant work
- CC cannot proceed without CO approval
- Violation log tracks patterns
- Protocol compliance improves measurably

---

**BEGIN PHASE 2 WHEN PHASE 1 VERIFIED.**
