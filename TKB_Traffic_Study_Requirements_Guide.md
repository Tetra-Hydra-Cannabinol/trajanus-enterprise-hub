# TRAFFIC IMPACT STUDY REQUIREMENTS - TRAJANUS KNOWLEDGE BASE

**Document Type:** Compliance Guide  
**Category:** Civil Engineering / Transportation Planning  
**Last Updated:** 2025-12-14  
**Applicable To:** Development Projects Requiring Traffic Analysis  

---

## EXECUTIVE SUMMARY

Traffic Impact Studies (TIS) are technical analyses required by Federal, State, and local jurisdictions to assess how proposed developments affect the transportation system. This guide provides comprehensive requirements for creating municipality, city, and state-approved traffic studies.

**Key Standards:**
- ITE Trip Generation Manual (primary reference)
- MUTCD (Manual on Uniform Traffic Control Devices)
- Highway Capacity Manual (HCM)
- State DOT-specific requirements
- Local jurisdiction guidelines

---

## REGULATORY FRAMEWORK

### Federal Requirements

**Federal Highway Administration (FHWA):**
- Oversight for Interstate access changes
- National standards via MUTCD
- Traffic Monitoring Guide (2022)
- Highway Performance Monitoring System (HPMS)
- Federal-aid project requirements

**Key Federal Regulations:**
- 23 CFR 625.2(a) - Interstate access policy
- 23 CFR 655.603(d) - Operational analysis
- 23 CFR 771.111(f) - Environmental review
- Traffic Monitoring requirements per 23 CFR 420.105(b)

### State Requirements

**State DOT Authority:**
- Approve TIS for state highway access
- Set methodology standards
- Review operational analysis
- Enforce MUTCD compliance
- Coordinate with local jurisdictions

**Common State Triggers:**
- 100+ vehicle trips in peak hour
- Access to state highway
- State funding involved
- Interstate interchange impacts
- Regional transportation system effects

### Local Requirements

**Municipal/City Authority:**
- Land use approval process
- Zoning compliance
- Development review
- Local street network impacts
- Community safety concerns

**Typical Triggers:**
- New development > 50,000 sq ft
- Residential > 100 units
- Change in land use
- Site redevelopment
- Variance requests

---

## WHEN IS A TIS REQUIRED?

### Size/Intensity Thresholds

**General Rules (Vary by Jurisdiction):**

**Residential:**
- Single family: 50-100 units
- Multi-family: 40-75 units
- Senior housing: 75-150 units

**Commercial:**
- Retail: 20,000-50,000 sq ft
- Office: 25,000-100,000 sq ft
- Restaurant: 2,500-5,000 sq ft
- Fast food: 1,500-3,000 sq ft

**Industrial:**
- Manufacturing: 50,000-100,000 sq ft
- Warehouse: 100,000-200,000 sq ft
- Distribution center: 50,000-100,000 sq ft

**Institutional:**
- School: Varies by students
- Hospital: 50-100 beds
- Church: 300-500 seats

**Trip Generation Threshold:**
- Most jurisdictions: 100 peak hour trips
- Some stricter: 50 peak hour trips
- Congested areas: 25 peak hour trips

### Situational Triggers

**Always Required:**
- Interstate access changes
- State highway new access
- Federal funding involved
- Areas with capacity constraints
- History of crashes/safety concerns

**Often Required:**
- Change in land use
- Redevelopment increasing traffic
- Variance from zoning
- Proximity to sensitive areas (schools, hospitals)
- Already congested intersections

**May Be Waived:**
- Internal circulation changes only
- Reduction in trip generation
- Existing adequate capacity
- Previous study still valid (< 2 years)
- Minor modifications

---

## PRE-SUBMITTAL PROCESS

### Scoping Meeting

**Purpose:**
- Determine study requirements
- Define study area boundaries
- Agree on methodology
- Identify critical intersections
- Set timeline and deliverables

**Participants:**
- Developer/consultant
- Municipal traffic engineer
- State DOT (if applicable)
- Planning department
- Other jurisdictions (as needed)

**Scoping Deliverables:**
```
TRAFFIC IMPACT STUDY SCOPE APPROVAL FORM

Project Information:
- Name: [Development Name]
- Location: [Address/Intersection]
- Jurisdiction: [City/County]
- Land Use: [Type and size]
- Expected Trip Generation: [Peak hour trips]

Study Requirements:
- Study Area: [Define boundaries]
- Analysis Intersections: [List with justification]
- Study Horizon Years: [Base, Opening, Design]
- Analysis Periods: [AM peak, PM peak, other]
- Required Analyses: [LOS, safety, queuing, etc.]
- Special Considerations: [Transit, bike/ped, etc.]

Methodology:
- Trip Generation: [ITE manual edition]
- Trip Distribution: [Method and assumptions]
- Traffic Assignment: [Approach]
- Capacity Analysis: [HCM edition, software]
- Level of Service: [Standards]

Deliverables:
- Draft Study: [Due date]
- Final Study: [Due date]
- Format: [PDF copies, digital files]

Approved By: _________________ Date: _______
            [City Traffic Engineer]
```

### Jurisdictional Coordination

**Multi-Jurisdiction Projects:**
1. Identify all affected jurisdictions
2. Contact each agency early
3. Coordinate study scope
4. Submit to all simultaneously
5. Address each jurisdiction's comments
6. Obtain approvals from all

**Coordination Cover Sheet:**
- List all reviewing agencies
- Track submission dates
- Monitor review status
- Consolidate comments

---

## STUDY HORIZON YEARS

### Standard Analysis Years

**Opening Year (Year 1):**
- First year of project operation
- Full buildout assumed
- Background growth included
- "Opening day" conditions

**Interim Year (Optional):**
- Phased developments only
- Partial buildout milestones
- Each major phase analyzed
- Typically Year 3-5

**Design Horizon Year:**
- Long-term conditions
- Typically 10-20 years out
- Federal projects: 20 years
- Local projects: 10-15 years
- Background growth applied

### Background Growth Assumptions

**Sources:**
1. State DOT Planning Division
2. Metropolitan Planning Organization (MPO)
3. Regional Planning Organization (RPO)
4. Local comprehensive plan
5. Historic traffic counts (trending)

**Growth Rates:**
- Annual: 1-3% typical
- Compounding recommended
- Vary by roadway type
- Document source clearly

**Formula:**
```
Future Traffic = Current Traffic × (1 + growth_rate)^years
```

**Pipeline Projects:**
- Include approved developments
- Not yet constructed
- Same horizon year
- Documented status required

---

## TRIP GENERATION

### ITE Trip Generation Manual

**Primary Reference:**
- Institute of Transportation Engineers
- Updated periodically (use latest edition)
- Land use code specific
- Statistical equations and rates
- Regional adjustments

**Using ITE Manual:**
```
Trip Generation Calculation:

Base Trips = Size × Trip Rate

Example - Shopping Center:
- Size: 50,000 sq ft gross leasable area
- Land Use Code: 820 (Shopping Center)
- PM Peak Hour Rate: 3.71 trips/1000 sq ft (ITE 11th Edition)
- Calculation: 50,000 × (3.71/1000) = 185.5 ≈ 186 trips

Note: Use equations when provided (preferred over rates)
```

### Trip Adjustments

**Pass-By Trips:**
- Already on adjacent street
- Divert into site (not new to system)
- Typical: Retail 25-40%, Fast food 40-50%
- Reduce external trip generation

**Diverted Link Trips:**
- New route for existing trip
- Change path due to new development
- Captured from parallel routes
- Document methodology

**Internal Capture (Mixed-Use):**
- Trips between uses on same site
- Office → Restaurant lunch trips
- Residential → Retail trips
- Reduce external impacts

**Transit/Alternative Mode Reduction:**
- Near transit stations
- Bike/pedestrian friendly areas
- Apply reduction factor
- Justify with data

**Formula:**
```
External Trips = Base Trips × (1 - pass_by%) × (1 - internal_capture%) × (1 - transit%)
```

### Trip Distribution

**Methods:**

**1. Existing Traffic Patterns:**
- Analyze current turning movements
- Apply to site trips
- Most common method

**2. Travel Demand Model:**
- MPO/regional model
- Zone-to-zone patterns
- Complex developments

**3. Gravity Model:**
- Based on population centers
- Distance decay factors
- Manual calculation

**4. Manual Estimates:**
- Local knowledge
- Site observations
- Professional judgment

**Documentation:**
- Show distribution assumptions clearly
- Present in tables and figures
- Justify methodology
- Compare to reasonable expectations

---

## DATA COLLECTION

### Traffic Counts

**When to Count:**
- Tuesday, Wednesday, or Thursday
- Avoid holidays and weeks adjacent
- Avoid special events
- School in session (if relevant)
- Normal weather conditions
- Peak periods: 7-9 AM, 4-6 PM

**What to Count:**
- All study area intersections
- Site access locations
- Key roadway segments
- Turning movements (15-min intervals)
- Vehicle classification (if required)

**Count Duration:**
- Minimum 2 hours peak period
- Preferably 3 hours
- Capture peak 15-min period
- May need 12-24 hours for daily totals

**Methods:**
- Automatic tube counters (volume)
- Video recording (turning movements)
- Manual counts (complex intersections)
- Permanent count stations (historical)

### Field Observations

**Geometric Conditions:**
- Lane configurations
- Turn bay lengths
- Sight distances
- Signage and striping
- Signal timing (if signalized)

**Physical Constraints:**
- Right-of-way limits
- Utilities
- Drainage features
- Adjacent property uses
- Environmental features

**Safety Observations:**
- Crash history (3-5 years)
- Sight distance obstructions
- Conflict points
- Pedestrian/bicycle facilities
- Crosswalk locations

---

## CAPACITY ANALYSIS

### Highway Capacity Manual (HCM)

**Current Edition:** HCM 7th Edition (2022)

**Analysis Software:**
- Synchro (most common)
- VISSIM (microsimulation)
- HCS (HCM standalone)
- SimTraffic (simulation)
- Vistro

**Analysis Components:**

**1. Level of Service (LOS):**
```
LOS Definitions (Signalized Intersections):

LOS A: Delay ≤ 10 seconds (Excellent)
LOS B: Delay 10-20 seconds (Good)
LOS C: Delay 20-35 seconds (Satisfactory)
LOS D: Delay 35-55 seconds (Acceptable)
LOS E: Delay 55-80 seconds (Poor)
LOS F: Delay > 80 seconds (Failure)

Note: Standards vary by jurisdiction
```

**2. Volume-to-Capacity (V/C) Ratio:**
- V/C < 0.85: Acceptable (typical)
- V/C 0.85-1.00: Approaching capacity
- V/C > 1.00: Over capacity

**3. Queue Analysis:**
- 95th percentile queue length
- Storage capacity comparison
- Spillback potential
- Turn bay adequacy

### Analysis Scenarios

**Existing Conditions:**
- Current traffic + current geometry
- Baseline for comparison
- Identify existing deficiencies

**Background Conditions:**
- Growth + pipeline projects
- No site traffic
- Future without project

**Total Future Conditions:**
- Background + site traffic
- Future with project
- Assess total impact

**Analysis Periods:**
- Weekday AM peak (7-9 AM)
- Weekday PM peak (4-6 PM)
- Weekend peak (if applicable)
- Special event (if applicable)

---

## IMPACT CRITERIA

### Determining Significant Impact

**Common Thresholds:**

**Level of Service Degradation:**
- Project causes LOS to worsen by one letter grade, OR
- Project adds ≥ 5 seconds delay when already LOS E/F, OR
- Project increases V/C by ≥ 0.05 when already ≥ 0.90

**Volume Criteria:**
- Project adds ≥ 1% of intersection capacity, OR
- Project adds ≥ 50 vehicles in peak hour (signalized), OR
- Project adds ≥ 25 vehicles in peak hour (unsignalized)

**Safety Criteria:**
- Sight distance deficiency created
- Inadequate queue storage
- Crash history pattern worsened
- Pedestrian/bicycle conflict added

**Example Impact Analysis:**
```
Intersection: Main St & Oak Ave

                Existing    Background    Total Future    Impact
                ---------   ----------    ------------    ------
AM Peak LOS:    C (28s)     D (42s)       E (63s)        Significant
PM Peak LOS:    D (48s)     D (51s)       D (54s)        Not Significant

Conclusion: Mitigation required for AM peak period
```

---

## MITIGATION MEASURES

### Intersection Improvements

**Geometric Improvements:**
- Add turn lanes
- Lengthen storage
- Widen approaches
- Add through lanes
- Improve sight distance
- Realign approaches

**Traffic Control:**
- Install signal (warrant analysis required)
- Upgrade signal (add phases, coordination)
- Optimize signal timing
- Add stop control
- Improve signing/striping

**Access Management:**
- Consolidate driveways
- Right-in/right-out restrictions
- Median installation
- Driveway relocation
- Shared access agreements

### Site Access Design

**Driveway Location:**
- Minimum 150-200 ft from intersection
- Adequate sight distance
- Avoid horizontal/vertical curves
- Consider conflicting accesses

**Driveway Design:**
- Adequate width (12-24 ft)
- Appropriate radius (15-30 ft)
- Proper grade (≤ 8%)
- ADA compliant (if applicable)

**Turn Lanes:**
- Deceleration lanes (right turn)
- Left turn storage + taper
- Bypass lanes (right turn)
- Based on traffic volume

### Transportation Demand Management (TDM)

**Strategies:**
- Transit pass subsidies
- Carpool/vanpool programs
- Bicycle facilities
- Flexible work schedules
- Telecommuting policies
- Parking management

**Applicability:**
- Large employment centers
- Urban/transit-accessible sites
- Environmentally sensitive areas
- Areas with capacity constraints

---

## SPECIAL ANALYSES

### Signal Warrant Analysis

**MUTCD Warrants (9 total):**
1. Eight-Hour Vehicular Volume
2. Four-Hour Vehicular Volume
3. Peak Hour
4. Pedestrian Volume
5. School Crossing
6. Coordinated Signal System
7. Crash Experience
8. Roadway Network
9. Intersection Near Railroad Crossing

**Most Common: Warrant 3 - Peak Hour**
```
Minimum Requirements:
- Both streets: ≥ 2 lanes
- Major street: ≥ 600 vph (2+ lanes) or ≥ 500 vph (1 lane)
- Minor street: ≥ 150 vph (1 lane) or ≥ 200 vph (2+ lanes)

Note: Meeting warrant ≠ automatic signal
       Engineering judgment required
```

### Pedestrian/Bicycle Analysis

**Requirements:**
- MUTCD pedestrian standards
- ADA compliance
- Crosswalk warrant analysis
- Sidewalk connectivity
- Bike lane/path provisions

**Key Elements:**
- Crossing distances
- Signal timing (walk/don't walk)
- Refuge islands
- Curb ramps
- Detectable warnings

### Safety Analysis

**Crash Data:**
- 3-5 years of history
- All crash types
- Severities
- Causation factors
- Crash rates

**Analysis:**
- Identify patterns
- Compare to averages
- Project impact on crashes
- Mitigation effectiveness

**Sources:**
- State DOT crash database
- Local police reports
- FHWA Crash Modification Factors

---

## REPORT STRUCTURE

### Required Sections

**1. Introduction & Executive Summary:**
- Project description
- Study purpose
- Key findings
- Recommendations summary

**2. Existing Conditions:**
- Study area description
- Road network
- Traffic counts
- Existing LOS
- Crash history
- Pedestrian/bicycle facilities

**3. Site Development:**
- Proposed land use
- Site plan
- Access locations
- Phasing (if applicable)

**4. Traffic Forecasting:**
- Trip generation
- Trip distribution
- Trip assignment
- Background growth
- Total future traffic

**5. Traffic Operations Analysis:**
- Methodology
- Analysis scenarios
- Capacity analysis results
- Impact assessment

**6. Mitigation Recommendations:**
- Required improvements
- Cost estimates
- Responsibility (developer vs. agency)
- Timing/phasing

**7. Conclusions:**
- Summary of findings
- Compliance with standards
- Outstanding issues

**8. Appendices:**
- Traffic count data
- HCM/Synchro output
- Signal warrant worksheets
- Site distance calculations
- Crash data (sealed/separate)
- Correspondence

### Presentation Standards

**Figures Required:**
- Site location map
- Study area map
- Existing traffic volumes
- Trip distribution diagram
- Future traffic volumes
- Intersection geometry
- Recommended improvements

**Tables Required:**
- Trip generation calculations
- Capacity analysis summary (LOS table)
- Queue analysis
- Signal warrants (if applicable)

**Format:**
- Professional binding
- Color preferred
- Clear graphics
- Legible text
- Page numbers
- Table of contents

---

## REVIEW & APPROVAL PROCESS

### Typical Timeline

**Scoping Meeting:** Week 0
**Data Collection:** Weeks 1-2
**Draft Study Preparation:** Weeks 3-6
**Draft Submittal:** Week 7
**Agency Review:** Weeks 8-11 (4 weeks typical)
**Response to Comments:** Weeks 12-13
**Final Submittal:** Week 14
**Final Approval:** Weeks 15-17 (3 weeks typical)

**Total Duration:** 4-5 months typical

### Common Review Comments

**Data Issues:**
- Counts during non-typical periods
- Missing turning movements
- Inconsistent volumes

**Methodology Issues:**
- Inappropriate trip generation
- Unsupported trip distribution
- Wrong analysis software/edition

**Analysis Issues:**
- Incorrect lane configurations
- Wrong signal timing
- Missing scenarios

**Mitigation Issues:**
- Inadequate improvements
- No cost estimates
- Unclear responsibility

### Addressing Comments

**Response Letter:**
```
RESPONSE TO REVIEW COMMENTS

Comment 1: Trip generation for Land Use Code 710 should use
           equation, not rate.

Response: Revised calculation on page 15 now uses ITE equation
          T = 0.54(X) + 78.81. Trips increase from 185 to 192.
          Analysis updated accordingly.

Comment 2: Queue analysis needed for Main St westbound left turn.

Response: Added queue analysis as Table 8 on page 28. 95th
          percentile queue = 145 ft. Recommend 200 ft turn bay.
          
[Continue for all comments]
```

**Revised Study:**
- Track changes or redline
- Update revision date
- Note all changes clearly
- Resubmit promptly

---

## STATE-SPECIFIC VARIATIONS

### Common Differences

**California:**
- CEQA environmental review
- VMT (Vehicle Miles Traveled) analysis
- Caltrans requirements for state highways
- Local agencies may use LOS or VMT

**Florida:**
- FDOT TIS procedures
- Concurrency requirements
- Proportionate share
- ARTPLAN analysis

**Pennsylvania:**
- PennDOT Pub. 46 requirements
- Highway Occupancy Permit (HOP) process
- MPC (Municipalities Planning Code) compliance
- Crash data sealed (not public)

**Texas:**
- TxDOT Access Management Manual
- Driveway permit process
- Traffic impact analysis (TIA) guidelines
- Regional mobility authorities

**Wisconsin:**
- WisDOT TIA Guidelines 2024
- Trans. 233 review process
- 100 peak hour trip threshold
- Regional office coordination

### Research State Requirements

**For Any State:**
1. Visit State DOT website
2. Search "Traffic Impact Study" or "TIA Guidelines"
3. Download latest manual
4. Review specific requirements
5. Contact regional office for scoping

**Key State DOT Links:**
- Caltrans: dot.ca.gov
- FDOT: fdot.gov
- PennDOT: penndot.pa.gov
- TxDOT: txdot.gov
- WisDOT: wisconsindot.gov

---

## TOOLKIT REQUIREMENTS

### Software Needs

**Essential:**
- Synchro/SimTraffic (capacity analysis)
- AutoCAD or similar (graphics)
- Excel (calculations, tables)
- Word (report writing)

**Helpful:**
- VISSIM (microsimulation)
- Google Earth Pro (aerial imagery)
- GIS software (mapping)

### Data Sources

**Traffic Counts:**
- Automated counters (purchase or rent)
- Video recording equipment
- Traffic count services (outsource)

**Background Data:**
- State DOT traffic count database
- MPO travel demand model
- Local comprehensive plans
- Census journey-to-work data

**Reference Materials:**
- ITE Trip Generation Manual (subscription)
- Highway Capacity Manual (purchase)
- MUTCD (free online)
- State DOT manuals (free download)

### Template Library

**Forms:**
- Scope approval form
- Traffic count field sheets
- Signal warrant worksheet
- Queue calculation sheet

**Report Sections:**
- Introduction boilerplate
- Methodology descriptions
- Standard figures
- Table templates

**Calculations:**
- Trip generation spreadsheet
- Trip distribution calculator
- Growth factor calculator
- Queue length formulas

---

## BEST PRACTICES

### Planning Ahead

- Start scoping early (before site plan finalized)
- Schedule counts in advance
- Allow time for weather delays
- Build in review time
- Coordinate with all jurisdictions

### Quality Control

- Peer review before submittal
- Check all calculations
- Verify data consistency
- Proofread carefully
- Validate software inputs/outputs

### Professional Conduct

- Licensed engineer required in most states
- Follow ethical guidelines
- Present objective analysis
- Disclose limitations
- Respond promptly to comments

---

## COST CONSIDERATIONS

### Typical Costs

**Small Study (< 5 intersections):**
- $8,000 - $15,000

**Medium Study (5-10 intersections):**
- $15,000 - $30,000

**Large Study (10+ intersections):**
- $30,000 - $75,000+

**Cost Drivers:**
- Number of intersections
- Analysis complexity
- Data collection scope
- Multiple scenarios
- Specialized analyses
- Revision iterations

### Developer Responsibility

**Typical Costs Borne by Developer:**
- TIS preparation
- Data collection
- Mitigation design
- Construction of improvements
- Fair share contribution (if multiple developers)

---

## CHECKLIST FOR TIS PREPARATION

### Pre-Study
- [ ] Determine if TIS required
- [ ] Contact all jurisdictions
- [ ] Schedule scoping meeting
- [ ] Obtain scope approval
- [ ] Secure qualified engineer

### Data Collection
- [ ] Schedule traffic counts
- [ ] Collect counts (proper conditions)
- [ ] Field verify geometry
- [ ] Obtain crash data
- [ ] Gather background data

### Analysis
- [ ] Calculate trip generation
- [ ] Develop trip distribution
- [ ] Assign trips to network
- [ ] Perform capacity analysis
- [ ] Assess impacts
- [ ] Develop mitigation

### Report Preparation
- [ ] Draft all sections
- [ ] Create figures/tables
- [ ] Include appendices
- [ ] Internal QC review
- [ ] Submit draft

### Approval Process
- [ ] Respond to comments
- [ ] Revise study
- [ ] Resubmit
- [ ] Obtain final approval
- [ ] Incorporate into permits

---

## GLOSSARY

**ADT:** Average Daily Traffic  
**HCM:** Highway Capacity Manual  
**ITE:** Institute of Transportation Engineers  
**LOS:** Level of Service  
**MPO:** Metropolitan Planning Organization  
**MUTCD:** Manual on Uniform Traffic Control Devices  
**PHF:** Peak Hour Factor  
**TDM:** Transportation Demand Management  
**TIS:** Traffic Impact Study  
**V/C:** Volume-to-Capacity Ratio  
**VMT:** Vehicle Miles Traveled  
**vph:** Vehicles per hour  

---

**END OF DOCUMENT**

**Implementation:** This guide provides foundation for building traffic study toolkit in Trajanus Hub. Next steps: Create automated forms, calculation templates, and report generation system.
