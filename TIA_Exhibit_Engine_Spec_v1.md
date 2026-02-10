# TIA EXHIBIT AUTOMATION ENGINE
## Engineering Specification v1.0
### Trajanus USA — ENGINEERED INTELLIGENCE™

**Document ID:** TFE-EXHIBIT-ENGINE-SPEC-001
**Date:** 2026-02-10
**Author:** Jake (Claude Opus) — Architecture & Design
**Review Required:** CC (Claude Code) Agent Team
**Status:** DRAFT — Pending Agent Review

---

## 1. EXECUTIVE SUMMARY

### What This Is
An automated system that transforms TMC (Turning Movement Count) spreadsheet data into professional Traffic Impact Analysis (TIA) exhibit slides — the kind Tom Chlebanowski currently builds by hand, one intersection at a time, taking hours per study.

### What Makes It Unique
Every other traffic engineering tool stops at data tables. This system generates **visual exhibits** — aerial photos with correctly positioned TMC data grids, directional arrows, landmark labels, trip generation summaries, and capacity analysis results overlaid on real intersection geometry. The output looks like a senior PE spent hours in PowerPoint. The input is a spreadsheet.

### The Three-Phase Vision
- **Phase 1 (NOW):** Component Library + Calibration Capture — manual positioning builds the intersection database
- **Phase 2 (NEAR):** Coordinate-Mapped Auto-Placement — one-time calibration per intersection, then every scenario year auto-generates
- **Phase 3 (FUTURE):** Geo-Referenced Generation — any intersection, any aerial, computed placement from lat/lon + road bearings

Each phase builds on the previous. Nothing is throwaway work.

---

## 2. SYSTEM ARCHITECTURE

### 2.1 High-Level Data Flow

```
TMC Spreadsheet (XLSX)
        |
        v
+---------------------+
|  TMC Data Parser     | -- Extracts counts per approach/movement/period/scenario
|  (TypeScript module) |
+--------+------------+
         |
         v
+---------------------+     +--------------------------+
|  Scenario Engine     |<----|  Growth Factor Config     |
|  (computes all       |     |  (annual rates, horizon   |
|   scenario years)    |     |   years, trip gen rates)   |
+--------+------------+     +--------------------------+
         |
         v
+---------------------+     +--------------------------+
|  Exhibit Composer    |<----|  Intersection Config      |
|  (assembles PPTX     |     |  (approach positions,      |
|   slides)            |     |   aerial metadata,         |
+--------+------------+     |   component placement)     |
         |                   +--------------------------+
         v
+---------------------+
|  PPTX Output         | -- Professional exhibit slides
|  (pptxgenjs)         |    with all objects independently
+---------------------+    selectable/moveable
```

### 2.2 Where This Lives

This is a **workspace module** within the TFE (Traffic Studies Toolkit) section of the Centurion v2.0 application. It connects to the existing 10-step TIA workflow:

| Step | Name | Status | Exhibit Connection |
|------|------|--------|--------------------|
| 1 | Project Setup | Complete | Defines project metadata for title bars |
| 2 | Study Area Definition | Complete | Provides intersection list + aerial photos |
| 3 | Data Collection | Complete | TMC spreadsheet = source of truth |
| 4 | Existing Conditions | Complete | Feeds existing year exhibit data |
| 5 | Trip Generation | Complete | Feeds trip gen summary boxes |
| 6 | Trip Distribution | Complete | Feeds distribution percentages + arrows |
| 7 | Site Access | Complete (CC just built) | Feeds driveway inventory data |
| 8 | Capacity Analysis | In Progress | Feeds LOS results per approach |
| 9 | **Exhibit Generation** | **THIS SPEC** | Consumes Steps 1-8 output |
| 10 | Report Assembly | Pending | Consumes exhibits as PPTX inserts |

### 2.3 Integration with Centurion

The Exhibit Engine runs as a Tauri v2 command invoked from the React frontend. The user interacts through the TFE workspace panel. Data flows through the existing `tfe_step*_data` localStorage/Supabase structure.

---

## 3. DATA SCHEMAS

### 3.1 TMC Data Structure (parsed from spreadsheet)

This is the canonical data format. The TMC Parser (Section 4.1) outputs this structure.

```typescript
interface TMCDataset {
  project: {
    name: string;           // "Heritage Park Shoppes"
    location: string;       // "11381 W. Tangerine Rd, Marana, AZ"
    analyst: string;        // "Thomas J. Chlebanowski, PE"
    date_collected: string; // "June 2025"
  };

  intersections: IntersectionData[];
}

interface IntersectionData {
  id: string;                      // "tangerine_lon_adams"
  name: string;                    // "W. Tangerine Rd & N. Lon Adams Rd"
  lat: number;                     // 32.4512
  lon: number;                     // -111.0823

  approaches: ApproachData[];
  driveways: DrivewayData[];       // From Step 7

  scenarios: ScenarioYear[];
}

interface ApproachData {
  id: string;                      // "eb_tangerine"
  road_name: string;               // "W. Tangerine Rd"
  direction: "NB" | "SB" | "EB" | "WB";
  bearing: number;                 // Compass bearing in degrees (0-360)
  lanes: number;                   // Number of approach lanes
  movements: MovementData[];
}

interface MovementData {
  type: "left" | "through" | "right" | "uturn";
  counts: {
    am: number;
    md: number;    // MIDDAY -- Tom includes this, we must too
    pm: number;
  };
}

interface DrivewayData {
  id: string;                      // "circle_k_dwy"
  name: string;                    // "Circle K Driveway"
  road: string;                    // "W. Tangerine Rd"
  type: "Full" | "Right-In-Out" | "3/4-Movement";
  bearing: number;
  movements: MovementData[];
}

interface ScenarioYear {
  id: string;                      // "2025_existing"
  label: string;                   // "2025 Existing Weekday"
  year: number;                    // 2025
  type: "existing" | "background" | "background_plus_project" | "total";
  growth_factor: number;           // 1.0 for existing, 1.044 for 2026, etc.

  // Per-approach adjusted counts (base x growth + project trips if applicable)
  approach_volumes: {
    [approach_id: string]: {
      movements: {
        type: string;
        am: number;
        md: number;
        pm: number;
      }[];
      total_approach: { am: number; md: number; pm: number; };
    };
  };

  // Trip generation for this scenario (null for existing)
  trip_gen: TripGeneration | null;

  // Distribution percentages (from Step 6)
  distribution: {
    [approach_id: string]: number;  // percentage, e.g. 0.40 = 40%
  } | null;

  // Capacity results (from Step 8, when available)
  capacity: {
    [approach_id: string]: {
      los: "A" | "B" | "C" | "D" | "E" | "F";
      delay: number;      // seconds
      vcRatio: number;    // volume/capacity
    };
  } | null;
}

interface TripGeneration {
  am_total: number;          // 132
  pm_total: number;          // 121
  am_in_pct: number;         // 0.59
  am_out_pct: number;        // 0.41
  pm_in_pct: number;         // 0.46
  pm_out_pct: number;        // 0.54
  am_in: number;             // 69
  am_out: number;            // 63
  pm_in: number;             // 61
  pm_out: number;            // 60
  ite_code: string;          // "720 / 934"
  land_use: string;          // "Shopping Center / QSR"
}
```

### 3.2 Intersection Configuration (placement rules)

This is the bridge from Phase 1 -> Phase 2 -> Phase 3. It starts empty, gets populated during calibration, and eventually computes from geo-data.

```typescript
interface IntersectionConfig {
  id: string;                      // "tangerine_lon_adams"
  name: string;

  // --- PHASE 1: Manual calibration data ---
  aerial: {
    source_file: string;           // "aerial_intersection.jpg"
    slide_dimensions: {            // PPTX slide space
      w: number;                   // 10 (inches, 16:9)
      h: number;                   // 5.625
    };
    // These get populated during calibration:
    center_x: number | null;       // Intersection center on slide (inches)
    center_y: number | null;
  };

  // Per-approach placement -- populated by calibration
  approach_placements: {
    [approach_id: string]: {
      grid_x: number;             // TMC grid top-left X on slide
      grid_y: number;             // TMC grid top-left Y on slide
      grid_orientation: "horizontal" | "vertical";
      arrow_x: number;            // Direction arrow X
      arrow_y: number;            // Direction arrow Y
      arrow_direction: string;    // "right", "left", "up", "down"
      label_x: number;            // Volume label X (if separate from grid)
      label_y: number;
    };
  };

  // Landmark positions
  landmarks: {
    name: string;                  // "FRY'S MARKET"
    x: number;
    y: number;
    style: "gold" | "orange" | "green" | "dark";
  }[];

  // Fixed furniture positions
  furniture: {
    trip_gen_box: { x: number; y: number; w: number; h: number; };
    legend: { x: number; y: number; };
    compass: { x: number; y: number; };
    title_bar: { y: number; };     // X is always 0, W is always full width
  };

  // --- PHASE 3: Geo-registration data ---
  geo: {
    // Aerial photo geo-bounds (populated if known)
    top_left: { lat: number; lon: number; } | null;
    bottom_right: { lat: number; lon: number; } | null;

    // Intersection center in real-world coords
    center: { lat: number; lon: number; } | null;

    // Road bearings (degrees from north, clockwise)
    road_bearings: {
      [road_name: string]: number;  // "W. Tangerine Rd": 85
    } | null;
  } | null;

  // --- METADATA ---
  calibrated_by: string | null;    // "Bill King"
  calibrated_date: string | null;  // "2026-02-10"
  calibration_source: "manual" | "computed" | null;
  version: number;                 // Increments on each calibration
}
```

### 3.3 Exhibit Template Definition

Each scenario year generates a specific set of exhibit slides. This defines what gets built:

```typescript
interface ExhibitTemplate {
  // Standard exhibit sequence (Tom's ordering)
  exhibits: ExhibitSlide[];
}

interface ExhibitSlide {
  id: string;                        // "existing_tmc_counts"
  title: string;                     // "2025 Existing Weekday AM & PM TMC Counts"
  type: "plat" | "trip_distribution" | "tmc_counts" | "lane_percentages" |
        "growth_adjusted" | "project_trips" | "total_volumes" | "capacity";
  scenario_id: string;               // Which scenario feeds this slide

  // What components appear on this slide
  components: {
    aerial_background: boolean;       // Use intersection aerial as bg
    tmc_grids: boolean;               // Show TMC data grids at approaches
    direction_arrows: boolean;        // Show movement arrows
    volume_labels: boolean;           // Show XX (XX) labels
    percentage_labels: boolean;       // Show distribution %
    trip_gen_box: boolean;            // Show trip generation summary
    capacity_results: boolean;        // Show LOS results
    landmark_labels: boolean;         // Show Fry's, Circle K, etc.
    car_icons: boolean;               // Show vehicle flow paths
    legend: boolean;
    compass: boolean;
    title_bar: boolean;               // Always true
  };
}
```

The standard Heritage Park exhibit set (matching Tom's report) is:

1. **Plat Area** -- wide aerial, project area highlighted
2. **Trip Distribution** -- aerial with large directional arrows + percentages
3. **2025 Existing TMC** -- aerial overlay with TMC grids (AM/MD/PM) at each approach
4. **2025 Lane Movement %** -- percentage labels at each movement
5. **2026 Background** -- growth-adjusted TMC grids (x1.044)
6. **2026 Background + Project** -- above + Lot #3 project trips added
7. **2031 Total Volumes** -- horizon year with full build (x1.24 + all project trips)
8. **2025 Capacity Analysis** -- LOS results overlaid
9. **2026 Capacity Analysis** -- LOS with growth
10. **2031 Capacity Analysis** -- LOS at horizon year

---

## 4. MODULE SPECIFICATIONS

### 4.1 TMC Data Parser

**Input:** XLSX file (Tom's TMC spreadsheet format)
**Output:** `TMCDataset` object
**Technology:** TypeScript + SheetJS (xlsx library)

**Requirements:**
- Parse multiple worksheet tabs (one per intersection is common)
- Handle Tom's specific layout: header rows, merged cells, approach sections
- Extract AM, MD (midday), and PM counts for each movement
- Identify approach names from road labels
- Handle both raw counts and pre-calculated totals
- Validate: all approaches have all three time periods
- Validate: left + through + right = total approach volume (within rounding)

**Known Complexity:**
Tom's spreadsheets are NOT standardized templates -- column positions and label formats vary between projects. The parser needs a flexible header detection algorithm, not hardcoded cell references. Recommend: scan for pattern keywords ("Left", "Thru/Through", "Right", "AM", "PM", "Midday/MD") and infer structure.

**DECISION (Bill, 2026-02-10):** Enforce a standardized TMC input template. Tom will adapt to the defined format. CC agents: design the template spec as part of your review -- define sheet names, column headers, cell layout, and validation rules.

### 4.2 Scenario Engine

**Input:** `TMCDataset` + growth configuration + trip generation data (from Steps 5-6)
**Output:** Complete `ScenarioYear[]` array with all computed volumes

**Computation Logic:**
```
For each scenario year:
  For each intersection:
    For each approach:
      For each movement (L/T/R):
        base_count = existing TMC count
        growth_adjusted = base_count x growth_factor

        if scenario includes project trips:
          project_addition = total_trips x distribution_pct x movement_share
          adjusted_count = growth_adjusted + project_addition
        else:
          adjusted_count = growth_adjusted

        Round to nearest integer
```

**Growth Factor Sources:**
- PAG (Pima Association of Governments) provides annual growth rates
- Tom typically uses 4.4% per year for Marana area
- Compound: `factor = (1 + annual_rate) ^ years_from_base`

**Critical Data Integrity Rule:**
Every number in the output exhibits must be traceable back to: (a) a raw TMC count, (b) a published growth rate, or (c) an ITE trip generation rate. No approximations. No "I'll estimate this." The TMC spreadsheet is scripture.

### 4.3 Component Renderer

**Input:** `ScenarioYear` data for one intersection + `IntersectionConfig`
**Output:** PptxGenJS slide objects with all components positioned

**Component Catalog:**

| Component | Description | Moveable | Editable |
|-----------|-------------|----------|----------|
| TMC Data Grid | Table showing L/T/R x AM/MD/PM per approach | Yes | Yes (double-click) |
| Direction Arrow | Block arrow showing movement direction | Yes | No |
| Turn Arrow | Curved arrow for L/R turns | Yes | No |
| Volume Label | "XX (XX)" formatted count box | Yes | Yes |
| Percentage Label | "XX%" formatted distribution box | Yes | Yes |
| Trip Gen Box | Gold summary box with in/out breakdown | Yes | Yes |
| Landmark Label | Named location box (Fry's, Circle K, etc.) | Yes | Yes |
| Legend Box | Explains notation format | Yes | No |
| LOS Result | Color-coded level of service indicator | Yes | No |
| North Compass | Orientation indicator | Yes | No |
| Title Bar | Gold bar at bottom with exhibit title | Yes | Yes |
| Car Icon | Vehicle silhouette for trip distribution | Yes | No |

**TMC Grid Spec (matching Tom's format):**
```
+-------------+------+------+------+
| [Road Name] |  AM  |  MD  |  PM  |   <- Gold header row
+-------------+------+------+------+
| Left  [<-]  |  37  |  22  |  90  |   <- Movement rows with
| Thru  [^]   |  26  |  15  |  23  |     directional arrows
| Right [->]  |   4  |   3  |   4  |     embedded in labels
+-------------+------+------+------+
| TOTAL       |  67  |  40  | 117  |   <- Auto-summed
+-------------+------+------+------+
```

**Missing from v1 prototype (must add):**
- Midday (MD) column
- Total row per approach
- Pedestrian count row (when applicable)
- Peak Hour Factor (PHF) display

### 4.4 Exhibit Composer

**Input:** Complete `ScenarioYear[]` + `IntersectionConfig` + `ExhibitTemplate`
**Output:** Complete PPTX file

**Composition Logic (per slide):**
1. Set slide background (aerial photo or white)
2. If aerial: add semi-transparent overlay for readability
3. For each approach in intersection config:
   a. Look up placement coordinates from config
   b. Look up volume data from scenario
   c. Render TMC grid at specified position
   d. Render directional arrows at specified position
4. Add landmark labels at configured positions
5. Add trip gen box at configured position
6. Add legend, compass, title bar at configured positions
7. Every element = independent PPTX object (no grouping in Phase 1)

### 4.5 Calibration Module (Phase 1->2 Bridge)

This is the critical piece that makes manual work reusable.

**Workflow:**
1. System generates a "calibration slide" with:
   - Aerial photo as background
   - TMC grids placed at default positions (best guess based on direction)
   - Landmarks at default positions
2. User opens in PowerPoint, drags everything to correct positions
3. User saves and re-uploads the calibrated PPTX
4. System reads back all object positions from the PPTX XML
5. System saves positions to `IntersectionConfig`
6. All future scenario years for this intersection auto-place correctly

**Position Extraction (reading PPTX XML):**

Every PptxGenJS object writes its position as EMU (English Metric Units) in the slide XML:
```xml
<p:sp>
  <p:spPr>
    <a:xfrm>
      <a:off x="914400" y="457200"/>  <!-- Position in EMU -->
      <a:ext cx="2743200" cy="1371600"/>  <!-- Size in EMU -->
    </a:xfrm>
  </p:spPr>
</p:sp>
```

EMU -> inches: `inches = emu / 914400`

The calibration reader parses the PPTX, identifies each component by its alt-text tag (we embed component IDs as alt-text during generation), and records the final x/y/w/h.

**CC Agent Review Question (DECISION NEEDED):** Should the calibration UI be built inside Centurion (React drag-and-drop canvas) instead of requiring PowerPoint round-trip? Bill deferred this to engineering. Agent 2: make the call with full rationale.

### 4.6 Geo-Registration Module (Phase 3)

**Purpose:** Given an aerial photo with known geographic bounds and an intersection with known road geometry, compute all component positions mathematically.

**Required Inputs:**
1. Aerial photo + its geographic bounds (two corner lat/lons)
2. Intersection center point (lat/lon)
3. Road bearings (compass degrees for each road)
4. Standard component offsets (how far from center to place each grid)

**Computation:**
```typescript
function geoToSlide(
  lat: number, lon: number,
  aerial: { topLeft: LatLon; bottomRight: LatLon; slideW: number; slideH: number; }
): { x: number; y: number } {
  const xPct = (lon - aerial.topLeft.lon) / (aerial.bottomRight.lon - aerial.topLeft.lon);
  const yPct = (aerial.topLeft.lat - lat) / (aerial.topLeft.lat - aerial.bottomRight.lat);
  return {
    x: xPct * aerial.slideW,
    y: yPct * aerial.slideH
  };
}

function approachPosition(
  center: { x: number; y: number },
  bearing: number,        // Road bearing in degrees
  offsetInches: number    // How far from center to place grid
): { x: number; y: number } {
  const rad = (bearing * Math.PI) / 180;
  return {
    x: center.x + Math.sin(rad) * offsetInches,
    y: center.y - Math.cos(rad) * offsetInches  // Y inverted on slide
  };
}
```

**Known Challenges:**
- Aerial photo projection distortion (Google Earth uses Mercator; at Arizona latitudes this is minor)
- Road bearing is not perfectly straight at most intersections (curves, tapers)
- Grid orientation needs to match road angle (a road running NE-SW needs a rotated grid)

**CC Agent Review Question:** Should we support rotated grids (matching actual road bearing) or only cardinal-aligned grids (N/S/E/W)? Rotated is more accurate but pptxgenjs table rotation is limited. We may need to render grids as images instead of tables for arbitrary rotation.

---

## 5. PHASE IMPLEMENTATION PLAN

### Phase 1: Component Library + Calibration Capture
**Goal:** Produce usable exhibits NOW while building the calibration database
**Timeline:** 2-3 weeks
**Deliverables:**

1. TMC Data Parser -- reads Tom's spreadsheet, outputs TMCDataset JSON
2. Scenario Engine -- computes all scenario years with correct math
3. Component Renderer -- generates all component types as PPTX objects
4. PPTX Generator -- assembles slides with components at default positions
5. **Calibration capture** -- embeds component IDs in alt-text so positions can be read back
6. **Per-scenario object kit slides** -- each scenario year gets its own library slide with pre-populated, pre-oriented components

**Output:** User gets PPTX with:
- 3 component library slides (arrows, grids, labels/branding)
- Per-scenario exhibit slides with components at approximate positions
- User fine-tunes in PowerPoint
- Re-upload captures positions for Phase 2

### Phase 2: Coordinate-Mapped Auto-Placement
**Goal:** Zero manual positioning for calibrated intersections
**Timeline:** 2-3 weeks after Phase 1
**Deliverables:**

1. Calibration Reader -- extracts positions from user-adjusted PPTX
2. Config Store -- saves/loads IntersectionConfig (Supabase)
3. Auto-Composer -- uses stored configs to place all components automatically
4. **New project, same intersection** = instant exhibits (just swap data)

**Key Metric:** Second TIA study at same intersection takes <5 minutes of exhibit work instead of hours.

### Phase 3: Geo-Referenced Generation
**Goal:** New intersection = minimal setup, computed placement
**Timeline:** 4-6 weeks after Phase 2
**Deliverables:**

1. Geo-Registration UI -- user marks two known points on aerial to establish coordinate system
2. Road Bearing Input -- user specifies or system detects from aerial
3. Computed Placement Engine -- positions all components from geo-data
4. **Prometheus Integration** -- shared coordinate math library

**Key Metric:** Brand new intersection exhibit set generated from TMC spreadsheet + aerial photo + 2 minutes of geo-calibration.

---

## 6. BRANDING & STYLE SPEC

All exhibits must match Tom Chlebanowski's established design language:

| Element | Specification |
|---------|--------------|
| Title bar | Gold (#D4A517) full-width bar, bottom of slide |
| Title text | Arial Bold 10pt, black, left-aligned with 0.65" indent |
| Compass | Tom's N-arrow icon, bottom-left corner of title bar |
| TMC grid header | Gold fill, black text, Arial Bold 8pt |
| TMC grid cells | White fill, black text, Arial 9pt |
| Grid borders | 1pt gray (#666666) |
| Direction arrows | Color-coded: Green=EB, Blue=WB, Orange=NB, Red=SB |
| Volume labels | Light yellow (#FFFFDD) fill, red text, Arial Bold 8pt |
| Percentage labels | Bright yellow (#FFEB3B) fill, black text, Arial Bold 11pt |
| Trip gen box | Gold fill, dark gold border, 1pt, drop shadow |
| Landmark labels | Gold fill for commercial, green for parks, orange for project |
| LOS indicators | Green->Red gradient matching standard A-F scale |
| Aerial overlay | 40% transparent white rectangle for readability |
| Font family | Arial exclusively (matches Tom's existing work) |

---

## 7. OPEN QUESTIONS FOR CC AGENT REVIEW

These are decisions that need engineering input before we commit code:

1. **TMC Parser Strategy:** DECIDED -- Enforce standardized template. CC agents to design template spec.

2. **Calibration UI:** DEFERRED TO ENGINEERING -- PowerPoint round-trip vs. in-app canvas? Agent 2 to recommend.

3. **Grid Rotation:** Cardinal-only vs. bearing-matched rotation? (Section 4.6)

4. **Data Storage:** Where do IntersectionConfigs live? Options:
   - Supabase (shared across team, requires connectivity)
   - Local JSON files in project folder (works offline, per-machine)
   - Both with sync (most robust, most complex)

5. **PPTX Generation Location:** Should this run:
   - In Tauri backend (Rust -> Node child process)?
   - In React frontend (pptxgenjs runs in browser)?
   - As a standalone CLI tool (CC can invoke directly)?

6. **Midday Counts:** Tom includes AM/MD/PM. Some jurisdictions only require AM/PM. Should the system support configurable time periods?

7. **Multiple Intersections per Study:** Heritage Park has one intersection. Many TIAs study 3-5+ intersections. How does the exhibit sequence scale? One aerial per intersection, or overview maps showing all intersections?

8. **Capacity Analysis Integration:** Step 8 (not yet built) will produce LOS results. Should the exhibit engine wait for Step 8 data, or generate TMC-only exhibits first and add capacity overlays later?

9. **Version Control:** When Tom adjusts counts or growth factors, how do we track which exhibit set corresponds to which data version? Timestamp-based? Git-style versioning?

10. **Export Formats:** PPTX is primary. Should we also support PDF export (for submittals) and HTML (for web preview in Centurion)?

---

## 8. CC AGENT REVIEW INSTRUCTIONS

CC -- please have your agents review this spec with the following focus areas:

### Architecture Review
- Does the data flow make sense? Are there missing connections?
- Is the TypeScript interface design sound? Any type safety gaps?
- Would you structure the module boundaries differently?

### Feasibility Review
- Can pptxgenjs handle all the rendering requirements listed?
- Is the calibration capture (reading back PPTX positions) realistic?
- What are the hardest engineering challenges you see?

### Integration Review
- How does this connect to the existing TFE workspace in Centurion?
- Where should the exhibit generation trigger live in the UI?
- How do Steps 1-8 feed data to Step 9?

### Missing Pieces
- What did Jake miss? What engineering concerns aren't addressed?
- Are there edge cases in the TMC data that would break the parser?
- What happens when Tom's format doesn't match the schema?

### Recommended Tech Stack
- Confirm or challenge: TypeScript + pptxgenjs + SheetJS
- Should we use python-pptx instead for server-side generation?
- Any libraries we should evaluate for geo-computation?

**Return your review as a structured document with sections matching the above.**

---

## 9. SKILL TEMPLATE NOTES

This system is designed to become a reusable **skill** -- not just for Heritage Park, not just for Trajanus, but for any traffic study. The architecture deliberately separates:

- **Data** (TMC counts, growth rates, trip generation) -- project-specific
- **Configuration** (intersection geometry, placement rules) -- intersection-specific but reusable
- **Templates** (exhibit types, slide sequences) -- study-type-specific
- **Branding** (colors, fonts, logo placement) -- firm-specific

A new TE firm could plug in their branding, their TMC spreadsheet format, and their preferred exhibit sequence -- and get the same automation. That's the product.

---

*End of specification. Awaiting CC agent review.*
