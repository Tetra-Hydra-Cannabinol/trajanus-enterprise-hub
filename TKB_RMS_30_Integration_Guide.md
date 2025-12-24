# RMS 3.0 INTEGRATION - TRAJANUS KNOWLEDGE BASE

**Document Type:** Integration Guide  
**Category:** USACE Construction Management  
**Last Updated:** 2025-12-14  
**Applicable To:** USACE Federal Construction Contracts  

---

## EXECUTIVE SUMMARY

Resident Management System (RMS) 3.0 is the U.S. Army Corps of Engineers' (USACE) mandated construction management information system used by both Government Resident Offices and Contractors. This guide documents integration requirements for federal construction compliance.

**Critical Note:** RMS 3.0 is NOT a typical API-based system. Integration requires specific file export/import procedures and data exchange formats.

---

## SYSTEM OVERVIEW

### RMS 3.0 Purpose

**Government Side (RMS):**
- Contract administration
- Progress payment processing
- Quality assurance oversight
- Project documentation
- Schedule monitoring
- CEFMS integration (financial system)
- Promise 2 (P2) integration (project management)

**Contractor Side (QCS - Quality Control System):**
- Quality control management
- Daily reports
- Three-phase control checklists
- Submittal tracking
- Deficiency tracking
- RFI management
- Equipment/material tracking

### Architecture

**Database:**
- Inter-relational database
- Feeds USACE financial (CEFMS) and project management (P2) systems
- Network-based module
- Bi-directional data exchange between Government and Contractor

**System Requirements:**
- Windows 11 (64-bit)
- Windows 10 (64-bit)
- Windows 8 (64-bit)
- **64-bit system REQUIRED**
- No 32-bit support

---

## DATA EXCHANGE METHODS

### Method 1: File Export/Import (Primary)

**RMS 3.0 Key Feature:**
> "With RMS 3.0 there is no more importing/exporting."

**RMS 3.0 Architecture:**
- Cloud-based system
- Real-time data sharing
- No manual export/import between Gov and Contractor
- Automatic synchronization

**Pre-RMS 3.0 (Legacy):**
- Manual export from QCS
- File transfer to Government
- Import into RMS
- Labor-intensive, error-prone

### Method 2: Standard Data Exchange Format (SDEF)

**Purpose:** Import CPM schedules from external tools (Primavera P3, P6, MS Project)

**SDEF Capabilities:**
- Network analysis data import
- Resource data import
- Activity relationships
- Critical path preservation

**Import Process:**
1. Export schedule from P3/P6 in SDEF format
2. Import into RMS via built-in importer
3. RMS processes and integrates with contract data
4. Schedule activities link to submittal requirements

**File Format:**
- Standardized exchange format
- Supported by major scheduling tools
- Preserves network logic
- Maintains resource assignments

---

## INTEGRATION WITH TRAJANUS HUB

### Current State Challenges

**RMS 3.0 Limitations:**
- No documented public API
- No REST/SOAP endpoints
- No OAuth authentication
- Cloud-based with restricted access
- Government CAC (Common Access Card) required
- Contractor access through approved accounts only

**Integration Reality:**
RMS 3.0 integration is NOT traditional API integration. It's workflow coordination and data preparation.

### Recommended Approach

**Strategy: Data Preparation & Workflow Support**

**Rather than direct integration, Trajanus Hub should:**

1. **Prepare Data for RMS Entry:**
   - Quality control checklists → Format for QCS entry
   - Daily reports → Generate RMS-compatible formats
   - Submittal logs → Match RMS submittal format
   - Test results → Prepare for manual RMS entry

2. **Mirror RMS Data Structures:**
   - Maintain parallel database with RMS-compatible structure
   - Track RMS entry status locally
   - Generate reports in RMS format
   - Export to Excel for RMS bulk entry

3. **Schedule Integration (Via P6/SDEF):**
   - Trajanus → P6 → SDEF → RMS
   - Maintain schedule in P6
   - Export SDEF for RMS import
   - Track milestones in Trajanus
   - Sync via P6 as intermediary

### Data Structures to Support

**Daily Reports:**
```javascript
// RMS Daily Report Format
{
  date: "2024-12-14",
  weather: {
    morning: "Clear, 45°F",
    afternoon: "Partly cloudy, 52°F"
  },
  workforce: {
    contractor: 25,
    subcontractors: [
      { company: "ABC Electric", count: 8 },
      { company: "XYZ Plumbing", count: 6 }
    ]
  },
  equipment: [
    { type: "Excavator", hours: 8, operator: "John Doe" },
    { type: "Crane", hours: 6, operator: "Jane Smith" }
  ],
  workAccomplished: "Completed foundation pour Grid A1-A5. Started formwork for Grid B1.",
  safetyIncidents: "None",
  qualityIssues: "None",
  delays: "None"
}
```

**Three-Phase Control Checklist:**
```javascript
// Phase 1: Preparatory
{
  activity: "Foundation Pour",
  phase: "Preparatory",
  checklistItems: [
    { item: "Formwork inspected", status: "Complete", inspector: "RE" },
    { item: "Rebar placement verified", status: "Complete", inspector: "RE" },
    { item: "Concrete mix design approved", status: "Complete", inspector: "RE" },
    { item: "Weather forecast reviewed", status: "Complete", inspector: "QC" }
  ],
  meetingDate: "2024-12-13",
  attendees: ["RE", "QC Manager", "Superintendent"],
  approved: true
}

// Phase 2: Initial
{
  activity: "Foundation Pour",
  phase: "Initial",
  checklistItems: [
    { item: "First concrete tested", status: "Complete", inspector: "RE" },
    { item: "Slump verified", status: "Complete", inspector: "QC" },
    { item: "Placement technique approved", status: "Complete", inspector: "RE" }
  ],
  inspectionDate: "2024-12-14 08:00",
  approved: true
}

// Phase 3: Follow-up
{
  activity: "Foundation Pour",
  phase: "Follow-up",
  checklistItems: [
    { item: "Concrete curing verified", status: "Complete", inspector: "QC" },
    { item: "Test cylinders collected", status: "Complete", inspector: "Lab" },
    { item: "Final dimensions verified", status: "Complete", inspector: "RE" }
  ],
  inspectionDate: "2024-12-15",
  deficiencies: [],
  approved: true
}
```

**Submittal Tracking:**
```javascript
// RMS Submittal Format
{
  submittalNumber: "001",
  specSection: "03 30 00",
  description: "Ready-Mix Concrete",
  submittedDate: "2024-11-15",
  receivedDate: "2024-11-16",
  reviewDays: 14,
  dueDate: "2024-11-30",
  reviewedDate: "2024-11-28",
  status: "Approved",
  reviewAction: "A - Approved",
  reviewer: "John Engineer, PE",
  relatedActivity: "Foundation Pour",
  outstanding: false
}
```

**RFI Tracking:**
```javascript
// RMS RFI Format
{
  rfiNumber: "RFI-001",
  date: "2024-12-10",
  from: "ABC Construction",
  to: "USACE Resident Engineer",
  subject: "Foundation Rebar Spacing",
  question: "Specify rebar spacing at grid intersection A1-B1. Drawings show conflicting dimensions.",
  drawingReference: "S-102, Detail 3/S-102",
  specReference: "03 20 00",
  dateSent: "2024-12-10",
  responseRequired: "2024-12-17",
  responseDate: "2024-12-15",
  response: "Use 12 inch spacing per structural calculation dated 2024-11-01.",
  status: "Closed",
  affectsSchedule: false,
  affectsCost: false
}
```

---

## PAY ESTIMATE WORKFLOW

### RMS Pay Estimate Process

**Government Side:**
1. Contractor submits progress data
2. RMS calculates earned value
3. Government reviews and validates
4. Retainage calculated automatically
5. Integration with CEFMS for payment processing

**Contractor Side (QCS):**
1. Track daily progress
2. Update activity completion percentages
3. Submit progress data to Government
4. Outstanding submittals flagged automatically
5. Payment worksheets generated

### Trajanus Hub Support

**Preparation for Pay Estimates:**
```javascript
// Track Progress for RMS Submission
{
  payPeriod: "December 2024",
  lineItems: [
    {
      clin: "0001",
      description: "Foundation Work",
      scheduledValue: 150000.00,
      previouslyCompleted: 100000.00,
      thisMonth: 25000.00,
      totalCompleted: 125000.00,
      percentComplete: 83.33,
      balance: 25000.00,
      materials: {
        onSite: 5000.00,
        storedOffSite: 0.00
      },
      retainage: {
        rate: 0.10,
        amount: 12500.00
      }
    }
  ],
  totalScheduledValue: 1200000.00,
  totalCompleted: 850000.00,
  retainageHeld: 85000.00,
  netDue: 765000.00
}
```

**Export Format:**
- Excel spreadsheet matching RMS template
- PDF backup for records
- Supporting documentation (photos, test reports)
- Submittal status verification

---

## TRANSMITTAL SYSTEM

### ENG Form 4025 Integration

**RMS Transmittal Process:**
- Auto-generated transmittal forms
- Pre-filled with contract data
- Numbered sequentially
- Tracks submittal items
- Links to schedule activities

**Trajanus Hub Transmittal Support:**
```javascript
// Generate RMS-Compatible Transmittal
{
  transmittalNumber: "T-2024-045",
  date: "2024-12-14",
  from: "ABC Construction",
  to: "USACE Jacksonville District",
  project: "SOUTHCOM Guatemala Construction",
  contractNumber: "W9127823R0034",
  subject: "Submittal - Structural Steel",
  items: [
    {
      number: 1,
      description: "Shop Drawings - Structural Steel",
      specSection: "05 12 00",
      drawingNumber: "S-201",
      copies: 3,
      forAction: true
    }
  ],
  deliveryMethod: "Email",
  preparedBy: "John QC Manager",
  signature: "digital_signature_hash"
}
```

---

## QUALITY CONTROL DATA

### QC Daily Reports

**RMS QC Report Requirements:**
- Work performed by location
- Tests conducted
- Materials received
- Equipment on site
- Workforce count
- Safety observations
- Weather conditions

**Trajanus Hub QC Report Generation:**
```javascript
async function generateQCDailyReport(date) {
  const report = {
    date: date,
    project: getProjectDetails(),
    weather: await getWeatherData(date),
    workforce: getWorkforceCount(date),
    workPerformed: getWorkLog(date),
    materialsReceived: getMaterialDeliveries(date),
    equipmentOnSite: getEquipmentLog(date),
    testing: {
      concrete: getConcretTests(date),
      soil: getSoilTests(date),
      other: getOtherTests(date)
    },
    deficiencies: getDeficienciesIdentified(date),
    photos: getProgressPhotos(date)
  };
  
  // Format for RMS entry
  return formatForRMS(report);
}
```

### Deficiency Tracking

**RMS Punch List System:**
- Deficiency number auto-assigned
- Location specified
- Responsible party tracked
- Due date established
- Status tracked (Open/Closed)
- Photos attached
- Affects payment if outstanding

**Trajanus Integration:**
```javascript
// Deficiency Data Structure
{
  deficiencyNumber: "DEF-2024-012",
  dateIdentified: "2024-12-14",
  location: "Grid B2, Second Floor",
  description: "Concrete spalling at column base",
  specReference: "03 30 00",
  identifiedBy: "RE Inspector",
  responsibleParty: "ABC Construction",
  dueDate: "2024-12-21",
  status: "Open",
  photos: ["photo001.jpg", "photo002.jpg"],
  affectsPayment: true,
  correctiveAction: "Remove spalled concrete, repair per approved procedure",
  closedDate: null
}
```

---

## SCHEDULE INTEGRATION

### P6 → RMS via SDEF

**Workflow:**
```
Primavera P6 Schedule (Master) 
  ↓
Export to SDEF Format
  ↓
Import into RMS 3.0
  ↓
RMS Links Activities to Submittals/QC
```

**Critical Path Integration:**
- RMS identifies critical activities
- Outstanding submittals on critical path flagged
- Pay estimates reflect schedule progress
- Delays tracked and reported

**Trajanus Role:**
- Maintain P6 schedule locally
- Generate SDEF exports
- Coordinate schedule updates
- Track milestone achievements
- Alert on critical path impacts

---

## CEFMS INTEGRATION (Government Only)

**CEFMS: Corps of Engineers Financial Management System**

**RMS → CEFMS Data Flow:**
- Approved pay estimates
- Contract modifications
- Financial transactions
- Budget tracking

**Outages:**
- CEFMS occasionally offline for maintenance
- RMS cannot process payments during outage
- Plan accordingly (e.g., submit before known outages)

**Contractor Impact:**
- Cannot directly access CEFMS
- RMS handles integration automatically
- Payment delays if CEFMS offline

---

## IMPLEMENTATION STRATEGY

### Phase 1: Data Structure Alignment

**Objectives:**
- Mirror RMS data structures in Trajanus
- Prepare templates for all RMS forms
- Establish field mapping
- Create export procedures

**Deliverables:**
- Database schema matching RMS
- Excel templates for data export
- Form generators (daily reports, checklists, etc.)
- Export automation scripts

### Phase 2: Workflow Support

**Objectives:**
- Support contractor QC process
- Generate RMS-ready data
- Facilitate manual entry
- Reduce data entry errors

**Features:**
- Daily report generator
- Three-phase checklist templates
- Submittal log management
- RFI tracking system
- Deficiency punch list
- Progress photo organization

### Phase 3: Schedule Coordination

**Objectives:**
- Integrate with P6
- Generate SDEF exports
- Track milestones
- Monitor critical path

**Tools:**
- P6 integration (per P6 guide)
- SDEF export automation
- Milestone dashboard
- Schedule variance alerts

---

## USACE COMPLIANCE REQUIREMENTS

### Mandatory RMS Use

**USACE Policy:**
- RMS 3.0 mandated Corps-wide since 2001
- All USACE construction contracts
- Government and Contractor participation required
- Non-negotiable for federal construction

### Training Requirements

**Government:**
- RMS training required for all Resident Office staff
- Ongoing support from RMS Support Center

**Contractor:**
- QCS training recommended
- RMS Support Center provides contractor training
- Online resources available
- Help files and manuals provided

### Documentation Requirements

**Must Maintain in RMS:**
- Preconstruction conference minutes
- Coordination meeting minutes
- Three-phase control checklists
- Daily QC reports
- Submittal logs and transmittals
- RFI tracking
- Deficiency punch lists
- Progress photos
- Test results
- Pay estimate data
- Schedule updates

---

## TECHNICAL SPECIFICATIONS

### System Access

**Government Access:**
- CAC (Common Access Card) required
- VPN to USACE network
- RMS 3.0 launcher application
- Windows 64-bit OS

**Contractor Access:**
- Approved account creation
- RMS Support Center coordinates
- Non-DoD CAC accounts available
- Email-based authentication option

### Installation

**Download:**
- RMS website: https://rms.usace.army.mil
- Contractor mode installer
- Extract ZIP file
- Run RMSLauncher37Gov.exe
- Follow installation wizard

**Configuration:**
- No local database required (cloud-based)
- Internet connection required
- Firewall exceptions may be needed
- Antivirus exclusions recommended

---

## SUPPORT RESOURCES

### Official Support

**RMS Support Center:**
- Website: https://rms.usace.army.mil
- Email support available
- Help desk for technical issues
- Training materials

**Documentation:**
- RMS 3.0 Contractor Mode User Manual
- Installation guides
- Help files (context-sensitive)
- Video tutorials

### Training

**Available Training:**
- Installation procedures
- Daily operations
- Transmittal process
- Pay estimate entry
- Submittal tracking
- Deficiency management

**Access:**
- RMS website Downloads section
- PDF manuals
- Video guides
- Help files within application

---

## INTEGRATION CHECKLIST

### Pre-Implementation
- [ ] Confirm USACE contract requirements
- [ ] Request contractor RMS access
- [ ] Install RMS 3.0 contractor mode
- [ ] Complete RMS training
- [ ] Document RMS data structures
- [ ] Design Trajanus mirror database

### Development
- [ ] Build RMS-compatible data structures
- [ ] Create export templates (Excel, PDF)
- [ ] Develop form generators
- [ ] Build three-phase checklist system
- [ ] Implement submittal tracking
- [ ] Create RFI management
- [ ] Build deficiency punch list
- [ ] Integrate with P6 for SDEF export

### Testing
- [ ] Validate data exports against RMS
- [ ] Test manual entry workflow
- [ ] Verify SDEF schedule import
- [ ] Check form generation accuracy
- [ ] Validate calculations (pay estimates)

### Deployment
- [ ] Train QC staff on Trajanus → RMS workflow
- [ ] Establish data export procedures
- [ ] Create RMS entry checklist
- [ ] Monitor first pay period closely
- [ ] Refine based on feedback

---

## BEST PRACTICES

### Data Quality
- Enter data once in Trajanus
- Export to RMS format
- Validate before manual entry
- Maintain audit trail
- Reconcile monthly

### Efficiency
- Automate form generation
- Use templates consistently
- Batch similar data
- Schedule regular exports
- Minimize manual re-entry

### Compliance
- Follow USACE RMS protocols
- Maintain documentation
- Meet submission deadlines
- Keep RMS current
- Archive exports

---

## LIMITATIONS & WORKAROUNDS

### No API Access
**Limitation:** RMS 3.0 has no public API  
**Workaround:** Data preparation and export strategy

### Manual Entry Required
**Limitation:** Some data must be manually entered  
**Workaround:** Generate pre-filled Excel templates for bulk entry

### Cloud Dependency
**Limitation:** Requires internet connection  
**Workaround:** Offline data collection in Trajanus, sync when online

### CAC Requirement
**Limitation:** Government access requires CAC  
**Workaround:** Contractors use approved non-DoD accounts

---

**END OF DOCUMENT**

**Next Steps:** Proceed to Traffic Study Requirements guide for civil engineering compliance.
