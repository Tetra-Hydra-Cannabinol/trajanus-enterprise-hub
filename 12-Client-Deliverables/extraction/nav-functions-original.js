// ============================================
// NAVIGATION FUNCTIONS
// Extracted from index.html lines 3220-3520
// ============================================

// ============================================
// TERMINAL TABS
// ============================================
let activeTab = 'devtools';
let tabCounter = 1;

function getActiveTerminal() {
    return document.getElementById(`terminal-${activeTab}`);
}

function switchTab(tabId) {
    // Update tab buttons
    document.querySelectorAll('.terminal-tab').forEach(tab => {
        tab.classList.remove('active');
        if (tab.dataset.tab === tabId) tab.classList.add('active');
    });

    // Update terminal bodies
    document.querySelectorAll('.terminal-body').forEach(body => {
        body.classList.remove('active');
    });
    document.getElementById(`terminal-${tabId}`).classList.add('active');

    activeTab = tabId;
}

function addTab(name = null) {
    tabCounter++;
    const tabId = `tab-${tabCounter}`;
    const tabName = name || `Terminal ${tabCounter}`;

    // Create tab button
    const tabBtn = document.createElement('button');
    tabBtn.className = 'terminal-tab';
    tabBtn.dataset.tab = tabId;
    tabBtn.onclick = () => switchTab(tabId);
    tabBtn.innerHTML = `${tabName} <span class="close-tab" onclick="closeTab(event, '${tabId}')">×</span>`;
    document.getElementById('terminalTabs').appendChild(tabBtn);

    // Create terminal body
    const termBody = document.createElement('div');
    termBody.className = 'terminal-body';
    termBody.id = `terminal-${tabId}`;
    termBody.dataset.tab = tabId;
    termBody.innerHTML = `<div class="info">[Ready] New terminal opened</div>`;
    document.getElementById('terminalBodies').appendChild(termBody);

    // Switch to new tab
    switchTab(tabId);

    return tabId;
}

function closeTab(event, tabId) {
    event.stopPropagation();

    // Never allow closing permanent tabs or main tab
    const permanentTabs = ['devtools', 'codes', 'external', 'main'];
    if (permanentTabs.includes(tabId)) {
        log('Permanent tabs cannot be closed', 'warning', tabId);
        return;
    }

    const tabs = document.querySelectorAll('.terminal-tab');
    if (tabs.length <= 6) return; // Don't close if only main + 5 permanent tabs remain

    // Remove tab button and body
    document.querySelector(`.terminal-tab[data-tab="${tabId}"]`).remove();
    document.getElementById(`terminal-${tabId}`).remove();

    // If closing active tab, switch to first remaining tab
    if (activeTab === tabId) {
        const firstTab = document.querySelector('.terminal-tab');
        if (firstTab) switchTab(firstTab.dataset.tab);
    }
}

// Track open tool tabs (limit to 4)
let toolTabCounter = 0;
const MAX_TOOL_TABS = 4;

// Create a workspace tab with custom content
function createWorkspaceTab(name, contentHTML) {
    // Count existing tool tabs (exclude permanent and main tabs)
    const permanentTabs = ['devtools', 'codes', 'external', 'main', 'review-history'];
    const existingToolTabs = Array.from(document.querySelectorAll('.terminal-tab'))
        .filter(tab => !permanentTabs.includes(tab.dataset.tab));

    // Check if at limit
    if (existingToolTabs.length >= MAX_TOOL_TABS) {
        alert(`Maximum ${MAX_TOOL_TABS} tool tabs allowed. Please close a tab before opening a new one.`);
        return null;
    }

    toolTabCounter++;
    const tabId = `tool-${toolTabCounter}`;

    // Create tab button
    const tabBtn = document.createElement('button');
    tabBtn.className = 'terminal-tab';
    tabBtn.dataset.tab = tabId;
    tabBtn.onclick = () => switchTab(tabId);
    tabBtn.innerHTML = `${name} <span class="close-tab" onclick="closeTab(event, '${tabId}')">×</span>`;
    document.getElementById('terminalTabs').appendChild(tabBtn);

    // Create terminal body
    const termBody = document.createElement('div');
    termBody.className = 'terminal-body';
    termBody.id = `terminal-${tabId}`;
    termBody.dataset.tab = tabId;
    termBody.innerHTML = contentHTML;
    document.getElementById('terminalBodies').appendChild(termBody);

    // Switch to new tab
    switchTab(tabId);

    log(`${name} workspace opened`, 'success', 'main');

    return tabId;
}

// ============================================
// UTILITY FUNCTIONS
// ============================================
function openExternal(url) {
    if (window.electronAPI) {
        window.electronAPI.openExternal(url);
    } else {
        window.open(url, '_blank');
    }
}

// ============================================
// PROJECT NAVIGATION
// ============================================
let currentProject = null; // Will be set to first project in list

// Function to switch to a project (called by both click and mouseup)
function switchToProject(btn) {
    const project = btn.dataset.project;

    log(``, 'info');
    log(`CLICKED PROJECT: ${project}`, 'info');

    // Remove active from all
    document.querySelectorAll('.project-btn[data-project]').forEach(b => b.classList.remove('active'));
    // Add to clicked
    btn.classList.add('active');

    const projectName = btn.querySelector('span').textContent;
    currentProject = project;

    // Update header
    document.getElementById('projectTitle').textContent = projectName;

    // Show/hide project-specific tools
    document.querySelectorAll('.project-tools').forEach(section => {
        section.style.display = 'none';
    });
    const activeTools = document.querySelector(`.project-tools[data-project="${project}"]`);
    if (activeTools) {
        activeTools.style.display = 'block';
    }

    log(`Switched to: ${projectName}`, 'info');
    loadProjectFiles(project);
}

// ============================================
// PROJECT ORDER PERSISTENCE
// ============================================

// Restore saved project order from localStorage
function restoreProjectOrder() {
    const devOrder = localStorage.getItem('projectOrder_dev');
    const deployedOrder = localStorage.getItem('projectOrder_deployed');

    if (devOrder) {
        const order = JSON.parse(devOrder);
        const container = document.querySelector('.project-section:first-of-type');
        const h3 = container.querySelector('h3');

        // Reorder buttons based on saved order
        order.forEach(projectId => {
            const btn = container.querySelector(`[data-project="${projectId}"]`);
            if (btn) container.appendChild(btn);
        });

        // Put h3 back at top
        container.insertBefore(h3, container.firstChild);
    }

    if (deployedOrder) {
        const order = JSON.parse(deployedOrder);
        const container = document.querySelectorAll('.project-section')[1];
        const h3 = container.querySelector('h3');

        // Reorder buttons
        order.forEach(projectId => {
            const btn = container.querySelector(`[data-project="${projectId}"]`);
            if (btn) container.appendChild(btn);
        });

        // Put h3 back at top
        container.insertBefore(h3, container.firstChild);
    }
}

// Save current project order to localStorage
function saveProjectOrder(container, key) {
    const buttons = container.querySelectorAll('.project-btn[data-project]');
    const order = Array.from(buttons).map(btn => btn.dataset.project);
    localStorage.setItem(key, JSON.stringify(order));
}

// ============================================
// DRAG AND DROP VARIABLES
// ============================================
let draggedElement = null;
let dragStartX = 0;
let dragStartY = 0;
let isDragging = false;
let placeholder = null;

// Note: Drag and drop event handlers are attached in DOMContentLoaded
// See index.html lines 3478-3560 for full implementation
