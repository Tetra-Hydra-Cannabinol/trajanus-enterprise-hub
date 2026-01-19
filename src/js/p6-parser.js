/**
 * Primavera P6 Parser Module
 * Parses XER and XML export files from Primavera P6
 * Provides Gantt chart, critical path, schedule variance, and earned value analysis
 */

// P6 Parser Core
const P6Parser = {
    // Parse XER format (tab-delimited text)
    parseXER(content) {
        const lines = content.split('\n');
        const tables = {};
        let currentTable = null;
        let columns = [];

        for (const line of lines) {
            const trimmed = line.trim();
            if (!trimmed) continue;

            const parts = trimmed.split('\t');
            const recordType = parts[0];

            if (recordType === '%T') {
                // Table definition
                currentTable = parts[1];
                tables[currentTable] = [];
                columns = [];
            } else if (recordType === '%F') {
                // Field names
                columns = parts.slice(1);
            } else if (recordType === '%R' && currentTable) {
                // Data row
                const row = {};
                parts.slice(1).forEach((value, index) => {
                    if (columns[index]) {
                        row[columns[index]] = value;
                    }
                });
                tables[currentTable].push(row);
            }
        }

        return this.transformXERData(tables);
    },

    // Transform XER tables into unified format
    transformXERData(tables) {
        const activities = [];
        const relationships = [];

        // Parse TASK table (activities)
        if (tables.TASK) {
            for (const task of tables.TASK) {
                activities.push({
                    id: task.task_id || task.task_code,
                    code: task.task_code || '',
                    name: task.task_name || '',
                    duration: parseFloat(task.target_drtn_hr_cnt || 0) / 8, // Convert hours to days
                    remainingDuration: parseFloat(task.remain_drtn_hr_cnt || 0) / 8,
                    startDate: this.parseDate(task.target_start_date || task.act_start_date),
                    finishDate: this.parseDate(task.target_end_date || task.act_end_date),
                    actualStart: this.parseDate(task.act_start_date),
                    actualFinish: this.parseDate(task.act_end_date),
                    percentComplete: parseFloat(task.phys_complete_pct || 0),
                    status: task.status_code || 'TK_NotStart',
                    totalFloat: parseFloat(task.total_float_hr_cnt || 0) / 8,
                    budgetCost: parseFloat(task.target_cost || 0),
                    actualCost: parseFloat(task.act_this_per_cost || 0),
                    wbsId: task.wbs_id || '',
                    calendarId: task.clndr_id || '',
                    isCritical: false // Will be calculated
                });
            }
        }

        // Parse TASKPRED table (relationships)
        if (tables.TASKPRED) {
            for (const pred of tables.TASKPRED) {
                relationships.push({
                    predecessorId: pred.pred_task_id,
                    successorId: pred.task_id,
                    type: this.mapRelationType(pred.pred_type),
                    lag: parseFloat(pred.lag_hr_cnt || 0) / 8
                });
            }
        }

        // Parse PROJWBS table (WBS)
        const wbs = [];
        if (tables.PROJWBS) {
            for (const w of tables.PROJWBS) {
                wbs.push({
                    id: w.wbs_id,
                    code: w.wbs_short_name || '',
                    name: w.wbs_name || '',
                    parentId: w.parent_wbs_id || null
                });
            }
        }

        return { activities, relationships, wbs };
    },

    // Parse P6 XML format
    parseXML(content) {
        const parser = new DOMParser();
        const doc = parser.parseFromString(content, 'text/xml');

        const activities = [];
        const relationships = [];
        const wbs = [];

        // Parse Activities
        const activityNodes = doc.querySelectorAll('Activity');
        activityNodes.forEach(node => {
            activities.push({
                id: this.getNodeText(node, 'ObjectId') || this.getNodeText(node, 'Id'),
                code: this.getNodeText(node, 'Id') || '',
                name: this.getNodeText(node, 'Name') || '',
                duration: parseFloat(this.getNodeText(node, 'PlannedDuration') || this.getNodeText(node, 'OriginalDuration') || 0),
                remainingDuration: parseFloat(this.getNodeText(node, 'RemainingDuration') || 0),
                startDate: this.parseDate(this.getNodeText(node, 'PlannedStartDate') || this.getNodeText(node, 'StartDate')),
                finishDate: this.parseDate(this.getNodeText(node, 'PlannedFinishDate') || this.getNodeText(node, 'FinishDate')),
                actualStart: this.parseDate(this.getNodeText(node, 'ActualStartDate')),
                actualFinish: this.parseDate(this.getNodeText(node, 'ActualFinishDate')),
                percentComplete: parseFloat(this.getNodeText(node, 'PercentComplete') || this.getNodeText(node, 'PhysicalPercentComplete') || 0),
                status: this.getNodeText(node, 'Status') || 'Not Started',
                totalFloat: parseFloat(this.getNodeText(node, 'TotalFloat') || 0),
                budgetCost: parseFloat(this.getNodeText(node, 'PlannedTotalCost') || this.getNodeText(node, 'BudgetedTotalCost') || 0),
                actualCost: parseFloat(this.getNodeText(node, 'ActualTotalCost') || 0),
                wbsId: this.getNodeText(node, 'WBSObjectId') || '',
                isCritical: false
            });
        });

        // Parse Relationships
        const relNodes = doc.querySelectorAll('Relationship');
        relNodes.forEach(node => {
            relationships.push({
                predecessorId: this.getNodeText(node, 'PredecessorActivityObjectId') || this.getNodeText(node, 'PredecessorActivityId'),
                successorId: this.getNodeText(node, 'SuccessorActivityObjectId') || this.getNodeText(node, 'SuccessorActivityId'),
                type: this.getNodeText(node, 'Type') || 'FS',
                lag: parseFloat(this.getNodeText(node, 'Lag') || 0)
            });
        });

        // Parse WBS
        const wbsNodes = doc.querySelectorAll('WBS');
        wbsNodes.forEach(node => {
            wbs.push({
                id: this.getNodeText(node, 'ObjectId') || this.getNodeText(node, 'Id'),
                code: this.getNodeText(node, 'Code') || '',
                name: this.getNodeText(node, 'Name') || '',
                parentId: this.getNodeText(node, 'ParentObjectId') || null
            });
        });

        return { activities, relationships, wbs };
    },

    // Helper: Get text content from XML node
    getNodeText(parent, tagName) {
        const node = parent.querySelector(tagName);
        return node ? node.textContent : null;
    },

    // Helper: Parse date string
    parseDate(dateStr) {
        if (!dateStr) return null;
        // Handle various P6 date formats
        const date = new Date(dateStr);
        return isNaN(date.getTime()) ? null : date;
    },

    // Helper: Map XER relationship type to standard
    mapRelationType(xerType) {
        const typeMap = {
            'PR_FS': 'FS',
            'PR_FF': 'FF',
            'PR_SS': 'SS',
            'PR_SF': 'SF'
        };
        return typeMap[xerType] || xerType || 'FS';
    },

    // Detect file format and parse
    parse(content, filename = '') {
        const ext = filename.toLowerCase().split('.').pop();

        if (ext === 'xer' || content.startsWith('ERMHDR')) {
            return this.parseXER(content);
        } else if (ext === 'xml' || content.trim().startsWith('<?xml') || content.trim().startsWith('<')) {
            return this.parseXML(content);
        } else {
            // Try to auto-detect
            if (content.includes('%T\t') && content.includes('%F\t')) {
                return this.parseXER(content);
            }
            return this.parseXML(content);
        }
    }
};

// Critical Path Calculator
const CriticalPathAnalyzer = {
    analyze(activities, relationships) {
        if (!activities.length) return { criticalPath: [], projectDuration: 0 };

        // Build adjacency lists
        const successors = {};
        const predecessors = {};
        const activityMap = {};

        activities.forEach(act => {
            activityMap[act.id] = { ...act, ES: 0, EF: 0, LS: Infinity, LF: Infinity };
            successors[act.id] = [];
            predecessors[act.id] = [];
        });

        relationships.forEach(rel => {
            if (activityMap[rel.predecessorId] && activityMap[rel.successorId]) {
                successors[rel.predecessorId].push({ id: rel.successorId, type: rel.type, lag: rel.lag });
                predecessors[rel.successorId].push({ id: rel.predecessorId, type: rel.type, lag: rel.lag });
            }
        });

        // Forward pass (calculate Early Start and Early Finish)
        const sorted = this.topologicalSort(Object.keys(activityMap), predecessors);

        sorted.forEach(actId => {
            const act = activityMap[actId];
            let maxES = 0;

            predecessors[actId].forEach(pred => {
                const predAct = activityMap[pred.id];
                let es = 0;

                switch (pred.type) {
                    case 'FS': es = predAct.EF + pred.lag; break;
                    case 'SS': es = predAct.ES + pred.lag; break;
                    case 'FF': es = predAct.EF + pred.lag - act.duration; break;
                    case 'SF': es = predAct.ES + pred.lag - act.duration; break;
                    default: es = predAct.EF + pred.lag;
                }

                maxES = Math.max(maxES, es);
            });

            act.ES = maxES;
            act.EF = act.ES + act.duration;
        });

        // Find project end date
        let projectDuration = 0;
        Object.values(activityMap).forEach(act => {
            projectDuration = Math.max(projectDuration, act.EF);
        });

        // Backward pass (calculate Late Start and Late Finish)
        sorted.reverse().forEach(actId => {
            const act = activityMap[actId];

            if (successors[actId].length === 0) {
                act.LF = projectDuration;
            } else {
                let minLF = Infinity;
                successors[actId].forEach(succ => {
                    const succAct = activityMap[succ.id];
                    let lf = Infinity;

                    switch (succ.type) {
                        case 'FS': lf = succAct.LS - succ.lag; break;
                        case 'SS': lf = succAct.LS - succ.lag + act.duration; break;
                        case 'FF': lf = succAct.LF - succ.lag; break;
                        case 'SF': lf = succAct.LF - succ.lag + act.duration; break;
                        default: lf = succAct.LS - succ.lag;
                    }

                    minLF = Math.min(minLF, lf);
                });
                act.LF = minLF;
            }

            act.LS = act.LF - act.duration;
            act.totalFloat = act.LS - act.ES;
            act.isCritical = Math.abs(act.totalFloat) < 0.01;
        });

        // Extract critical path
        const criticalPath = Object.values(activityMap)
            .filter(act => act.isCritical)
            .sort((a, b) => a.ES - b.ES);

        return {
            activities: Object.values(activityMap),
            criticalPath,
            projectDuration
        };
    },

    topologicalSort(nodes, predecessors) {
        const visited = new Set();
        const result = [];
        const visiting = new Set();

        const visit = (node) => {
            if (visited.has(node)) return;
            if (visiting.has(node)) return; // Cycle detected

            visiting.add(node);
            predecessors[node].forEach(pred => visit(pred.id));
            visiting.delete(node);
            visited.add(node);
            result.push(node);
        };

        nodes.forEach(node => visit(node));
        return result;
    }
};

// Schedule Variance Calculator
const ScheduleAnalyzer = {
    calculate(activities, dataDate = new Date()) {
        const results = {
            onSchedule: [],
            ahead: [],
            behind: [],
            completed: [],
            notStarted: [],
            summary: {
                totalActivities: activities.length,
                completedCount: 0,
                inProgressCount: 0,
                notStartedCount: 0,
                behindCount: 0,
                aheadCount: 0,
                avgVarianceDays: 0
            }
        };

        let totalVariance = 0;
        let varianceCount = 0;

        activities.forEach(act => {
            const plannedStart = act.startDate;
            const plannedFinish = act.finishDate;
            const actualStart = act.actualStart;
            const actualFinish = act.actualFinish;
            const percentComplete = act.percentComplete || 0;

            // Calculate variance in days
            let startVariance = 0;
            let finishVariance = 0;

            if (percentComplete >= 100 || actualFinish) {
                results.completed.push(act);
                results.summary.completedCount++;

                if (actualFinish && plannedFinish) {
                    finishVariance = (plannedFinish - actualFinish) / (1000 * 60 * 60 * 24);
                }
            } else if (percentComplete > 0 || actualStart) {
                results.summary.inProgressCount++;

                // Calculate expected progress
                if (plannedStart && plannedFinish) {
                    const totalDuration = (plannedFinish - plannedStart) / (1000 * 60 * 60 * 24);
                    const elapsedDuration = (dataDate - plannedStart) / (1000 * 60 * 60 * 24);
                    const expectedProgress = Math.min(100, (elapsedDuration / totalDuration) * 100);

                    const progressVariance = percentComplete - expectedProgress;

                    if (progressVariance < -5) {
                        results.behind.push({ ...act, variance: progressVariance });
                        results.summary.behindCount++;
                    } else if (progressVariance > 5) {
                        results.ahead.push({ ...act, variance: progressVariance });
                        results.summary.aheadCount++;
                    } else {
                        results.onSchedule.push({ ...act, variance: progressVariance });
                    }

                    totalVariance += progressVariance;
                    varianceCount++;
                }
            } else {
                results.notStarted.push(act);
                results.summary.notStartedCount++;

                // Check if should have started
                if (plannedStart && plannedStart < dataDate) {
                    results.behind.push({ ...act, variance: -100 });
                    results.summary.behindCount++;
                }
            }
        });

        results.summary.avgVarianceDays = varianceCount > 0 ? totalVariance / varianceCount : 0;

        return results;
    }
};

// Earned Value Calculator
const EarnedValueAnalyzer = {
    calculate(activities, dataDate = new Date()) {
        let BAC = 0;  // Budget at Completion
        let PV = 0;   // Planned Value
        let EV = 0;   // Earned Value
        let AC = 0;   // Actual Cost

        activities.forEach(act => {
            const budget = act.budgetCost || 0;
            const actual = act.actualCost || 0;
            const percentComplete = (act.percentComplete || 0) / 100;

            BAC += budget;
            AC += actual;
            EV += budget * percentComplete;

            // Calculate planned value based on schedule
            if (act.startDate && act.finishDate) {
                const totalDuration = act.finishDate - act.startDate;
                const elapsed = Math.max(0, Math.min(dataDate - act.startDate, totalDuration));
                const plannedProgress = totalDuration > 0 ? elapsed / totalDuration : 0;
                PV += budget * plannedProgress;
            }
        });

        // Calculate EVM metrics
        const SV = EV - PV;              // Schedule Variance ($)
        const CV = EV - AC;              // Cost Variance ($)
        const SPI = PV > 0 ? EV / PV : 1; // Schedule Performance Index
        const CPI = AC > 0 ? EV / AC : 1; // Cost Performance Index
        const EAC = CPI > 0 ? BAC / CPI : BAC; // Estimate at Completion
        const ETC = EAC - AC;            // Estimate to Complete
        const VAC = BAC - EAC;           // Variance at Completion
        const TCPI = (BAC - EV) / (BAC - AC); // To-Complete Performance Index

        return {
            BAC: Math.round(BAC),
            PV: Math.round(PV),
            EV: Math.round(EV),
            AC: Math.round(AC),
            SV: Math.round(SV),
            CV: Math.round(CV),
            SPI: Math.round(SPI * 100) / 100,
            CPI: Math.round(CPI * 100) / 100,
            EAC: Math.round(EAC),
            ETC: Math.round(ETC),
            VAC: Math.round(VAC),
            TCPI: Math.round(TCPI * 100) / 100,
            percentComplete: BAC > 0 ? Math.round((EV / BAC) * 100) : 0,
            percentSpent: BAC > 0 ? Math.round((AC / BAC) * 100) : 0
        };
    }
};

// Gantt Chart Renderer
const GanttRenderer = {
    render(containerId, activities, options = {}) {
        const container = document.getElementById(containerId);
        if (!container) return;

        const {
            showCriticalPath = true,
            daysPerPixel = 2,
            rowHeight = 32,
            headerHeight = 50
        } = options;

        // Find date range
        let minDate = null;
        let maxDate = null;

        activities.forEach(act => {
            if (act.startDate) {
                if (!minDate || act.startDate < minDate) minDate = act.startDate;
            }
            if (act.finishDate) {
                if (!maxDate || act.finishDate > maxDate) maxDate = act.finishDate;
            }
        });

        if (!minDate || !maxDate) {
            container.innerHTML = '<div class="gantt-empty">No schedule data available</div>';
            return;
        }

        // Add padding
        minDate = new Date(minDate.getTime() - 7 * 24 * 60 * 60 * 1000);
        maxDate = new Date(maxDate.getTime() + 7 * 24 * 60 * 60 * 1000);

        const totalDays = Math.ceil((maxDate - minDate) / (1000 * 60 * 60 * 24));
        const chartWidth = totalDays * daysPerPixel;
        const chartHeight = activities.length * rowHeight + headerHeight;

        // Generate HTML
        let html = `
            <div class="gantt-container">
                <div class="gantt-header-row">
                    <div class="gantt-activity-header">Activity</div>
                    <div class="gantt-timeline-header" style="width: ${chartWidth}px;">
                        ${this.renderTimelineHeader(minDate, maxDate, daysPerPixel)}
                    </div>
                </div>
                <div class="gantt-body">
                    <div class="gantt-activity-list">
                        ${activities.map((act, i) => `
                            <div class="gantt-activity-row ${act.isCritical ? 'critical' : ''}" style="height: ${rowHeight}px;">
                                <span class="gantt-activity-code">${act.code || act.id}</span>
                                <span class="gantt-activity-name">${act.name}</span>
                            </div>
                        `).join('')}
                    </div>
                    <div class="gantt-chart-area" style="width: ${chartWidth}px;">
                        ${this.renderGridLines(minDate, maxDate, activities.length, rowHeight, daysPerPixel)}
                        ${activities.map((act, i) => this.renderBar(act, i, minDate, daysPerPixel, rowHeight)).join('')}
                        ${this.renderTodayLine(minDate, new Date(), daysPerPixel, activities.length * rowHeight)}
                    </div>
                </div>
            </div>
        `;

        container.innerHTML = html;
    },

    renderTimelineHeader(minDate, maxDate, daysPerPixel) {
        let html = '<div class="gantt-months">';
        let current = new Date(minDate);
        current.setDate(1);

        while (current < maxDate) {
            const monthStart = new Date(current);
            const monthEnd = new Date(current.getFullYear(), current.getMonth() + 1, 0);
            const daysInView = Math.min(
                (monthEnd - Math.max(monthStart, minDate)) / (1000 * 60 * 60 * 24),
                (Math.min(monthEnd, maxDate) - Math.max(monthStart, minDate)) / (1000 * 60 * 60 * 24)
            );
            const width = Math.max(0, daysInView * daysPerPixel);

            if (width > 30) {
                const monthName = current.toLocaleString('default', { month: 'short', year: 'numeric' });
                html += `<div class="gantt-month" style="width: ${width}px;">${monthName}</div>`;
            }

            current.setMonth(current.getMonth() + 1);
        }

        html += '</div>';
        return html;
    },

    renderGridLines(minDate, maxDate, rowCount, rowHeight, daysPerPixel) {
        let html = '';
        let current = new Date(minDate);

        // Weekly grid lines
        while (current < maxDate) {
            const dayOfWeek = current.getDay();
            if (dayOfWeek === 0) { // Sunday
                const x = ((current - minDate) / (1000 * 60 * 60 * 24)) * daysPerPixel;
                html += `<div class="gantt-grid-line" style="left: ${x}px; height: ${rowCount * rowHeight}px;"></div>`;
            }
            current.setDate(current.getDate() + 1);
        }

        return html;
    },

    renderBar(activity, index, minDate, daysPerPixel, rowHeight) {
        if (!activity.startDate || !activity.finishDate) return '';

        const startOffset = ((activity.startDate - minDate) / (1000 * 60 * 60 * 24)) * daysPerPixel;
        const duration = ((activity.finishDate - activity.startDate) / (1000 * 60 * 60 * 24)) * daysPerPixel;
        const top = index * rowHeight + 6;
        const height = rowHeight - 12;
        const progress = activity.percentComplete || 0;

        const barClass = activity.isCritical ? 'gantt-bar critical' : 'gantt-bar';

        return `
            <div class="${barClass}" style="left: ${startOffset}px; width: ${Math.max(duration, 4)}px; top: ${top}px; height: ${height}px;"
                 title="${activity.name} (${progress}%)">
                <div class="gantt-bar-progress" style="width: ${progress}%;"></div>
                ${duration > 50 ? `<span class="gantt-bar-label">${progress}%</span>` : ''}
            </div>
        `;
    },

    renderTodayLine(minDate, today, daysPerPixel, height) {
        const x = ((today - minDate) / (1000 * 60 * 60 * 24)) * daysPerPixel;
        return `<div class="gantt-today-line" style="left: ${x}px; height: ${height}px;"></div>`;
    }
};

// P6 Workspace UI Controller
class P6Workspace {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.data = null;
        this.analyzedData = null;
        this.render();
    }

    render() {
        if (!this.container) return;

        this.container.innerHTML = `
            <div class="p6-workspace">
                <div class="p6-header">
                    <h3>P6 Schedule Analyzer</h3>
                    <div class="p6-actions">
                        <input type="file" id="p6-file-input" accept=".xer,.xml" style="display: none;">
                        <button class="p6-btn p6-btn-primary" id="p6-upload-btn">
                            <span class="btn-icon">📂</span> Import P6 File
                        </button>
                        <button class="p6-btn" id="p6-sample-btn">
                            <span class="btn-icon">📋</span> Load Sample
                        </button>
                    </div>
                </div>

                <div class="p6-tabs">
                    <button class="p6-tab active" data-tab="gantt">Gantt Chart</button>
                    <button class="p6-tab" data-tab="critical">Critical Path</button>
                    <button class="p6-tab" data-tab="variance">Schedule Variance</button>
                    <button class="p6-tab" data-tab="evm">Earned Value</button>
                </div>

                <div class="p6-content">
                    <div class="p6-tab-content active" id="p6-gantt">
                        <div class="p6-placeholder">
                            <span class="placeholder-icon">📊</span>
                            <p>Import a P6 XER or XML file to view the Gantt chart</p>
                        </div>
                    </div>
                    <div class="p6-tab-content" id="p6-critical">
                        <div class="p6-placeholder">
                            <span class="placeholder-icon">🎯</span>
                            <p>Critical path will be calculated after import</p>
                        </div>
                    </div>
                    <div class="p6-tab-content" id="p6-variance">
                        <div class="p6-placeholder">
                            <span class="placeholder-icon">📈</span>
                            <p>Schedule variance analysis will appear here</p>
                        </div>
                    </div>
                    <div class="p6-tab-content" id="p6-evm">
                        <div class="p6-placeholder">
                            <span class="placeholder-icon">💰</span>
                            <p>Earned value metrics will be calculated after import</p>
                        </div>
                    </div>
                </div>

                <div class="p6-status-bar" id="p6-status">
                    Ready - Import a P6 file to begin analysis
                </div>
            </div>
        `;

        this.bindEvents();
    }

    bindEvents() {
        // File upload
        const uploadBtn = this.container.querySelector('#p6-upload-btn');
        const fileInput = this.container.querySelector('#p6-file-input');

        uploadBtn?.addEventListener('click', () => fileInput.click());
        fileInput?.addEventListener('change', (e) => this.handleFileUpload(e));

        // Sample data
        const sampleBtn = this.container.querySelector('#p6-sample-btn');
        sampleBtn?.addEventListener('click', () => this.loadSampleData());

        // Tab switching
        this.container.querySelectorAll('.p6-tab').forEach(tab => {
            tab.addEventListener('click', (e) => this.switchTab(e.target.dataset.tab));
        });
    }

    async handleFileUpload(event) {
        const file = event.target.files[0];
        if (!file) return;

        this.setStatus('Loading file...');

        try {
            const content = await file.text();
            this.data = P6Parser.parse(content, file.name);
            this.processData();
            this.setStatus(`Loaded ${this.data.activities.length} activities from ${file.name}`);
        } catch (error) {
            console.error('Parse error:', error);
            this.setStatus('Error parsing file: ' + error.message);
        }
    }

    loadSampleData() {
        // Generate sample construction project data
        const today = new Date();
        const startDate = new Date(today);
        startDate.setDate(startDate.getDate() - 30);

        this.data = {
            activities: [
                { id: '1', code: 'A1000', name: 'Mobilization', duration: 5, startDate: new Date(startDate), finishDate: this.addDays(startDate, 5), percentComplete: 100, budgetCost: 25000, actualCost: 24000 },
                { id: '2', code: 'A1010', name: 'Site Preparation', duration: 10, startDate: this.addDays(startDate, 5), finishDate: this.addDays(startDate, 15), percentComplete: 100, budgetCost: 75000, actualCost: 78000 },
                { id: '3', code: 'A1020', name: 'Foundation Excavation', duration: 8, startDate: this.addDays(startDate, 15), finishDate: this.addDays(startDate, 23), percentComplete: 100, budgetCost: 45000, actualCost: 44000 },
                { id: '4', code: 'A1030', name: 'Foundation Concrete', duration: 12, startDate: this.addDays(startDate, 23), finishDate: this.addDays(startDate, 35), percentComplete: 85, budgetCost: 120000, actualCost: 95000 },
                { id: '5', code: 'A1040', name: 'Structural Steel', duration: 20, startDate: this.addDays(startDate, 35), finishDate: this.addDays(startDate, 55), percentComplete: 40, budgetCost: 250000, actualCost: 85000 },
                { id: '6', code: 'A1050', name: 'Metal Deck', duration: 10, startDate: this.addDays(startDate, 45), finishDate: this.addDays(startDate, 55), percentComplete: 20, budgetCost: 80000, actualCost: 15000 },
                { id: '7', code: 'A1060', name: 'Concrete Slab', duration: 15, startDate: this.addDays(startDate, 55), finishDate: this.addDays(startDate, 70), percentComplete: 0, budgetCost: 95000, actualCost: 0 },
                { id: '8', code: 'A1070', name: 'Exterior Walls', duration: 25, startDate: this.addDays(startDate, 55), finishDate: this.addDays(startDate, 80), percentComplete: 0, budgetCost: 180000, actualCost: 0 },
                { id: '9', code: 'A1080', name: 'Roofing', duration: 12, startDate: this.addDays(startDate, 70), finishDate: this.addDays(startDate, 82), percentComplete: 0, budgetCost: 65000, actualCost: 0 },
                { id: '10', code: 'A1090', name: 'MEP Rough-In', duration: 30, startDate: this.addDays(startDate, 70), finishDate: this.addDays(startDate, 100), percentComplete: 0, budgetCost: 220000, actualCost: 0 },
                { id: '11', code: 'A1100', name: 'Interior Finishes', duration: 25, startDate: this.addDays(startDate, 82), finishDate: this.addDays(startDate, 107), percentComplete: 0, budgetCost: 150000, actualCost: 0 },
                { id: '12', code: 'A1110', name: 'Punch List', duration: 10, startDate: this.addDays(startDate, 107), finishDate: this.addDays(startDate, 117), percentComplete: 0, budgetCost: 25000, actualCost: 0 }
            ],
            relationships: [
                { predecessorId: '1', successorId: '2', type: 'FS', lag: 0 },
                { predecessorId: '2', successorId: '3', type: 'FS', lag: 0 },
                { predecessorId: '3', successorId: '4', type: 'FS', lag: 0 },
                { predecessorId: '4', successorId: '5', type: 'FS', lag: 0 },
                { predecessorId: '5', successorId: '6', type: 'SS', lag: 10 },
                { predecessorId: '5', successorId: '7', type: 'FS', lag: 0 },
                { predecessorId: '5', successorId: '8', type: 'FS', lag: 0 },
                { predecessorId: '7', successorId: '9', type: 'FS', lag: 0 },
                { predecessorId: '7', successorId: '10', type: 'FS', lag: 0 },
                { predecessorId: '9', successorId: '11', type: 'FS', lag: 0 },
                { predecessorId: '10', successorId: '11', type: 'FF', lag: 0 },
                { predecessorId: '11', successorId: '12', type: 'FS', lag: 0 }
            ],
            wbs: []
        };

        this.processData();
        this.setStatus('Loaded sample construction project (12 activities)');
    }

    addDays(date, days) {
        const result = new Date(date);
        result.setDate(result.getDate() + days);
        return result;
    }

    processData() {
        if (!this.data) return;

        // Run critical path analysis
        const cpResult = CriticalPathAnalyzer.analyze(this.data.activities, this.data.relationships);
        this.analyzedData = {
            activities: cpResult.activities,
            criticalPath: cpResult.criticalPath,
            projectDuration: cpResult.projectDuration,
            scheduleVariance: ScheduleAnalyzer.calculate(cpResult.activities),
            earnedValue: EarnedValueAnalyzer.calculate(cpResult.activities)
        };

        // Update all views
        this.renderGantt();
        this.renderCriticalPath();
        this.renderVariance();
        this.renderEVM();
    }

    renderGantt() {
        const container = this.container.querySelector('#p6-gantt');
        container.innerHTML = '<div id="p6-gantt-chart"></div>';
        GanttRenderer.render('p6-gantt-chart', this.analyzedData.activities, { showCriticalPath: true });
    }

    renderCriticalPath() {
        const container = this.container.querySelector('#p6-critical');
        const cp = this.analyzedData.criticalPath;
        const duration = this.analyzedData.projectDuration;

        container.innerHTML = `
            <div class="critical-path-view">
                <div class="cp-summary">
                    <div class="cp-metric">
                        <span class="cp-value">${cp.length}</span>
                        <span class="cp-label">Critical Activities</span>
                    </div>
                    <div class="cp-metric">
                        <span class="cp-value">${Math.round(duration)}</span>
                        <span class="cp-label">Project Duration (days)</span>
                    </div>
                    <div class="cp-metric">
                        <span class="cp-value">${Math.round((cp.length / this.analyzedData.activities.length) * 100)}%</span>
                        <span class="cp-label">Critical Percentage</span>
                    </div>
                </div>
                <div class="cp-path">
                    <h4>Critical Path Sequence</h4>
                    <div class="cp-sequence">
                        ${cp.map((act, i) => `
                            <div class="cp-activity">
                                <span class="cp-code">${act.code || act.id}</span>
                                <span class="cp-name">${act.name}</span>
                                <span class="cp-duration">${act.duration}d</span>
                            </div>
                            ${i < cp.length - 1 ? '<span class="cp-arrow">→</span>' : ''}
                        `).join('')}
                    </div>
                </div>
                <div class="cp-table">
                    <h4>Critical Activities Detail</h4>
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Activity</th>
                                <th>Duration</th>
                                <th>ES</th>
                                <th>EF</th>
                                <th>LS</th>
                                <th>LF</th>
                                <th>Float</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${cp.map(act => `
                                <tr>
                                    <td>${act.code || act.id}</td>
                                    <td>${act.name}</td>
                                    <td>${act.duration}d</td>
                                    <td>${Math.round(act.ES)}</td>
                                    <td>${Math.round(act.EF)}</td>
                                    <td>${Math.round(act.LS)}</td>
                                    <td>${Math.round(act.LF)}</td>
                                    <td>${Math.round(act.totalFloat)}</td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            </div>
        `;
    }

    renderVariance() {
        const container = this.container.querySelector('#p6-variance');
        const sv = this.analyzedData.scheduleVariance;

        container.innerHTML = `
            <div class="variance-view">
                <div class="variance-summary">
                    <div class="variance-card good">
                        <span class="variance-count">${sv.summary.completedCount}</span>
                        <span class="variance-label">Completed</span>
                    </div>
                    <div class="variance-card neutral">
                        <span class="variance-count">${sv.onSchedule.length}</span>
                        <span class="variance-label">On Schedule</span>
                    </div>
                    <div class="variance-card ahead">
                        <span class="variance-count">${sv.summary.aheadCount}</span>
                        <span class="variance-label">Ahead</span>
                    </div>
                    <div class="variance-card behind">
                        <span class="variance-count">${sv.summary.behindCount}</span>
                        <span class="variance-label">Behind</span>
                    </div>
                    <div class="variance-card">
                        <span class="variance-count">${sv.summary.notStartedCount}</span>
                        <span class="variance-label">Not Started</span>
                    </div>
                </div>

                ${sv.behind.length > 0 ? `
                <div class="variance-section">
                    <h4>Behind Schedule Activities</h4>
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Activity</th>
                                <th>Progress</th>
                                <th>Variance</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${sv.behind.map(act => `
                                <tr class="behind-row">
                                    <td>${act.code || act.id}</td>
                                    <td>${act.name}</td>
                                    <td>${act.percentComplete || 0}%</td>
                                    <td>${Math.round(act.variance || 0)}%</td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
                ` : ''}

                ${sv.ahead.length > 0 ? `
                <div class="variance-section">
                    <h4>Ahead of Schedule Activities</h4>
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Activity</th>
                                <th>Progress</th>
                                <th>Variance</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${sv.ahead.map(act => `
                                <tr class="ahead-row">
                                    <td>${act.code || act.id}</td>
                                    <td>${act.name}</td>
                                    <td>${act.percentComplete || 0}%</td>
                                    <td>+${Math.round(act.variance || 0)}%</td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
                ` : ''}
            </div>
        `;
    }

    renderEVM() {
        const container = this.container.querySelector('#p6-evm');
        const evm = this.analyzedData.earnedValue;

        const formatCurrency = (val) => '$' + val.toLocaleString();
        const getIndicatorClass = (value, threshold = 1) => {
            if (value >= threshold) return 'good';
            if (value >= threshold * 0.9) return 'warning';
            return 'bad';
        };

        container.innerHTML = `
            <div class="evm-view">
                <div class="evm-metrics">
                    <div class="evm-card">
                        <span class="evm-label">Budget at Completion (BAC)</span>
                        <span class="evm-value">${formatCurrency(evm.BAC)}</span>
                    </div>
                    <div class="evm-card">
                        <span class="evm-label">Planned Value (PV)</span>
                        <span class="evm-value">${formatCurrency(evm.PV)}</span>
                    </div>
                    <div class="evm-card">
                        <span class="evm-label">Earned Value (EV)</span>
                        <span class="evm-value">${formatCurrency(evm.EV)}</span>
                    </div>
                    <div class="evm-card">
                        <span class="evm-label">Actual Cost (AC)</span>
                        <span class="evm-value">${formatCurrency(evm.AC)}</span>
                    </div>
                </div>

                <div class="evm-variances">
                    <div class="evm-variance ${evm.SV >= 0 ? 'positive' : 'negative'}">
                        <span class="evm-label">Schedule Variance (SV)</span>
                        <span class="evm-value">${evm.SV >= 0 ? '+' : ''}${formatCurrency(evm.SV)}</span>
                    </div>
                    <div class="evm-variance ${evm.CV >= 0 ? 'positive' : 'negative'}">
                        <span class="evm-label">Cost Variance (CV)</span>
                        <span class="evm-value">${evm.CV >= 0 ? '+' : ''}${formatCurrency(evm.CV)}</span>
                    </div>
                </div>

                <div class="evm-indices">
                    <div class="evm-index ${getIndicatorClass(evm.SPI)}">
                        <span class="evm-index-value">${evm.SPI}</span>
                        <span class="evm-index-label">SPI</span>
                        <span class="evm-index-desc">${evm.SPI >= 1 ? 'On/Ahead Schedule' : 'Behind Schedule'}</span>
                    </div>
                    <div class="evm-index ${getIndicatorClass(evm.CPI)}">
                        <span class="evm-index-value">${evm.CPI}</span>
                        <span class="evm-index-label">CPI</span>
                        <span class="evm-index-desc">${evm.CPI >= 1 ? 'Under Budget' : 'Over Budget'}</span>
                    </div>
                </div>

                <div class="evm-forecasts">
                    <h4>Forecasts</h4>
                    <div class="evm-forecast-grid">
                        <div class="evm-forecast">
                            <span class="evm-label">Estimate at Completion (EAC)</span>
                            <span class="evm-value">${formatCurrency(evm.EAC)}</span>
                        </div>
                        <div class="evm-forecast">
                            <span class="evm-label">Estimate to Complete (ETC)</span>
                            <span class="evm-value">${formatCurrency(evm.ETC)}</span>
                        </div>
                        <div class="evm-forecast ${evm.VAC >= 0 ? 'positive' : 'negative'}">
                            <span class="evm-label">Variance at Completion (VAC)</span>
                            <span class="evm-value">${evm.VAC >= 0 ? '+' : ''}${formatCurrency(evm.VAC)}</span>
                        </div>
                        <div class="evm-forecast">
                            <span class="evm-label">To-Complete Performance Index (TCPI)</span>
                            <span class="evm-value">${isFinite(evm.TCPI) ? evm.TCPI : 'N/A'}</span>
                        </div>
                    </div>
                </div>

                <div class="evm-progress">
                    <h4>Project Progress</h4>
                    <div class="progress-bars">
                        <div class="progress-item">
                            <span class="progress-label">Work Complete</span>
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: ${evm.percentComplete}%"></div>
                            </div>
                            <span class="progress-value">${evm.percentComplete}%</span>
                        </div>
                        <div class="progress-item">
                            <span class="progress-label">Budget Spent</span>
                            <div class="progress-bar">
                                <div class="progress-fill ${evm.percentSpent > evm.percentComplete ? 'over' : ''}" style="width: ${Math.min(evm.percentSpent, 100)}%"></div>
                            </div>
                            <span class="progress-value">${evm.percentSpent}%</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    switchTab(tabId) {
        // Update tab buttons
        this.container.querySelectorAll('.p6-tab').forEach(tab => {
            tab.classList.toggle('active', tab.dataset.tab === tabId);
        });

        // Update content panels
        this.container.querySelectorAll('.p6-tab-content').forEach(content => {
            content.classList.toggle('active', content.id === `p6-${tabId}`);
        });
    }

    setStatus(message) {
        const statusBar = this.container.querySelector('#p6-status');
        if (statusBar) statusBar.textContent = message;
    }
}

// Export for use
window.P6Parser = P6Parser;
window.CriticalPathAnalyzer = CriticalPathAnalyzer;
window.ScheduleAnalyzer = ScheduleAnalyzer;
window.EarnedValueAnalyzer = EarnedValueAnalyzer;
window.GanttRenderer = GanttRenderer;
window.P6Workspace = P6Workspace;
