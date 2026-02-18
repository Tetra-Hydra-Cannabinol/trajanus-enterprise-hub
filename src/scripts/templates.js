// Trajanus Enterprise Hub - Templates

const Templates = {
    currentTemplate: null,
    currentMode: 'production',

    definitions: {
        pm: {
            name: 'PM Toolkit',
            templates: [
                { id: 'rfi-response', name: 'RFI Response', prompt: 'Generate a professional RFI response based on the provided documents. Include clear answers, references to specifications, and any required clarifications.' },
                { id: 'submittal-review', name: 'Submittal Review', prompt: 'Review the submittal package for compliance with specifications and contract requirements. Identify any discrepancies, missing information, or items requiring clarification.' },
                { id: 'schedule-analysis', name: 'Schedule Analysis', prompt: 'Analyze the project schedule for critical path items, potential delays, and resource conflicts. Provide recommendations for optimization.' },
                { id: 'cost-report', name: 'Cost Report', prompt: 'Generate a cost report summarizing budget status, variances, and forecasts. Include breakdown by category and trend analysis.' },
                { id: 'meeting-minutes', name: 'Meeting Minutes', prompt: 'Create professional meeting minutes from the provided notes. Include attendees, action items, decisions made, and next steps.' },
                { id: 'progress-report', name: 'Progress Report', prompt: 'Generate a progress report covering work completed, upcoming activities, issues, and overall project status.' },
                { id: 'change-order', name: 'Change Order Analysis', prompt: 'Analyze the proposed change order for cost and schedule impact. Evaluate justification and provide recommendations.' }
            ]
        },
        traffic: {
            name: 'Traffic Studies',
            templates: [
                { id: 'trip-generation', name: 'Trip Generation Calculation', prompt: 'Calculate trip generation using ITE Trip Generation Manual methodology. Include peak hour and daily trip estimates with appropriate rates and adjustments.' },
                { id: 'tis-outline', name: 'TIS Report Outline', prompt: 'Generate a Traffic Impact Study outline following standard methodology. Include all required sections for jurisdiction approval.' },
                { id: 'los-analysis', name: 'LOS Analysis', prompt: 'Perform Level of Service analysis for the intersection or roadway segment. Calculate delays, queue lengths, and provide LOS grades.' },
                { id: 'dot-compliance', name: 'State DOT Compliance Check', prompt: 'Review the traffic study for compliance with State DOT requirements. Identify any missing elements or non-conforming analyses.' },
                { id: 'traffic-count', name: 'Traffic Count Summary', prompt: 'Summarize traffic count data including peak hours, daily volumes, and seasonal adjustment factors.' },
                { id: 'intersection-analysis', name: 'Intersection Analysis', prompt: 'Analyze intersection operations including capacity, signal timing, and geometric adequacy. Provide improvement recommendations.' }
            ]
        },
        developer: {
            name: 'Developer Toolkit',
            templates: [
                { id: 'session-summary', name: 'Session Summary', prompt: 'Create a summary of the development session including tasks completed, decisions made, and items for follow-up.' },
                { id: 'technical-journal', name: 'Technical Journal', prompt: 'Document technical findings, solutions implemented, and lessons learned for future reference.' },
                { id: 'handoff-doc', name: 'Handoff Document', prompt: 'Generate a handoff document for transitioning work to another developer. Include context, current status, and next steps.' },
                { id: 'code-review', name: 'Code Review', prompt: 'Review the provided code for quality, best practices, security issues, and potential improvements.' },
                { id: 'kb-query', name: 'KB Query', prompt: 'Search the knowledge base and synthesize relevant information to answer the query.' },
                { id: 'agent-status', name: 'Agent Status Report', prompt: 'Generate a status report for agent activities including tasks completed, errors encountered, and performance metrics.' }
            ]
        },
        qcm: {
            name: 'QCM Toolkit',
            templates: [
                { id: 'submittal-3phase', name: 'Submittal Review (3-Phase)', prompt: 'Perform a 3-phase submittal review: preparatory, initial, and follow-up. Document findings and required corrections for each phase.' },
                { id: 'inspection-report', name: 'Inspection Report', prompt: 'Generate an inspection report documenting observations, measurements, and compliance status. Include photos and corrective actions if needed.' },
                { id: 'deficiency-log', name: 'Deficiency Log Entry', prompt: 'Create a deficiency log entry with detailed description, location, responsible party, and required corrective action.' },
                { id: 'qc-checklist', name: 'QC Checklist', prompt: 'Generate a QC checklist for the specified work activity. Include all inspection points and acceptance criteria.' },
                { id: 'material-approval', name: 'Material Approval', prompt: 'Review material submittal for specification compliance. Document approval status and any conditions.' },
                { id: 'test-report-review', name: 'Test Report Review', prompt: 'Review test reports for compliance with specifications. Verify test methods, results, and acceptance criteria.' }
            ]
        }
    },

    init: function(containerId, toolkit) {
        this.container = document.getElementById(containerId);
        this.toolkit = toolkit;
        if (!this.container) return;

        this.render();
    },

    render: function() {
        const toolkitData = this.definitions[this.toolkit];
        if (!toolkitData) return;

        this.container.innerHTML = `
            <h2>Template Selection</h2>
            <div class="panel-content">
                <div class="template-group">
                    <label>Template</label>
                    <select class="template-select" id="template-select" onchange="Templates.selectTemplate(this.value)">
                        <option value="">Select a template...</option>
                        ${toolkitData.templates.map(t => `
                            <option value="${t.id}">${t.name}</option>
                        `).join('')}
                    </select>
                </div>
                <div class="template-group">
                    <label>Mode</label>
                    <div class="mode-toggle">
                        <button class="btn ${this.currentMode === 'production' ? 'active' : ''}"
                                onclick="Templates.setMode('production')">Production</button>
                        <button class="btn ${this.currentMode === 'review' ? 'active' : ''}"
                                onclick="Templates.setMode('review')">Review</button>
                    </div>
                </div>
                <div class="template-info" id="template-info">
                    <p class="placeholder">Select a template to see details</p>
                </div>
            </div>
        `;
    },

    selectTemplate: function(templateId) {
        const toolkitData = this.definitions[this.toolkit];
        if (!toolkitData) return;

        this.currentTemplate = toolkitData.templates.find(t => t.id === templateId);
        this.updateTemplateInfo();
    },

    setMode: function(mode) {
        this.currentMode = mode;
        this.render();
        if (this.currentTemplate) {
            document.getElementById('template-select').value = this.currentTemplate.id;
            this.updateTemplateInfo();
        }
    },

    updateTemplateInfo: function() {
        const infoEl = document.getElementById('template-info');
        if (!infoEl) return;

        if (this.currentTemplate) {
            const modeDesc = this.currentMode === 'production'
                ? 'Generate new document'
                : 'Analyze uploaded document';
            infoEl.innerHTML = `
                <div class="template-details">
                    <p class="template-name"><strong>${this.currentTemplate.name}</strong></p>
                    <p class="template-mode">Mode: ${modeDesc}</p>
                </div>
            `;
        } else {
            infoEl.innerHTML = '<p class="placeholder">Select a template to see details</p>';
        }
    },

    getSystemPrompt: function() {
        if (!this.currentTemplate) return '';

        const modeContext = this.currentMode === 'production'
            ? 'You are generating a new document. Create professional, comprehensive output.'
            : 'You are reviewing/analyzing the provided documents. Focus on accuracy and completeness.';

        return `${modeContext}\n\nTask: ${this.currentTemplate.prompt}`;
    },

    getCurrentTemplate: function() {
        return this.currentTemplate;
    },

    getMode: function() {
        return this.currentMode;
    }
};

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('template-selection')) {
        // Determine toolkit from URL
        const path = window.location.pathname;
        let toolkit = 'pm';
        if (path.includes('traffic.html')) toolkit = 'traffic';
        else if (path.includes('developer.html')) toolkit = 'developer';
        else if (path.includes('qcm.html')) toolkit = 'qcm';

        Templates.init('template-selection', toolkit);
    }
});
