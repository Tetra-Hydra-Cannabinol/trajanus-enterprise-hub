/**
 * TMUTCD Traffic Signal Warrant Calculator
 * Trajanus Command Center — TSE Warrant Engine
 *
 * Implements Warrants 1, 2, and 3 per the Texas Manual on Uniform Traffic
 * Control Devices (TMUTCD), which mirrors the national MUTCD standards.
 *
 * Global export: window.WarrantEngine
 * No bundler required — plain ES5-compatible vanilla JavaScript.
 *
 * Created: 2026-02-18
 */

(function (global) {
  'use strict';

  // ─────────────────────────────────────────────────────────────────────────────
  // ENUMS
  // ─────────────────────────────────────────────────────────────────────────────

  var ThresholdColumn = {
    FULL:      100,
    EIGHTY:     80,
    SEVENTY:    70,
    FIFTY_SIX:  56
  };

  var LaneConfig = {
    ONE_ONE:        '1_1',
    TWO_PLUS_ONE:   '2+_1',
    TWO_PLUS_TWO_PLUS: '2+_2+',
    ONE_TWO_PLUS:   '1_2+'
  };

  var WarrantResult = {
    MET:     'MET',
    NOT_MET: 'NOT MET'
  };

  // ─────────────────────────────────────────────────────────────────────────────
  // WARRANT 1 THRESHOLD TABLES (Legal Standards — Do Not Modify)
  // ─────────────────────────────────────────────────────────────────────────────

  // Condition A — Minimum Vehicular Volume
  var WARRANT1_CONDITION_A = {
    '1_1':   {
      100: { major: 500, minor: 150 },
       80: { major: 400, minor: 120 },
       70: { major: 350, minor: 105 },
       56: { major: 280, minor:  84 }
    },
    '2+_1':  {
      100: { major: 600, minor: 150 },
       80: { major: 480, minor: 120 },
       70: { major: 420, minor: 105 },
       56: { major: 336, minor:  84 }
    },
    '2+_2+': {
      100: { major: 600, minor: 200 },
       80: { major: 480, minor: 160 },
       70: { major: 420, minor: 140 },
       56: { major: 336, minor: 112 }
    },
    '1_2+':  {
      100: { major: 500, minor: 200 },
       80: { major: 400, minor: 160 },
       70: { major: 350, minor: 140 },
       56: { major: 280, minor: 112 }
    }
  };

  // Condition B — Interruption of Continuous Traffic
  var WARRANT1_CONDITION_B = {
    '1_1':   {
      100: { major: 750, minor:  75 },
       80: { major: 600, minor:  60 },
       70: { major: 525, minor:  53 },
       56: { major: 420, minor:  42 }
    },
    '2+_1':  {
      100: { major: 900, minor:  75 },
       80: { major: 720, minor:  60 },
       70: { major: 630, minor:  53 },
       56: { major: 504, minor:  42 }
    },
    '2+_2+': {
      100: { major: 900, minor: 100 },
       80: { major: 720, minor:  80 },
       70: { major: 630, minor:  70 },
       56: { major: 504, minor:  56 }
    },
    '1_2+':  {
      100: { major: 750, minor: 100 },
       80: { major: 600, minor:  80 },
       70: { major: 525, minor:  70 },
       56: { major: 420, minor:  56 }
    }
  };

  // ─────────────────────────────────────────────────────────────────────────────
  // WARRANT 2 — FOUR-HOUR VEHICLE VOLUME CURVES
  // ─────────────────────────────────────────────────────────────────────────────
  // Format: [majorVPH, minorVPH] control points for piecewise linear interpolation

  // 100% curves
  var W2_CURVE_1_1_100   = [[300,310],[400,260],[500,220],[600,190],[700,170],[800,155],[900,140],[1000,130],[1100,120],[1200,110],[1300,100],[1400,80]];
  var W2_CURVE_2P_1_100  = [[300,250],[400,210],[500,180],[600,155],[700,140],[800,130],[900,120],[1000,110],[1100,100],[1200,90],[1300,80],[1400,80]];
  var W2_CURVE_2P_2P_100 = [[300,290],[400,240],[500,200],[600,175],[700,160],[800,145],[900,130],[1000,120],[1100,115],[1200,115],[1300,115],[1400,115]];

  // 70% curves (also used for 56% column — selection is by 70/100 family)
  var W2_CURVE_1_1_70    = [[210,220],[280,185],[350,155],[420,135],[490,120],[560,110],[630,100],[700,92],[770,85],[840,78],[910,70],[980,60]];
  var W2_CURVE_2P_1_70   = [[210,175],[280,150],[350,128],[420,110],[490,100],[560,92],[630,85],[700,78],[770,72],[840,65],[910,60],[980,60]];
  var W2_CURVE_2P_2P_70  = [[210,205],[280,170],[350,142],[420,125],[490,115],[560,105],[630,95],[700,88],[770,82],[840,80],[910,80],[980,80]];

  // ─────────────────────────────────────────────────────────────────────────────
  // WARRANT 3 — PEAK-HOUR VOLUME CURVES
  // ─────────────────────────────────────────────────────────────────────────────

  // 100% curves
  var W3_CURVE_1_1_100   = [[400,180],[500,160],[600,145],[700,130],[800,120],[900,115],[1000,110],[1100,105],[1200,100],[1400,100],[1600,100],[1800,100]];
  var W3_CURVE_2P_1_100  = [[400,160],[500,140],[600,125],[700,115],[800,108],[900,102],[1000,100],[1100,100],[1200,100],[1400,100],[1600,100],[1800,100]];
  var W3_CURVE_2P_2P_100 = [[400,200],[500,180],[600,165],[700,155],[800,150],[900,150],[1000,150],[1100,150],[1200,150],[1400,150],[1600,150],[1800,150]];

  // 70% curves
  var W3_CURVE_1_1_70    = [[280,130],[350,115],[420,105],[490,95],[560,88],[630,83],[700,78],[770,75],[840,75],[980,75],[1120,75],[1260,75]];
  var W3_CURVE_2P_1_70   = [[280,115],[350,100],[420,90],[490,83],[560,78],[630,75],[700,75],[770,75],[840,75],[980,75],[1120,75],[1260,75]];
  var W3_CURVE_2P_2P_70  = [[280,145],[350,130],[420,120],[490,112],[560,108],[630,105],[700,100],[770,100],[840,100],[980,100],[1120,100],[1260,100]];

  // ─────────────────────────────────────────────────────────────────────────────
  // CURVE SELECTION HELPER
  // ─────────────────────────────────────────────────────────────────────────────

  /**
   * Select the appropriate Warrant 2 curve array given lane config and threshold column.
   * 1_2+ uses same curves as 1_1.
   * Columns 70 and 56 → use 70% curve family.
   * Columns 100 and 80 → use 100% curve family.
   */
  function selectW2Curve(laneConfig, thresholdColumn) {
    var use70 = (thresholdColumn === 70 || thresholdColumn === 56);
    if (laneConfig === '2+_2+') {
      return use70 ? W2_CURVE_2P_2P_70 : W2_CURVE_2P_2P_100;
    }
    if (laneConfig === '2+_1') {
      return use70 ? W2_CURVE_2P_1_70  : W2_CURVE_2P_1_100;
    }
    // '1_1' and '1_2+' use same curves
    return use70 ? W2_CURVE_1_1_70 : W2_CURVE_1_1_100;
  }

  /**
   * Select the appropriate Warrant 3 curve array.
   */
  function selectW3Curve(laneConfig, thresholdColumn) {
    var use70 = (thresholdColumn === 70 || thresholdColumn === 56);
    if (laneConfig === '2+_2+') {
      return use70 ? W3_CURVE_2P_2P_70 : W3_CURVE_2P_2P_100;
    }
    if (laneConfig === '2+_1') {
      return use70 ? W3_CURVE_2P_1_70  : W3_CURVE_2P_1_100;
    }
    return use70 ? W3_CURVE_1_1_70 : W3_CURVE_1_1_100;
  }

  // ─────────────────────────────────────────────────────────────────────────────
  // INTERPOLATION
  // ─────────────────────────────────────────────────────────────────────────────

  /**
   * Piecewise-linear interpolation along a curve.
   * curve: array of [x, y] control points, sorted ascending by x.
   * majorVPH: the x-value to look up.
   * Returns the interpolated minimum minor VPH threshold.
   */
  function interpolateCurve(curve, majorVPH) {
    if (majorVPH <= curve[0][0]) return curve[0][1];
    if (majorVPH >= curve[curve.length - 1][0]) return curve[curve.length - 1][1];
    for (var i = 0; i < curve.length - 1; i++) {
      if (majorVPH >= curve[i][0] && majorVPH <= curve[i + 1][0]) {
        var t = (majorVPH - curve[i][0]) / (curve[i + 1][0] - curve[i][0]);
        return Math.round(curve[i][1] + t * (curve[i + 1][1] - curve[i][1]));
      }
    }
    return curve[curve.length - 1][1];
  }

  // ─────────────────────────────────────────────────────────────────────────────
  // THRESHOLD COLUMN DETERMINATION
  // ─────────────────────────────────────────────────────────────────────────────

  /**
   * Determine which threshold column (100, 80, 70, or 56) applies.
   *
   * Reductions apply when:
   *   - 85th percentile speed > 40 mph (rural/higher speed)
   *   - OR population < 10,000 (small community)
   *
   * combinationAB: true when evaluating Condition A+B combination after
   *   remedial measures have been tried.
   *
   * Returns: { column: number, reason: string }
   */
  function determineThresholdColumn(speed85th, population, combinationAB) {
    combinationAB = combinationAB || false;

    var speed70 = speed85th > 40;
    var pop70   = population < 10000;
    var use70   = speed70 || pop70;

    if (use70 && combinationAB) {
      var reasons = [];
      if (speed70) reasons.push('85th %ile speed = ' + speed85th + ' mph > 40 mph');
      if (pop70)   reasons.push('population = ' + population.toLocaleString() + ' < 10,000');
      reasons.push('combination A+B after remedial measures');
      return { column: 56, reason: '56% — ' + reasons.join('; ') };
    }

    if (combinationAB) {
      return { column: 80, reason: '80% — combination A+B after remedial measures' };
    }

    if (use70) {
      var reasons2 = [];
      if (speed70) reasons2.push('85th %ile speed = ' + speed85th + ' mph > 40 mph');
      if (pop70)   reasons2.push('population = ' + population.toLocaleString() + ' < 10,000');
      return { column: 70, reason: '70% — ' + reasons2.join('; ') };
    }

    return { column: 100, reason: '100% — standard thresholds (no reductions)' };
  }

  // ─────────────────────────────────────────────────────────────────────────────
  // LANE CONFIG DETERMINATION
  // ─────────────────────────────────────────────────────────────────────────────

  /**
   * Determine lane configuration key from approach lane descriptors.
   * majorLanes: '1' or '2+'
   * minorLanes: '1' or '2+'
   */
  function determineLaneConfig(majorLanes, minorLanes) {
    if (majorLanes === '2+' && minorLanes === '2+') return '2+_2+';
    if (majorLanes === '2+' && minorLanes === '1')  return '2+_1';
    if (majorLanes === '1'  && minorLanes === '2+') return '1_2+';
    return '1_1';
  }

  // ─────────────────────────────────────────────────────────────────────────────
  // HOURLY VOLUME PROCESSING
  // ─────────────────────────────────────────────────────────────────────────────

  /**
   * Process raw hourly approach volumes and evaluate each hour against warrants.
   *
   * hourlyVolumes: array of 24 objects, one per hour (index 0 = midnight–1am):
   *   { hour, majorApproach1, majorApproach2, minorApproach1, minorApproach2 }
   *
   * Returns array of HourlyAnalysisRow:
   *   {
   *     hour, majorTotal, minorHigher,
   *     condA_pass, condB_pass,
   *     w2_curveThreshold, w2_pass,
   *     majorApproach1, majorApproach2, minorApproach1, minorApproach2
   *   }
   *
   * CRITICAL:
   *   majorTotal  = majorApproach1 + majorApproach2  (SUM both directions)
   *   minorHigher = Math.max(minorApproach1, minorApproach2)  (HIGHER direction only)
   */
  function processHourlyVolumes(hourlyVolumes, laneConfig, thresholdColumn, condAThresh, condBThresh) {
    var w2Curve = selectW2Curve(laneConfig, thresholdColumn);

    return hourlyVolumes.map(function (vol) {
      var majorTotal  = vol.majorApproach1 + vol.majorApproach2;
      var minorHigher = Math.max(vol.minorApproach1, vol.minorApproach2);

      // Warrant 1 Condition A: both major and minor must meet or exceed threshold
      var condA_pass = (majorTotal >= condAThresh.major) && (minorHigher >= condAThresh.minor);

      // Warrant 1 Condition B
      var condB_pass = (majorTotal >= condBThresh.major) && (minorHigher >= condBThresh.minor);

      // Warrant 2: interpolate curve to get minimum minor threshold at this major volume
      var w2Threshold = interpolateCurve(w2Curve, majorTotal);
      var w2_pass     = minorHigher >= w2Threshold;

      return {
        hour:             vol.hour,
        majorApproach1:   vol.majorApproach1,
        majorApproach2:   vol.majorApproach2,
        minorApproach1:   vol.minorApproach1,
        minorApproach2:   vol.minorApproach2,
        majorTotal:       majorTotal,
        minorHigher:      minorHigher,
        condA_pass:       condA_pass,
        condB_pass:       condB_pass,
        w2_curveThreshold: w2Threshold,
        w2_pass:          w2_pass
      };
    });
  }

  // ─────────────────────────────────────────────────────────────────────────────
  // WARRANT 1 EVALUATION
  // ─────────────────────────────────────────────────────────────────────────────

  /**
   * Evaluate Warrant 1 — Minimum Vehicular Volume.
   *
   * Condition A: >= 8 hours where BOTH major AND minor pass Cond A threshold.
   * Condition B: >= 8 hours where BOTH major AND minor pass Cond B threshold.
   * Overall result: MET if Condition A OR Condition B is MET.
   * Hours do NOT need to be consecutive.
   *
   * Returns:
   *   {
   *     conditionA: { hoursMet, threshold8, result },
   *     conditionB: { hoursMet, threshold8, result },
   *     result: WarrantResult,
   *     condAThresholds: { major, minor },
   *     condBThresholds: { major, minor }
   *   }
   */
  function evaluateWarrant1(hourlyAnalysis, condAThresholds, condBThresholds) {
    var condAHours = 0;
    var condBHours = 0;

    hourlyAnalysis.forEach(function (row) {
      if (row.condA_pass) condAHours++;
      if (row.condB_pass) condBHours++;
    });

    var condAMet = condAHours >= 8;
    var condBMet = condBHours >= 8;
    var overallMet = condAMet || condBMet;

    return {
      conditionA: {
        hoursMet:   condAHours,
        threshold8: 8,
        result:     condAMet ? WarrantResult.MET : WarrantResult.NOT_MET
      },
      conditionB: {
        hoursMet:   condBHours,
        threshold8: 8,
        result:     condBMet ? WarrantResult.MET : WarrantResult.NOT_MET
      },
      condAThresholds: condAThresholds,
      condBThresholds: condBThresholds,
      result: overallMet ? WarrantResult.MET : WarrantResult.NOT_MET
    };
  }

  // ─────────────────────────────────────────────────────────────────────────────
  // WARRANT 2 EVALUATION
  // ─────────────────────────────────────────────────────────────────────────────

  /**
   * Evaluate Warrant 2 — Four-Hour Vehicular Volume.
   *
   * Count hours where the data point is above the warrant curve.
   * MET if >= 4 such hours.
   *
   * Returns:
   *   { hoursMet, threshold4, result }
   */
  function evaluateWarrant2(hourlyAnalysis) {
    var hoursMet = 0;
    hourlyAnalysis.forEach(function (row) {
      if (row.w2_pass) hoursMet++;
    });

    return {
      hoursMet:   hoursMet,
      threshold4: 4,
      result:     hoursMet >= 4 ? WarrantResult.MET : WarrantResult.NOT_MET
    };
  }

  // ─────────────────────────────────────────────────────────────────────────────
  // WARRANT 3 EVALUATION
  // ─────────────────────────────────────────────────────────────────────────────

  /**
   * Evaluate Warrant 3 — Peak-Hour Volume.
   *
   * AM peak = highest majorTotal hour in range 6–10 (inclusive, 24-hour clock index).
   * PM peak = highest majorTotal hour in range 15–19 (inclusive).
   *
   * For each peak, interpolate the Warrant 3 curve.
   * MET if EITHER peak's minorHigher >= curve threshold.
   *
   * Returns:
   *   {
   *     amPeak: { hour, majorTotal, minorHigher, curveThreshold, pass },
   *     pmPeak: { hour, majorTotal, minorHigher, curveThreshold, pass },
   *     result: WarrantResult
   *   }
   */
  function evaluateWarrant3(hourlyAnalysis, laneConfig, thresholdColumn) {
    var w3Curve = selectW3Curve(laneConfig, thresholdColumn);

    // Find AM peak (hours index 6–10)
    var amRows = hourlyAnalysis.filter(function (r) { return r.hour >= 6 && r.hour <= 10; });
    var amPeakRow = amRows.reduce(function (best, row) {
      return row.majorTotal > best.majorTotal ? row : best;
    }, amRows[0]);

    // Find PM peak (hours index 15–19)
    var pmRows = hourlyAnalysis.filter(function (r) { return r.hour >= 15 && r.hour <= 19; });
    var pmPeakRow = pmRows.reduce(function (best, row) {
      return row.majorTotal > best.majorTotal ? row : best;
    }, pmRows[0]);

    function evalPeak(row) {
      var threshold = interpolateCurve(w3Curve, row.majorTotal);
      return {
        hour:           row.hour,
        majorTotal:     row.majorTotal,
        minorHigher:    row.minorHigher,
        curveThreshold: threshold,
        pass:           row.minorHigher >= threshold
      };
    }

    var amPeak = evalPeak(amPeakRow);
    var pmPeak = evalPeak(pmPeakRow);
    var overallMet = amPeak.pass || pmPeak.pass;

    return {
      amPeak: amPeak,
      pmPeak: pmPeak,
      result: overallMet ? WarrantResult.MET : WarrantResult.NOT_MET
    };
  }

  // ─────────────────────────────────────────────────────────────────────────────
  // MAIN ENTRY POINT
  // ─────────────────────────────────────────────────────────────────────────────

  /**
   * Evaluate all three warrants for a given study.
   *
   * input: WarrantStudyInput {
   *   projectName:   string,
   *   location:      string,
   *   majorStreet:   string,
   *   minorStreet:   string,
   *   majorLanes:    '1' | '2+',
   *   minorLanes:    '1' | '2+',
   *   speed85th:     number (mph),
   *   population:    number,
   *   postedSpeed:   number (mph),
   *   combinationAB: boolean (optional),
   *   hourlyVolumes: array of 24 HourlyVolume objects
   * }
   *
   * Returns: WarrantStudyResult {
   *   input,
   *   laneConfig,
   *   thresholdInfo: { column, reason },
   *   condAThresholds: { major, minor },
   *   condBThresholds: { major, minor },
   *   hourlyAnalysis:  [ ...HourlyAnalysisRow ],
   *   warrant1:        Warrant1Result,
   *   warrant2:        Warrant2Result,
   *   warrant3:        Warrant3Result,
   *   summary:         { warrantsMetCount, recommendation, details }
   * }
   */
  function evaluateWarrants(input) {
    // Determine lane config and threshold column
    var laneConfig    = determineLaneConfig(input.majorLanes, input.minorLanes);
    var thresholdInfo = determineThresholdColumn(input.speed85th, input.population, input.combinationAB || false);
    var col           = thresholdInfo.column;

    // Look up thresholds
    var condAThresholds = WARRANT1_CONDITION_A[laneConfig][col];
    var condBThresholds = WARRANT1_CONDITION_B[laneConfig][col];

    // Process hourly volumes
    var hourlyAnalysis = processHourlyVolumes(
      input.hourlyVolumes,
      laneConfig,
      col,
      condAThresholds,
      condBThresholds
    );

    // Evaluate each warrant
    var warrant1 = evaluateWarrant1(hourlyAnalysis, condAThresholds, condBThresholds);
    var warrant2 = evaluateWarrant2(hourlyAnalysis);
    var warrant3 = evaluateWarrant3(hourlyAnalysis, laneConfig, col);

    // Build summary
    var metCount = 0;
    var metList  = [];
    if (warrant1.result === WarrantResult.MET) { metCount++; metList.push('Warrant 1'); }
    if (warrant2.result === WarrantResult.MET) { metCount++; metList.push('Warrant 2'); }
    if (warrant3.result === WarrantResult.MET) { metCount++; metList.push('Warrant 3'); }

    var recommendation;
    if (metCount === 0) {
      recommendation = 'No warrants are met. A traffic signal is NOT justified based on volume warrants alone.';
    } else if (metCount === 1) {
      recommendation = metList[0] + ' is met. Installation of a traffic signal MAY be justified; engineering judgment required.';
    } else {
      recommendation = metList.join(' and ') + ' are met. Installation of a traffic signal is JUSTIFIED based on volume warrants.';
    }

    return {
      input:           input,
      laneConfig:      laneConfig,
      thresholdInfo:   thresholdInfo,
      condAThresholds: condAThresholds,
      condBThresholds: condBThresholds,
      hourlyAnalysis:  hourlyAnalysis,
      warrant1:        warrant1,
      warrant2:        warrant2,
      warrant3:        warrant3,
      summary: {
        warrantsMetCount: metCount,
        warrantsMet:      metList,
        recommendation:   recommendation
      }
    };
  }

  // ─────────────────────────────────────────────────────────────────────────────
  // VALERO / TX 82 TEST DATA
  // ─────────────────────────────────────────────────────────────────────────────

  /**
   * Synthetic 24-hour hourly volume data for the Valero / TX 82 & Public Road
   * reference case (Port Arthur, TX).
   *
   * Lane config: 2+_1 (TX 82 = 2+ lanes, Public Road = 1 lane)
   * 85th pct speed: 48 mph  →  speed > 40 → use 70% column
   * Population: 65,000       →  >= 10,000 → no population reduction
   * Threshold column: 70
   *
   * Condition A thresholds (2+_1, 70): major=420, minor=105
   * Condition B thresholds (2+_1, 70): major=630, minor=53
   *
   * Daily totals:
   *   Major (TX 82 combined): ~20,226 vpd
   *   Minor (Public Road combined): ~3,243 vpd
   *   Minor is heavily directional: ~95% NB (approach1), ~5% SB (approach2)
   *
   * Data is engineered to produce:
   *   W1 Condition A: < 8 hours meeting (major >= 420 AND minor >= 105)  → NOT MET
   *   W1 Condition B: >= 8 hours meeting (major >= 630 AND minor >= 53)  → MET
   *   Warrant 2: >= 4 hours above curve  → MET
   *   Warrant 3: at least one peak above curve  → MET
   */

  // Daily volume targets
  // Major: 20,226 total (split ~50/50 EB/WB)
  // Minor: 3,243 total (95% NB = 3,090; 5% SB = 153)
  var MAJOR_DAILY = 20226;
  var MINOR_NB    = 3090;   // approach1 (higher direction)
  var MINOR_SB    = 153;    // approach2 (lower direction)

  // Hourly K-factor distribution (fraction of daily volume per hour, index 0 = midnight)
  // Total sums to 1.0
  var MAJOR_KFACTORS = [
    0.012,  // 0  midnight
    0.008,  // 1
    0.007,  // 2
    0.007,  // 3
    0.010,  // 4
    0.020,  // 5
    0.050,  // 6
    0.082,  // 7  AM peak
    0.072,  // 8
    0.053,  // 9
    0.045,  // 10
    0.045,  // 11
    0.048,  // 12
    0.048,  // 13
    0.046,  // 14
    0.060,  // 15
    0.082,  // 16  PM peak
    0.092,  // 17  PM peak (highest)
    0.062,  // 18
    0.040,  // 19
    0.032,  // 20
    0.028,  // 21
    0.022,  // 22
    0.019   // 23
  ];
  // Sum check: these add to ~1.000

  // Minor K-factors — more peaked than major (minor street traffic is
  // concentrated in AM/PM commute).  Only 7 hours exceed K = 0.034
  // (i.e., minorHigher >= 105 VPH), so Condition A (need 8) is NOT MET.
  // Meanwhile 12+ hours exceed K = 0.017 (minor >= 53), so Condition B
  // easily has 8+ hours when combined with major >= 630.
  var MINOR_KFACTORS = [
    0.008,  // 0   →  NB ≈ 25
    0.005,  // 1   →  NB ≈ 15
    0.004,  // 2   →  NB ≈ 12
    0.004,  // 3   →  NB ≈ 12
    0.007,  // 4   →  NB ≈ 22
    0.015,  // 5   →  NB ≈ 46
    0.032,  // 6   →  NB ≈ 99   (below 105)
    0.090,  // 7   →  NB ≈ 278  (above 105) ✓
    0.075,  // 8   →  NB ≈ 232  (above 105) ✓
    0.033,  // 9   →  NB ≈ 102  (below 105)
    0.025,  // 10  →  NB ≈ 77
    0.025,  // 11  →  NB ≈ 77
    0.028,  // 12  →  NB ≈ 87
    0.027,  // 13  →  NB ≈ 83
    0.028,  // 14  →  NB ≈ 87
    0.050,  // 15  →  NB ≈ 155  (above 105) ✓
    0.100,  // 16  →  NB ≈ 309  (above 105) ✓
    0.115,  // 17  →  NB ≈ 355  (above 105) ✓
    0.060,  // 18  →  NB ≈ 185  (above 105) ✓
    0.038,  // 19  →  NB ≈ 117  (above 105) ✓
    0.025,  // 20  →  NB ≈ 77
    0.020,  // 21  →  NB ≈ 62
    0.015,  // 22  →  NB ≈ 46
    0.010   // 23  →  NB ≈ 31
  ];
  // 7 hours with minorHigher >= 105: hours 7,8,15,16,17,18,19 → Cond A NOT MET

  function buildValeroHourlyVolumes() {
    var volumes = [];
    for (var h = 0; h < 24; h++) {
      var majorTotal = Math.round(MAJOR_DAILY * MAJOR_KFACTORS[h]);
      // Split major ~50/50 between EB (approach1) and WB (approach2)
      var majorEB = Math.round(majorTotal * 0.50);
      var majorWB = majorTotal - majorEB;

      var minorNBTotal = Math.round(MINOR_NB * MINOR_KFACTORS[h]);
      var minorSBTotal = Math.round(MINOR_SB * MINOR_KFACTORS[h]);

      volumes.push({
        hour:           h,
        majorApproach1: majorEB,
        majorApproach2: majorWB,
        minorApproach1: minorNBTotal,  // NB = higher direction
        minorApproach2: minorSBTotal   // SB = lower direction
      });
    }
    return volumes;
  }

  var VALERO_TEST_DATA = {
    projectName:   'Valero / TX 82 & Public Road',
    location:      'Port Arthur, TX',
    majorStreet:   'TX 82',
    minorStreet:   'Public Road',
    majorLanes:    '2+',
    minorLanes:    '1',
    speed85th:     48,
    population:    65000,
    postedSpeed:   45,
    combinationAB: false,
    hourlyVolumes: buildValeroHourlyVolumes(),

    // Expected results (for self-test verification)
    _expected: {
      laneConfig:        '2+_1',
      thresholdColumn:   70,
      condAMajor:        420,
      condAMinor:        105,
      condBMajor:        630,
      condBMinor:        53,
      warrant1Result:    'MET',       // Condition B meets
      warrant1CondA:     'NOT MET',
      warrant1CondB:     'MET',
      warrant2Result:    'MET',
      warrant3Result:    'MET'
    }
  };

  // ─────────────────────────────────────────────────────────────────────────────
  // SELF-TEST
  // ─────────────────────────────────────────────────────────────────────────────

  /**
   * Run the Valero test case and boundary tests.
   * Returns { passed, failed, results: [] }
   */
  function runSelfTest() {
    var passed  = 0;
    var failed  = 0;
    var results = [];

    function assert(name, actual, expected) {
      var ok = (actual === expected);
      results.push({
        test:     name,
        expected: expected,
        actual:   actual,
        pass:     ok
      });
      if (ok) {
        passed++;
        console.log('[PASS] ' + name + ' — ' + actual);
      } else {
        failed++;
        console.error('[FAIL] ' + name + ' — expected: ' + expected + ', got: ' + actual);
      }
    }

    // ── Test 1: Run Valero data ────────────────────────────────────────────────
    var r = evaluateWarrants(VALERO_TEST_DATA);
    var exp = VALERO_TEST_DATA._expected;

    assert('Lane config',               r.laneConfig,                         exp.laneConfig);
    assert('Threshold column',          r.thresholdInfo.column,               exp.thresholdColumn);
    assert('Cond A major threshold',    r.condAThresholds.major,              exp.condAMajor);
    assert('Cond A minor threshold',    r.condAThresholds.minor,              exp.condAMinor);
    assert('Cond B major threshold',    r.condBThresholds.major,              exp.condBMajor);
    assert('Cond B minor threshold',    r.condBThresholds.minor,              exp.condBMinor);
    assert('Warrant 1 overall result',  r.warrant1.result,                    exp.warrant1Result);
    assert('Warrant 1 Condition A',     r.warrant1.conditionA.result,         exp.warrant1CondA);
    assert('Warrant 1 Condition B',     r.warrant1.conditionB.result,         exp.warrant1CondB);
    assert('Warrant 2 result',          r.warrant2.result,                    exp.warrant2Result);
    assert('Warrant 3 result',          r.warrant3.result,                    exp.warrant3Result);

    // Log passing hour counts for informational purposes
    console.log('  W1 Cond A hours met: ' + r.warrant1.conditionA.hoursMet + ' (need >= 8 for MET)');
    console.log('  W1 Cond B hours met: ' + r.warrant1.conditionB.hoursMet + ' (need >= 8 for MET)');
    console.log('  W2 hours above curve: ' + r.warrant2.hoursMet + ' (need >= 4 for MET)');
    console.log('  W3 AM peak (hr ' + r.warrant3.amPeak.hour + '): major=' + r.warrant3.amPeak.majorTotal + ', minorHigher=' + r.warrant3.amPeak.minorHigher + ', curveThreshold=' + r.warrant3.amPeak.curveThreshold + ', pass=' + r.warrant3.amPeak.pass);
    console.log('  W3 PM peak (hr ' + r.warrant3.pmPeak.hour + '): major=' + r.warrant3.pmPeak.majorTotal + ', minorHigher=' + r.warrant3.pmPeak.minorHigher + ', curveThreshold=' + r.warrant3.pmPeak.curveThreshold + ', pass=' + r.warrant3.pmPeak.pass);

    // ── Test 2: Boundary — exactly 8 hours pass W1B → MET ────────────────────
    (function () {
      // Build synthetic data: 8 hours that clearly pass Cond B (major=700, minorHigher=60)
      // and remaining 16 hours that clearly fail (major=100, minor=5)
      var boundaryVols = [];
      for (var h = 0; h < 24; h++) {
        if (h < 8) {
          // Pass: major 700 total (350+350), minor NB=60, SB=5
          boundaryVols.push({ hour: h, majorApproach1: 350, majorApproach2: 350, minorApproach1: 60, minorApproach2: 5 });
        } else {
          // Fail: clearly below both conditions
          boundaryVols.push({ hour: h, majorApproach1: 50,  majorApproach2: 50,  minorApproach1: 5,  minorApproach2: 2 });
        }
      }
      var boundaryInput = Object.assign({}, VALERO_TEST_DATA, { hourlyVolumes: boundaryVols, combinationAB: false });
      var rb = evaluateWarrants(boundaryInput);
      assert('Boundary 8 hrs W1B → MET', rb.warrant1.conditionB.result, WarrantResult.MET);
      assert('Boundary 8 hrs W1B → condB hoursMet', rb.warrant1.conditionB.hoursMet, 8);
    })();

    // ── Test 3: Boundary — exactly 7 hours pass W1B → NOT MET ───────────────
    (function () {
      var boundaryVols = [];
      for (var h = 0; h < 24; h++) {
        if (h < 7) {
          boundaryVols.push({ hour: h, majorApproach1: 350, majorApproach2: 350, minorApproach1: 60, minorApproach2: 5 });
        } else {
          boundaryVols.push({ hour: h, majorApproach1: 50,  majorApproach2: 50,  minorApproach1: 5,  minorApproach2: 2 });
        }
      }
      var boundaryInput = Object.assign({}, VALERO_TEST_DATA, { hourlyVolumes: boundaryVols, combinationAB: false });
      var rb = evaluateWarrants(boundaryInput);
      assert('Boundary 7 hrs W1B → NOT MET', rb.warrant1.conditionB.result, WarrantResult.NOT_MET);
      assert('Boundary 7 hrs W1B → condB hoursMet', rb.warrant1.conditionB.hoursMet, 7);
    })();

    // ── Test 4: Speed change — speed=35 → column should be 100 ──────────────
    (function () {
      var lowSpeedInput = Object.assign({}, VALERO_TEST_DATA, {
        speed85th:  35,
        population: 65000  // >= 10,000 so no pop reduction either
      });
      var rt = evaluateWarrants(lowSpeedInput);
      assert('speed=35, pop=65000 → column 100', rt.thresholdInfo.column, 100);
    })();

    // ── Test 5: Lane change — 2+/2+ → check thresholds (condA at 70%) ────────
    // When we force 2+_2+ with same speed/pop (column 70):
    // condA major=420, condA minor=140
    // condB major=630, condB minor=70
    (function () {
      var dualInput = Object.assign({}, VALERO_TEST_DATA, {
        majorLanes: '2+',
        minorLanes: '2+',
        speed85th:  48,     // > 40 → column 70
        population: 65000
      });
      var rd = evaluateWarrants(dualInput);
      assert('2+_2+ lane config', rd.laneConfig, '2+_2+');
      assert('2+_2+ col 70 condA major threshold', rd.condAThresholds.major, 420);
      assert('2+_2+ col 70 condA minor threshold', rd.condAThresholds.minor, 140);
      assert('2+_2+ col 70 condB major threshold', rd.condBThresholds.major, 630);
      assert('2+_2+ col 70 condB minor threshold', rd.condBThresholds.minor, 70);
    })();

    // ── Summary ───────────────────────────────────────────────────────────────
    console.log('\n=== SELF-TEST SUMMARY ===');
    console.log('Passed: ' + passed);
    console.log('Failed: ' + failed);
    console.log('Total:  ' + (passed + failed));

    return { passed: passed, failed: failed, results: results };
  }

  // ─────────────────────────────────────────────────────────────────────────────
  // GLOBAL EXPORT
  // ─────────────────────────────────────────────────────────────────────────────

  global.WarrantEngine = {
    evaluateWarrants:         evaluateWarrants,
    runSelfTest:              runSelfTest,
    determineThresholdColumn: determineThresholdColumn,
    determineLaneConfig:      determineLaneConfig,
    interpolateCurve:         interpolateCurve,
    processHourlyVolumes:     processHourlyVolumes,
    evaluateWarrant1:         evaluateWarrant1,
    evaluateWarrant2:         evaluateWarrant2,
    evaluateWarrant3:         evaluateWarrant3,
    VALERO_TEST_DATA:         VALERO_TEST_DATA,
    TABLES: {
      WARRANT1_CONDITION_A: WARRANT1_CONDITION_A,
      WARRANT1_CONDITION_B: WARRANT1_CONDITION_B
    },
    CURVES: {
      W2: {
        CURVE_1_1_100:   W2_CURVE_1_1_100,
        CURVE_2P_1_100:  W2_CURVE_2P_1_100,
        CURVE_2P_2P_100: W2_CURVE_2P_2P_100,
        CURVE_1_1_70:    W2_CURVE_1_1_70,
        CURVE_2P_1_70:   W2_CURVE_2P_1_70,
        CURVE_2P_2P_70:  W2_CURVE_2P_2P_70
      },
      W3: {
        CURVE_1_1_100:   W3_CURVE_1_1_100,
        CURVE_2P_1_100:  W3_CURVE_2P_1_100,
        CURVE_2P_2P_100: W3_CURVE_2P_2P_100,
        CURVE_1_1_70:    W3_CURVE_1_1_70,
        CURVE_2P_1_70:   W3_CURVE_2P_1_70,
        CURVE_2P_2P_70:  W3_CURVE_2P_2P_70
      }
    },
    ThresholdColumn: ThresholdColumn,
    LaneConfig:      LaneConfig,
    WarrantResult:   WarrantResult
  };

}(typeof window !== 'undefined' ? window : global));
