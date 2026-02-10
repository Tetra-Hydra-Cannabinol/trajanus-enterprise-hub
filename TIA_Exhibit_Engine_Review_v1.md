# TIA Exhibit Engine — Engineering Review
## Review Date: 2026-02-10
## Reviewers: Agent 1 (Architecture & Data Engineering), Agent 2 (PPTX Rendering & Feasibility), Agent 3 (Integration & Product)

---

### EXECUTIVE SUMMARY

The TIA Exhibit Engine specification is architecturally sound in its three-phase vision and correctly identifies the core value proposition: transforming TMC spreadsheet data into professional exhibit slides that currently take a senior PE hours to build by hand. The data flow from Steps 1-8 into exhibit generation is logical, and the TypeScript interface design provides a reasonable starting point. However, all three review agents identified significant gaps that must be addressed before committing code.

**The biggest risks are:** (1) The current TFE data model does not store per-movement turning counts from parsed TMC files — only metadata about the uploaded file is saved, meaning the exhibit engine has no turning movement data to render without re-parsing; (2) The spec's step numbering conflicts with the existing 10-step workflow where Step 9 is already "Report Assembly" and Step 10 is "Final Delivery"; (3) Several critical TIA scenario types (cumulative, improved/mitigated) are missing from the data model; and (4) The PowerPoint round-trip calibration approach is architecturally fragile and should be replaced with an in-app React canvas.

**Top recommendations:** Ship SVG-first/PPTX-second to get value to Tom faster. Embed exhibit generation as a sub-panel within the existing Step 9 rather than creating a new step. Enhance Step 2 to save parsed TMC data to localStorage. Use the standardized 4-sheet XLSX template designed by Agent 1. Adopt the in-app React canvas for calibration (Agent 2's decision). Target a realistic 3-week Phase 1 MVP that generates turning movement diagrams and volume tables — not full PPTX slide decks.

---

### ARCHITECTURE & DATA ENGINEERING (Agent 1)

#### Interface Review

**General Assessment:** The interfaces represent the core domain model for a TIA workflow. Based on review of the existing traffic toolkit and the Centurion codebase, the following issues and recommendations were identified:

**1. TMCDataset — Missing critical metadata fields:**
- Must include `countVendor: string` (e.g., "National Data & Surveying") — different vendors produce different raw formats
- Missing `seasonalAdjustmentFactor?: number` — many jurisdictions (especially ADOT) require seasonal adjustment of raw TMC counts
- Missing `weatherConditions: string` — required by many agencies to validate count acceptability
- `countDate` must be typed as `string` (ISO 8601 `YYYY-MM-DD`), NOT `Date`, to avoid timezone serialization issues

**2. IntersectionData — Structural concerns:**
- Must include `intNumber: number` (study intersection number, 1-based)
- Must include `controlType: 'signalized' | 'unsignalized' | 'roundabout' | 'stop_controlled'`
- Must include `jurisdiction: string`
- **Critical missing field:** `isDriveway: boolean` — the existing toolkit treats driveways and intersections differently. Site driveways have different exhibit requirements (typically no existing counts, only projected volumes)

**3. ApproachData — Direction enum is incomplete:**
```typescript
type ApproachDirection = 'NB' | 'SB' | 'EB' | 'WB' | 'NEB' | 'NWB' | 'SEB' | 'SWB';
```
- Standard 4-way uses NB/SB/EB/WB but angled intersections (common in Phoenix metro grid deviations) require 8-point variants
- Must include `streetName: string` — "NB" must mean "Northbound on Scottsdale Rd"

**4. MovementData — Type safety gaps:**
- `uturn` movement is missing but required for Synchro models
- `volumes` should be `Record<TimePeriod, number>` where `TimePeriod` is a proper enum, preventing "am" vs "AM" vs "a.m." inconsistencies
- **Critical: Missing PHF (Peak Hour Factor) per movement.** Synchro requires PHF. If TMC gives 15-minute intervals, PHF = `V / (4 * V15_max)`. Raw 15-minute sub-counts need a place in the data model

**5. DrivewayData — Should extend IntersectionData:**
```typescript
interface DrivewayData extends Omit<IntersectionData, 'approaches'> {
  isDriveway: true;
  accessType: 'full' | 'right_in_right_out' | 'left_in_left_out' | 'right_in_only' | 'right_out_only';
  projectedApproaches: ApproachData[];
}
```

**6. ScenarioYear — Missing scenario types:**
```typescript
type ScenarioType =
  | 'existing'
  | 'background_opening'
  | 'background_horizon'
  | 'total_opening'
  | 'total_horizon'
  | 'cumulative_opening'    // MISSING — includes other approved projects
  | 'cumulative_horizon';   // MISSING
```
- Many Arizona TIAs require "Cumulative" scenarios (includes trips from other approved but unbuilt developments)
- "Improved/Mitigated" scenarios also missing — needed post-capacity-analysis

**7. TripGeneration — Missing pass-by/diverted trip adjustments:**
```typescript
interface TripGeneration {
  // ... existing fields ...
  passByReduction?: number;      // Percentage (0-100)
  divertedReduction?: number;
  internalCapture?: number;
  netNewAmIn?: number;           // After reductions
  netNewAmOut?: number;
  netNewPmIn?: number;
  netNewPmOut?: number;
  source: string;                // "ITE 11th Edition" or "Local study"
}
```
- The gross-to-net reduction chain is the most scrutinized calculation in any TIA and must be modeled explicitly

**8. ExhibitSlide — Should use discriminated union by exhibit type:**
```typescript
type ExhibitSlide =
  | VolumeExhibit
  | LOSExhibit
  | TripGenExhibit
  | DistributionExhibit
  | GeometryExhibit;
```

**9. TimePeriod — Must be a proper enum:**
```typescript
enum TimePeriod {
  AM = 'AM',
  MD = 'MD',
  PM = 'PM',
  SAT = 'SAT',
  DAILY = 'DAILY'
}
```

#### Data Flow Assessment

**1. Critical flow dependency issues:**

**a. Missing automated TMC-to-existing-volumes link:** Parsed TMC data (Step 2) should directly populate `IntersectionData.approaches[].movements[].volumes` for the existing scenario. Currently this appears to be manual re-entry.

**b. Race condition in Step 5:** The "Total Future" scenario requires BOTH background volumes AND site trips. If the user changes trip generation after computing future volumes, scenario data becomes stale. The spec must enforce **reactive recomputation** — any upstream change invalidates and recomputes downstream scenarios.

**c. Partial generation behavior undefined:** If capacity analysis (LOS) is not complete, exhibit generation should still proceed for volume exhibits but block LOS exhibit generation. The spec should define partial-generation behavior.

**d. Missing reverse flow:** Capacity analysis often reveals mitigations needed (e.g., adding a turn lane), which changes lane geometry, which changes exhibits, which changes the Synchro model. The data flow must accommodate iterative refinement.

**e. Circular dependency risk:** Trip Distribution (Step 4) determines which intersections receive site traffic, but the intersection list (Step 1/2) determines available distribution routes. Late-addition intersections need a global registry with downstream cascade notifications.

**2. Data persistence recommendation:** Tauri file system with JSON project files. Each TIA project is a `.tia.json` file containing the full `TMCDataset` + scenario data + exhibit configuration.

#### Standardized TMC Template Proposal

**Template Name:** `Trajanus_TMC_Template_v1.xlsx`

**SHEET 1: "Project Info"**

| Row | Column A (Label) | Column B (Value) | Notes |
|-----|-------------------|-------------------|-------|
| 1 | **TRAJANUS TMC DATA TEMPLATE** | v1.0 | DO NOT MODIFY (parser signature) |
| 3 | Project Name | *(user enters)* | Required |
| 4 | Project Number | *(user enters)* | e.g., "TRA-2026-042" |
| 5 | Count Date | *(user enters)* | Format: YYYY-MM-DD |
| 6 | Day of Week | *(auto or user)* | Must be Tue/Wed/Thu per ADOT |
| 7 | Count Vendor | *(user enters)* | e.g., "National Data & Surveying" |
| 8 | Weather Conditions | *(user enters)* | e.g., "Clear, 85F" |
| 10 | AM Peak Start | *(user enters)* | HH:MM 24hr, e.g., 07:00 |
| 11 | AM Peak End | *(user enters)* | HH:MM, e.g., 09:00 |
| 12 | PM Peak Start | *(user enters)* | HH:MM, e.g., 16:00 |
| 13 | PM Peak End | *(user enters)* | HH:MM, e.g., 18:00 |
| 14 | MD Peak Start | *(optional)* | e.g., 11:00 |
| 15 | MD Peak End | *(optional)* | e.g., 13:00 |
| 19 | Number of Intersections | *(integer)* | Must match Sheet 2 |
| 20 | Number of Driveways | *(integer)* | 0 if none counted |
| 21 | Seasonal Adjustment Factor | *(optional, default 1.00)* | 0.50 - 1.50 |

**Validation Rules:** Row 1/A1 must contain exact template signature. Count date not future, not >2 years old. Day of week must match date. Time fields HH:MM 24hr. AM start < AM end. PM start < PM end.

**SHEET 2: "Intersections"**

| Column | Header | Type | Required | Validation |
|--------|--------|------|----------|------------|
| A | Int # | Integer | Yes | Sequential 1-N, unique |
| B | Intersection Name | Text | Yes | e.g., "Scottsdale Rd & Shea Blvd" |
| C | Type | Text | Yes | "Signalized", "Unsignalized", "Roundabout", "Stop-Controlled", "Driveway" |
| D | Jurisdiction | Text | Yes | e.g., "City of Scottsdale" |
| E | NS Street | Text | Yes | North-South street name |
| F | EW Street | Text | Yes | East-West street name |
| G | Latitude | Decimal | No | -90 to 90 |
| H | Longitude | Decimal | No | -180 to 180 |
| I | Approaches | Text | Yes | Comma-separated: "NB,SB,EB,WB" |
| J | Notes | Text | No | Free text |

**SHEET 3: "TMC Counts" (Core Data Sheet)**

One row per intersection per approach per movement per 15-minute interval.

| Column | Header | Type | Required | Validation |
|--------|--------|------|----------|------------|
| A | Int # | Integer | Yes | Must match Sheet 2 |
| B | Period | Text | Yes | "AM", "PM", "MD", "SAT" |
| C | Time | Text | Yes | 15-min interval start HH:MM |
| D | Approach | Text | Yes | "NB", "SB", "EB", "WB" |
| E | Left | Integer | Yes | >= 0 |
| F | Through | Integer | Yes | >= 0 |
| G | Right | Integer | Yes | >= 0 |
| H | U-Turn | Integer | No | >= 0, defaults to 0 |
| I | Peds | Integer | No | >= 0 |
| J | Bikes | Integer | No | >= 0 |
| K | Heavy Vehicles | Integer | No | >= 0 |

**Row count formula:** Per intersection: 4 approaches x 8 intervals (2hr/15min) x 2 periods = 64 rows. For 5 intersections: 320 rows. Manageable for Tom.

**SHEET 4: "Peak Hour Summary" (Optional convenience sheet)**

| Column | Header | Type | Required |
|--------|--------|------|----------|
| A | Int # | Integer | Yes |
| B | Period | Text | Yes |
| C | Peak Hour Start | Text | Yes |
| D | Approach | Text | Yes |
| E | Left | Integer | Yes |
| F | Through | Integer | Yes |
| G | Right | Integer | Yes |
| H | U-Turn | Integer | No |
| I | Total | Integer | Yes |
| J | PHF | Decimal | Yes (0.50-1.00) |

If present, parser cross-validates against computed peak hour from Sheet 3. Mismatch = WARNING (not error).

**Parser Output:**
```typescript
interface ParseResult {
  success: boolean;
  dataset?: TMCDataset;
  errors: ParseError[];     // Fatal: file rejected
  warnings: ParseWarning[]; // Non-fatal: data accepted with caveats
}
```

**Tom-Friendliness:** Template ships with example data pre-filled. Frozen header rows. Data validation dropdowns for Period, Approach, Type columns. Red conditional formatting for invalid cells. README instruction row (parser ignores rows where Col A is empty or starts with "#").

#### Scenario Engine Validation

**1. Growth Factor — Floating point precision issue:**
- `Math.pow(1.02, 5)` = 1.1040808032...
- Applied to 500 vehicles: 552.04. Round to 552 or 553?
- **Rule required:** "All intermediate volume calculations retain full floating-point precision. Rounding to integer occurs ONLY when producing final exhibit values."

**2. Missing growth rate source documentation:** Add `growthRateSource: string` field.

**3. Missing scenario types:**

| Scenario | Status | Notes |
|----------|--------|-------|
| Existing | Covered | |
| Background Opening/Horizon | Covered | |
| Background + Project Opening/Horizon | Covered | |
| Cumulative Opening/Horizon | **MISSING** | Required when other approved projects nearby |
| Improved/Mitigated | **MISSING** | Needed post-capacity-analysis |

**4. Site trip assignment must be per-movement, not per-approach:**
```typescript
interface SiteTripAssignment {
  intersectionId: string;
  approach: ApproachDirection;
  turn: 'left' | 'through' | 'right' | 'uturn';
  period: TimePeriod;
  inboundTrips: number;
  outboundTrips: number;
  totalAdded: number;
}
```

**5. Rounding reconciliation required:** After applying growth factors and distributing trips, individual movement volumes may not sum to approach/intersection totals. **Use the "largest remainder method"** (Hamilton's method): compute all fractional values, floor them, distribute remaining deficit to movements with largest fractional remainders.

#### Recommendations

1. Add `countVendor`, `seasonalAdjustmentFactor`, and `weatherConditions` to `TMCDataset`
2. Add `isDriveway` boolean and `accessType` to `IntersectionData`
3. Expand `ApproachDirection` to include diagonal directions (NEB, NWB, SEB, SWB)
4. Add `uturn` to movement turn type enum
5. Add `PHF` (Peak Hour Factor) as computed field on `MovementData`
6. Add pass-by/diverted/internal capture fields to `TripGeneration`
7. Add `cumulative` and `improved` scenario types
8. Define `SiteTripAssignment` interface for per-movement, per-intersection site trip mapping
9. Adopt the 4-sheet XLSX template as specified
10. Implement "largest remainder method" for rounding reconciliation
11. Specify full floating-point precision for intermediate computations
12. Add `growthRateSource: string` to scenario configuration
13. Implement reactive recomputation when upstream data changes
14. Define partial exhibit generation behavior for incomplete data
15. Use Tauri file system with `.tia.json` project files for persistence
16. Add `CumulativeProject` interface for modeling other approved developments
17. Use discriminated union typing for `ExhibitSlide` by exhibit type
18. Define `TimePeriod` as a proper TypeScript enum
19. Validate TMC template intersection count matches actual data rows
20. Ship template XLSX with frozen headers, dropdowns, conditional formatting, and example data

---

### PPTX RENDERING & FEASIBILITY (Agent 2)

#### Component Feasibility Matrix

| Component | Feasible? | pptxgenjs Approach | Limitations |
|---|---|---|---|
| **TMC Data Grid** | YES | `slide.addTable()` with `colspan/rowspan`, per-cell styling | Tables **cannot be rotated**. `colW` ignored with `colspan` (Issue #764). Text `rotate` in cells doesn't work (Issue #755). For Phase 3 bearing-matched: tables cannot be used directly |
| **Direction Arrow** | YES | `slide.addShape(pptx.shapes.RIGHT_ARROW, { fill, rotate })` | Straightforward. Fill, line, shadow all supported |
| **Turn Arrow** | YES (with caveats) | `curvedLeftArrow`, `curvedRightArrow`, `uturnArrow` ShapeType presets | Arc radius/arm width NOT parameterizable. If exact geometry matters, use pre-rendered PNG/SVG images |
| **Volume Label** | YES | `slide.addText()` with fill, color, fontSize | Fully supported including transparency |
| **Percentage Label** | YES | Same as Volume Label with yellow fill | No issues |
| **Trip Gen Box** | YES | `slide.addText()` with fill, shadow (outer), rectRadius | Shadow fully supported. Multi-line mixed formatting via text array |
| **Landmark Label** | YES | `slide.addText()` with fill, border | Trivial |
| **Legend Box** | PARTIAL | Must compose from multiple overlapping `addText()` + `addShape()` calls | No `addGroup()` API. Each element independently positioned. Consider pre-rendered image |
| **LOS Result** | YES | `slide.addText()` with solid color fill | **No gradient fill support** (Issue #102, open since 2017). Solid color-coded cells work. If gradient needed: pre-rendered images |
| **North Compass** | IMAGE ONLY | `slide.addImage({ data: base64, rotate })` | No compass preset. Pre-render as PNG. Rotation supported |
| **Title Bar** | YES | `slide.addText()` with full-width, fill, bold | Percentage-based width supported |
| **Car Icon** | IMAGE ONLY | `slide.addImage({ data: base64, rotate })` | Must be pre-rendered asset. Rotation supported |

**Summary:** 10/12 directly feasible. 2 require pre-rendered images (North Compass, Car Icon). Legend Box requires manual sub-element positioning. No showstoppers for Phase 1.

#### Calibration Approach Recommendation

**DECISION: Option B — In-App React Canvas**

##### Option A Analysis: PowerPoint Round-Trip

| Factor | Assessment |
|--------|------------|
| altText availability | Only on images in pptxgenjs, NOT shapes/text. Limits tagging strategy |
| Read-back capability | pptxgenjs is write-only. Requires JSZip + raw XML parsing — doubles tech surface |
| Round-trip XML fidelity | PowerPoint may rewrite/strip attributes. `cNvPr name` generally preserved but auto-renamed during copy-paste |
| EMU precision | Non-integer EMU values can cause file corruption (Discussion #1216) |
| User experience | High friction: generate -> open PPT -> drag 15-30 elements -> save -> re-import -> verify |
| Live preview | None. No feedback until round-trip complete |
| Format dependency | Ties calibration permanently to PowerPoint |

**Verdict on Option A:** Technically possible but architecturally fragile, user-hostile, and creates a write-only/read-back split.

##### Option B Analysis: In-App React Canvas

| Factor | Assessment |
|--------|------------|
| Single environment | Everything in Centurion, no external tool dependency |
| Live preview | WYSIWYG — user sees final result as they drag |
| Feedback loop | Instant: drag, see result, adjust |
| Data model | Clean typed JSON, no XML/EMU parsing |
| Tech alignment | React + Tauri already the stack. `react-rnd` for drag/resize |
| Phase 2/3 extensibility | Canvas becomes primary authoring surface for approach bearings, geometry |
| Persistence | Trivial JSON save/load |

**Cons:** More upfront dev (2-3 sprints for polished implementation). Aerial photo pan/zoom adds complexity (solved by `react-zoom-pan-pinch`).

**RECOMMENDATION:** Implement Option B. Superior UX, cleaner architecture, no round-trip fragility, natural Phase 2/3 extensibility. The upfront cost is justified.

**Implementation guidance:**
- `react-rnd` for draggable + resizable component placeholders
- `react-zoom-pan-pinch` for aerial photo pan/zoom
- Calibration profiles stored as typed JSON
- Component previews as styled `<div>` elements matching PPTX output
- Snapping guides for alignment accuracy
- "Preview PPTX" button for verification

#### Technical Risks

**1. Embedded Aerial Photos — File Size (MEDIUM risk)**
- 5000x4000 aerial: 15-40 MB PNG, 2-5 MB JPEG
- Single slide with hi-res aerial + 20 components: 10-20 MB PPTX
- **Mitigation:** Pre-compress to JPEG 85%. Use `sizing: 'cover'` to crop. "Draft" vs "Final" quality setting. Recommended: 150 DPI at final print size (2250x1500 px for 11x17)

**2. Table Rotation for Phase 3 (HIGH risk)**
- pptxgenjs tables cannot be rotated. `rotate` not available on `TableProps`
- **Alternatives:**
  1. Pre-render table as HTML -> PNG via `html2canvas`, embed as rotated image (loses text selectability but preserves visual fidelity) — **RECOMMENDED**
  2. Compose from individual rotated `addText()` calls (maintains selectability but extremely tedious)
  3. Switch to python-pptx server-side (supports grouped shape rotation)

**3. EMU Precision (LOW risk)**
- pptxgenjs handles inch-to-EMU conversion. Only an issue for position read-back (Option A, not recommended)
- **Mitigation:** Round all positions to 4 decimal inches. Utility: `toEMU(inches) = Math.round(inches * 914400)`

**4. Semi-Transparent Overlays (LOW risk)**
- Directly supported: `fill: { color: '000000', transparency: 50 }`

**5. Drop Shadows (LOW risk)**
- Outer shadows work correctly. Known bug with `type: 'inner'` (Issue #1293) — use outer only

**6. Gradient Fills for LOS (LOW practical risk)**
- Not supported (Issue #102, open since 2017). Solid color-coded cells (Green=A, Red=F) work and match professional standards. If gradients explicitly required, pre-render as PNG images.

#### Tech Stack Assessment

**pptxgenjs — CONFIRMED.** Covers all Phase 1-2 requirements. Active maintenance, TypeScript defs included, JSZip as sole dependency. Limitations (no gradients, no table rotation, no shape grouping) have documented workarounds.

**SheetJS — CONFIRMED.** Reads .xlsx/.xls/.csv client-side. TypeScript support.

**python-pptx — NOT recommended for Phase 1-2.** Objectively more capable (read+write, gradients, table rotation, grouping) but requires Python runtime, IPC bridge, server infrastructure. Architectural benefit of staying in single TypeScript runtime is significant for Tauri desktop app.

**Phase 3 contingency:** Hybrid approach — pptxgenjs for 90% generation, JSZip post-processing of PPTX ZIP to inject raw OOXML for features pptxgenjs cannot handle.

**Geo-Computation Libraries (Phase 3):**

| Library | Use Case | Recommendation |
|---|---|---|
| **Turf.js** | Bearing, distance, point-in-polygon | PRIMARY — `turf.bearing()` returns degrees from north |
| **Proj4js** | Coordinate system transformation | SECONDARY — needed if input uses state plane coords |
| **math.js** | Matrix operations for affine transforms | OPTIONAL — native `Math` sufficient for simple 2D |

#### Recommendations

1. Adopt Option B (In-App React Canvas) for calibration
2. Confirm pptxgenjs as PPTX generation library; do NOT introduce python-pptx unless Phase 3 reveals hard blockers
3. Pre-render North Compass, Car Icon, and Legend Box as image assets
4. Plan HTML-to-image approach for Phase 3 table rotation
5. Add `toSafeEMU()` utility function from day one
6. Define standard aerial photo pipeline: JPEG preferred, 3000px max for draft, 85% quality, resize at import
7. Implement PPTX post-processing via JSZip for injecting `descr` (alt-text) attributes on all shapes
8. Use solid color fills for LOS indicators — do not attempt gradients
9. Add Turf.js and Proj4js to Phase 3 dependency plan only
10. Build React canvas calibration as reusable `<ExhibitCanvas />` module
11. Use `react-rnd` for canvas component placeholders
12. Create coordinate mapping layer: `canvasToSlide(canvasPx, config) -> {x: inches, y: inches}`
13. Only use `type: 'outer'` shadows — add lint rule preventing inner shadows
14. Validate curved arrow shapes early in Phase 1 week 1 — if they don't match traffic engineering conventions, switch to pre-rendered images

---

### INTEGRATION & PRODUCT (Agent 3)

#### TFE Workflow Integration

**The Step Numbering Problem:** The spec calls the exhibit engine "Step 9," but the existing workflow already has:
- Step 9: Report Assembly (`tfe_step9_data`)
- Step 10: Final Delivery (`tfe_step10_data`)

**Three viable placements:**

| Option | Description | Verdict |
|--------|-------------|---------|
| Sub-feature of Step 9 | Embed in existing Report Assembly panel | **RECOMMENDED** |
| Step 9.5 | Insert between 9 and 10 | Bad — breaks folder tracker, dependency map, CSS/JS |
| Toolbar action | Persistent button accessible from any step | Premature for MVP |

**Recommendation:** Build exhibit generation as a major sub-panel within the existing Step 9: Report Assembly. The "Generate Exhibits" button replaces the manual "Add Exhibit" workflow. The exhibits table auto-populates with generated items. This avoids breaking the 10-step workflow, localStorage keys, and folder tracker.

**Critical Data Gap:** The current data model stores volumes at the *direction* level (NB/SB/EB/WB) with single AM/PM values. It does NOT store per-movement turning counts (left, through, right) from parsed TMC files. The TMC file is uploaded and validated in Step 2 but its parsed turning movement data is never saved to localStorage.

**Fix required:** Enhance Step 2 to save parsed TMC data to `tfe_step2_tmc_parsed` localStorage key with per-intersection, per-approach, per-movement, per-period turning counts.

**Data consumed by the Exhibit Engine:**

| localStorage Key | Exhibit Engine Uses |
|---|---|
| `tfe_active_project` | Title block, header/footer, study parameters |
| `tfe_step2_data` + `tfe_step2_tmc_parsed` (NEW) | Count date labels, turning movement volumes |
| `tfe_step3_data` | Trip generation summary exhibit |
| `tfe_step4_data` | Trip distribution diagram, directional splits |
| `tfe_step5_data` | Existing volumes, future volume scenarios |
| `tfe_step6_data` | LOS summary table exhibits |
| `tfe_step7_data` | Site access exhibits |
| `tfe_step8_data` | Signal warrant exhibits |

#### MVP Definition

**The "Tom's Tuesday" Test:** Tom needs to produce a TIA report every few weeks. Highest-pain-point tasks: (1) manually drawing turning movement count diagrams in PowerPoint (2-4 hours per intersection), (2) manually creating volume scenario exhibits, (3) ensuring numbers are consistent across exhibits.

**MVP (Ship in 2-3 weeks):**

| # | Feature | Time Estimate |
|---|---------|---------------|
| 1 | TMC Parser — parse standardized template into structured data, save to `tfe_step2_tmc_parsed` | 2-3 days |
| 2 | Intersection data model — TypeScript interfaces | 2-3 days |
| 3 | Single Intersection Turning Movement Diagram — SVG with L/T/R arrows + volume labels for AM/PM | 3-5 days |
| 4 | Scenario Volume Table — auto-generated HTML table (Existing / Background / Background+Site) | 2-3 days |
| 5 | Step 9 integration — "Generate Exhibits" button populates exhibits table | 1-2 days |

**What Waits for v2:**
- PPTX generation (use copy/paste or screenshot for now)
- Calibration UI
- Multi-intersection batch generation
- Grid rotation / bearing matching
- Branded templates with firm logo
- PDF export
- Roundabout / 5-leg / non-standard geometries
- Supabase cloud storage
- Version control / audit trail

**What Waits for v3:**
- Full PPTX slide deck generation with template system
- White-label configuration for other firms
- API-based TMC vendor integrations
- Capacity analysis integration (reading .syn files)

**Rationale:** The turning movement diagram is the single most time-consuming exhibit. Auto-generating one correct intersection diagram from parsed TMC data saves Tom 30-60 minutes per intersection. With 4-6 intersections per project, that is 2-6 hours saved on day one. PPTX generation is polish — Tom can screenshot the SVG into his existing PowerPoint template.

#### Edge Cases & Limitations

| Edge Case | Handling | Phase |
|---|---|---|
| **5-leg intersections** | Defer. Display warning: "5+ legs require manual exhibit." Store data, skip diagram | v2 |
| **Roundabouts** | Defer. Fundamentally different geometry (circular flow, entry/circulating/exit). Tom does these in CAD | v2 |
| **T-intersections (3-leg)** | Support in MVP. 4-leg with one arm removed. Renderer detects 3 active approaches | MVP |
| **Multiple driveways same approach** | List in table, don't render on single diagram. Show as separate mini-diagrams | v2 |
| **One-way streets** | Support. One-way approach has movements in only one direction. Show one-way arrow indicator | MVP |
| **Split-phase signal timing** | Not relevant to volume exhibits. Affects capacity only (Step 6) | N/A |
| **U-turns** | Defer diagram arrow. Lump into left turn count with footnote in MVP | v2 |
| **Pedestrian movements** | Defer. Separate TMC category. Appears in capacity inputs, not volume diagrams | v2 |
| **Right-turn overlap** | Signal timing concept. No exhibit engine work needed | N/A |
| **Incomplete TMC data** | Generate available exhibits, flag missing data. "N/A" for missing periods, never show zeros for missing data | MVP |

#### Open Question Responses

**Q1: TMC Parser Strategy — DECIDED.** Confirmed: standardized template. See Agent 1's 4-sheet XLSX template proposal.

**Q2: Calibration UI.** Product perspective: Defer calibration UI to v2. For MVP, Tom generates exhibit, verifies visually, fixes CSV if wrong. Agent 2's in-app canvas recommendation is correct for v2.

**Q3: Grid Rotation.** **Cardinal-only for MVP and likely permanently.** North-up is how 90%+ of TIA exhibits are oriented and matches NB/SB/EB/WB labeling. Bearing-matched rotation adds complexity with minimal value. For v2, offer optional rotation field per intersection.

**Q4: Data Storage.** **localStorage only for MVP. Supabase for v4.** Tom works on one project at a time on one machine. No collaboration requirement. localStorage handles 5-10MB per origin — a TIA project is <500KB. Adding Supabase now means building auth, sync, conflict resolution, offline handling before the core feature works.

**Q5: PPTX Generation Location.** **Defer PPTX to v2. For MVP: SVG/HTML exhibits.** For v2: JavaScript assembles exhibit data, Tauri command uses pptxgenjs, Tauri file dialog saves. Do NOT touch Rust files per CLAUDE.md protocol — use `@tauri-apps/plugin-dialog` and `@tauri-apps/plugin-fs` APIs. Do NOT build a CLI tool — Tom is not a command-line user.

**Q6: Midday Counts.** **Yes, configurable but default to AM/PM.** Step 2 already stores AM/PM time ranges. "Midday" toggle adds third period. TMC template has optional MD columns. 30-minute addition to parser.

**Q7: Multiple Intersections.** Per-intersection generation, assembled in sequence. Figure naming: `Figure {category + intersection_index * exhibits_per + type_index}`. Design numbering system now even if MVP is single-intersection.

**Q8: Capacity Analysis Integration.** **Generate incrementally.** Generate whatever exhibits are possible with current data. If Steps 1-5 done but Step 6 not: generate volume exhibits, skip LOS. Show: "4 of 8 exhibit types generated. Complete Step 6 for remaining." Matches Tom's actual workflow — he drafts volume exhibits while waiting for Synchro results.

**Q9: Version Control.** **Timestamps for MVP.** Each `tfe_step*_data` object includes `savedAt` ISO timestamp and auto-incrementing `version` integer. When exhibits are generated, record source versions. Detect stale exhibits: "Warning: Step 5 data updated since exhibits generated. Regenerate?"

**Q10: Export Formats.** **HTML only for MVP** with browser print-to-PDF (Ctrl+P in Tauri webview). PPTX for v2. Branded PDF with TOC and page numbering for v3.

#### Reusability Assessment

| Component | Universal | Firm-Specific |
|---|---|---|
| TMC parser | Yes | Column mapping might vary |
| Intersection data model | Yes | No |
| TMC diagram renderer | Yes | Arrow styling, colors, fonts |
| Volume scenario computation | Yes | No |
| LOS summary table | Mostly yes | Column headers, thresholds |
| ITE trip rates | Yes (industry standard) | Custom rates for non-ITE |
| Branding | No | Completely firm-specific |
| PPTX template | No | Slide master, fonts, colors |
| Jurisdiction dropdown | Partially | Arizona-centric currently |

**What a different TE firm changes:** (1) `config/branding.json` — logo, name, colors, fonts; (2) PPTX slide master template; (3) Jurisdiction list; (4) ITE trip rate table; (5) Default exhibit list. These configs must be extracted in Phase 1, not Phase 3 — otherwise firm-specific values get baked into generation code.

**The monolith problem:** `traffic.html` is already 421KB+. Adding the exhibit engine (SVG renderer, TMC parser, PPTX builder) will push past 600KB. Phase 1 should introduce the exhibit engine as a separate JS module loaded via `<script>` tag.

#### Phase Timeline Reality Check

| Phase | Spec Estimate | Realistic Estimate | Ship Date |
|---|---|---|---|
| Phase 1: TMC parser, SVG diagram, volume table, Step 9 integration | 2-3 weeks | **3 weeks** | Early March 2026 |
| Phase 2: Multi-intersection, PPTX generation | 2-3 weeks | **4 weeks** (PPTX library integration is 1-2 weeks alone) | Early April 2026 |
| Phase 3: Calibration UI, white-label config | 4-6 weeks | **3 weeks** (if config extraction done in Phase 1) | Late April 2026 |
| Phase 4: Supabase, auth, sync | Not in spec | **4 weeks** | Late May 2026 |

**Key risk:** The SVG intersection renderer is the Phase 1 time sink. Professional-looking turning movement diagrams with clean arrows, proper positioning, overlap avoidance — budget 5+ days minimum.

**Blocking dependency:** Step 2 must be enhanced to save parsed TMC data before anything else works. This is prerequisite work, not new feature work.

#### Recommendations

1. Do NOT create a new step — embed in existing Step 9: Report Assembly
2. Enhance Step 2 to save parsed TMC data to `tfe_step2_tmc_parsed`
3. Ship SVG-first, PPTX-second — gets value to Tom faster
4. Define and bundle TMC template immediately — Tom needs it day one of Phase 1
5. Support 3-leg and 4-leg intersections in MVP — T-intersections are 20-30% of projects
6. Use cardinal-only orientation (North up) for all diagrams
7. Store data in localStorage only for MVP — no Supabase until Phase 4
8. Extract branding config in Phase 1, not Phase 3 — `config/branding.json` from the start
9. Add `savedAt` timestamps and `version` counters to every step's localStorage data now
10. Handle incomplete data gracefully — partial exhibit generation with clear warnings
11. Do not touch Rust files — use Tauri JS APIs for file operations
12. Budget 5+ days for the SVG intersection renderer
13. Defer calibration UI entirely for MVP
14. Make time periods configurable but default to AM/PM
15. Introduce exhibit engine as separate JS module — don't add to 421KB monolith
16. Design figure numbering system now even for single-intersection MVP
17. The Centurion React app and TFE toolkit are separate codebases — don't attempt cross-app integration in Phase 1

---

### CONSOLIDATED ACTION ITEMS

Prioritized list of all recommended changes/additions to the spec:

**P0 — Must Fix Before Coding:**

1. **Resolve step numbering conflict.** Embed exhibit generation in existing Step 9: Report Assembly, not as a new step. (Agent 3)
2. **Enhance Step 2 to save parsed TMC data** to `tfe_step2_tmc_parsed` localStorage key with per-movement turning counts. Without this, the exhibit engine has no core data. (Agent 3)
3. **Adopt the standardized 4-sheet TMC XLSX template** designed by Agent 1. Ship with example data, frozen headers, dropdowns, and conditional formatting. (Agent 1)
4. **Add missing scenario types** to ScenarioYear: `cumulative_opening`, `cumulative_horizon`, `improved`. (Agent 1)
5. **Add missing interface fields:** `countVendor`, `seasonalAdjustmentFactor`, `weatherConditions` on TMCDataset; `isDriveway`, `controlType`, `jurisdiction` on IntersectionData; `passByReduction`, `internalCapture`, `netNew*` on TripGeneration. (Agent 1)
6. **Define `SiteTripAssignment` interface** for per-movement, per-intersection site trip distribution. (Agent 1)

**P1 — Architecture Decisions (Decided by Review):**

7. **Calibration: Use in-app React canvas (Option B).** Do not pursue PowerPoint round-trip. (Agent 2 — DECISION)
8. **Grid orientation: Cardinal-only (North up).** No bearing-matched rotation in any near-term phase. (Agent 3)
9. **PPTX generation: Defer to v2.** Ship SVG/HTML exhibits for MVP. (Agent 3)
10. **Data storage: localStorage only for MVP.** Supabase deferred to Phase 4. (Agent 3)
11. **Tech stack confirmed:** TypeScript + pptxgenjs + SheetJS. No python-pptx. (Agent 2)

**P2 — Engineering Requirements:**

12. **Implement "largest remainder method"** for rounding reconciliation in scenario computations. (Agent 1)
13. **Specify full floating-point precision** for intermediate calculations, integer rounding only at final output. (Agent 1)
14. **Define partial exhibit generation behavior** — generate available exhibits when upstream data incomplete. (Agents 1, 3)
15. **Implement reactive recomputation** — upstream data changes invalidate downstream scenarios. (Agent 1)
16. **Pre-render image assets:** North Compass, Car Icon, (optionally) Legend Box as base64 PNGs. (Agent 2)
17. **Add `toSafeEMU()` utility** and coordinate mapping layer from day one. (Agent 2)
18. **Define aerial photo pipeline:** JPEG 85%, 3000px max draft, resize at import. (Agent 2)
19. **Add `savedAt` and `version` fields** to every step's localStorage data object. (Agent 3)
20. **Introduce exhibit engine as separate JS module** — do not add to traffic.html monolith. (Agent 3)

**P3 — Phase 1 MVP Scope Definition:**

21. **MVP features:** TMC parser, single intersection SVG diagram (3-leg + 4-leg), scenario volume HTML table, Step 9 "Generate Exhibits" button. (Agent 3)
22. **MVP deferred:** PPTX generation, calibration UI, multi-intersection batch, grid rotation, roundabouts, 5-leg, Supabase, PDF export. (Agent 3)
23. **Extract branding config** (`config/branding.json`) in Phase 1, not Phase 3. (Agent 3)
24. **Budget 5+ days for SVG renderer** — this is the visual centerpiece. (Agent 3)
25. **Design figure numbering convention now** even for single-intersection MVP. (Agent 3)

**P4 — Phase 2-3 Planning:**

26. **Phase 3 table rotation:** Use HTML-to-image approach (html2canvas -> rotated PNG). (Agent 2)
27. **Phase 3 geo-computation:** Turf.js (primary), Proj4js (secondary). Do not install until Phase 3. (Agent 2)
28. **Phase 2 PPTX post-processing:** JSZip to inject alt-text `descr` attributes on all shapes. (Agent 2)
29. **Build React canvas calibration as reusable `<ExhibitCanvas />` module** for Phase 2. (Agent 2)
30. **Validate curved arrow shapes** in Phase 1 week 1 spike — switch to images if they don't match TE conventions. (Agent 2)

**P5 — Data Model Enhancements:**

31. **Use `TimePeriod` enum** instead of scattered string literals. (Agent 1)
32. **Use discriminated union** for `ExhibitSlide` by exhibit type. (Agent 1)
33. **Add `CumulativeProject` interface** for modeling other approved developments. (Agent 1)
34. **Add `growthRateSource` field** to scenario configuration. (Agent 1)
35. **Expand `ApproachDirection`** to include diagonal directions. (Agent 1)

---

*End of Engineering Review. Ready for Bill's disposition.*
