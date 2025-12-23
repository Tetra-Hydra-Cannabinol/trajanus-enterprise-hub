// ============================================
// TRAJANUS ENTERPRISE HUB - PLATFORM NAVIGATION
// Version: 4.0.0
// Date: December 2025
// ============================================

// ============================================
// PLATFORM STATE MANAGEMENT
// ============================================

const PlatformState = {
    currentPlatform: null,
    currentWorkspace: null,
    history: [],

    // Platform definitions
    platforms: {
        'construction': {
            name: 'Construction Management',
            icon: 'fa-hard-hat',
            workspaces: ['qcm', 'pm', 'dashboard']
        },
        'pe-services': {
            name: 'P.E. Services',
            icon: 'fa-stamp',
            workspaces: ['legal-opinion', 'pe-review']
        },
        'route-optimization': {
            name: 'Route Optimization',
            icon: 'fa-route',
            workspaces: ['route-planner']
        },
        'traffic-studies': {
            name: 'Traffic Studies',
            icon: 'fa-traffic-light',
            workspaces: ['traffic-analysis', 'signal-timing']
        }
    },

    // Workspace definitions
    workspaces: {
        'qcm': {
            name: 'QCM Workspace',
            platform: 'construction',
            icon: 'fa-clipboard-check'
        },
        'pm': {
            name: 'PM Toolkit',
            platform: 'construction',
            icon: 'fa-tasks'
        },
        'dashboard': {
            name: 'Project Dashboard',
            platform: 'construction',
            icon: 'fa-chart-line'
        },
        'legal-opinion': {
            name: 'Legal Opinion',
            platform: 'pe-services',
            icon: 'fa-gavel'
        },
        'pe-review': {
            name: 'PE Review & Stamp',
            platform: 'pe-services',
            icon: 'fa-stamp'
        },
        'route-planner': {
            name: 'Route Planner',
            platform: 'route-optimization',
            icon: 'fa-map-marked-alt'
        },
        'traffic-analysis': {
            name: 'Traffic Analysis',
            platform: 'traffic-studies',
            icon: 'fa-chart-bar'
        },
        'signal-timing': {
            name: 'Signal Timing',
            platform: 'traffic-studies',
            icon: 'fa-clock'
        }
    }
};

// ============================================
// NAVIGATION FUNCTIONS
// ============================================

/**
 * Navigate to a platform from the selection page
 * @param {string} platformId - The platform identifier
 */
function enterPlatform(platformId) {
    console.log(`[Nav] Entering platform: ${platformId}`);

    const platform = PlatformState.platforms[platformId];
    if (!platform) {
        console.error(`[Nav] Unknown platform: ${platformId}`);
        return;
    }

    // Update state
    PlatformState.history.push({ type: 'platform-select' });
    PlatformState.currentPlatform = platformId;
    PlatformState.currentWorkspace = null;

    // Save to localStorage
    saveNavigationState();

    // Log navigation
    console.log(`[Nav] -> Platform: ${platform.name}`);
    console.log(`[Nav] -> Workspaces: ${platform.workspaces.join(', ')}`);

    // In production: navigate to platform page
    // window.location.href = `${platformId}-platform.html`;

    return {
        success: true,
        platform: platformId,
        name: platform.name,
        workspaces: platform.workspaces
    };
}

/**
 * Navigate back in history
 */
function goBack() {
    console.log('[Nav] Going back');

    const previous = PlatformState.history.pop();

    if (!previous) {
        console.log('[Nav] -> No history, going to platform selection');
        PlatformState.currentPlatform = null;
        PlatformState.currentWorkspace = null;
        saveNavigationState();
        // window.location.href = 'platform-selection.html';
        return { success: true, destination: 'platform-selection' };
    }

    if (previous.type === 'platform-select') {
        console.log('[Nav] -> Returning to platform selection');
        PlatformState.currentPlatform = null;
        PlatformState.currentWorkspace = null;
        saveNavigationState();
        // window.location.href = 'platform-selection.html';
        return { success: true, destination: 'platform-selection' };
    }

    if (previous.type === 'workspace') {
        console.log(`[Nav] -> Returning to platform: ${previous.platform}`);
        PlatformState.currentWorkspace = null;
        saveNavigationState();
        // window.location.href = `${previous.platform}-platform.html`;
        return { success: true, destination: previous.platform };
    }

    return { success: false, error: 'Unknown history state' };
}

/**
 * Open a workspace within the current platform
 * @param {string} workspaceId - The workspace identifier
 */
function openWorkspace(workspaceId) {
    console.log(`[Nav] Opening workspace: ${workspaceId}`);

    const workspace = PlatformState.workspaces[workspaceId];
    if (!workspace) {
        console.error(`[Nav] Unknown workspace: ${workspaceId}`);
        return { success: false, error: 'Unknown workspace' };
    }

    // Verify workspace belongs to current platform
    if (PlatformState.currentPlatform && workspace.platform !== PlatformState.currentPlatform) {
        console.warn(`[Nav] Workspace ${workspaceId} not in current platform ${PlatformState.currentPlatform}`);
    }

    // Update state
    PlatformState.history.push({
        type: 'workspace',
        platform: PlatformState.currentPlatform
    });
    PlatformState.currentWorkspace = workspaceId;

    // Save to localStorage
    saveNavigationState();

    // Log navigation
    console.log(`[Nav] -> Workspace: ${workspace.name}`);
    console.log(`[Nav] -> Platform: ${workspace.platform}`);

    return {
        success: true,
        workspace: workspaceId,
        name: workspace.name,
        platform: workspace.platform
    };
}

// ============================================
// WORKSPACE TAB MANAGEMENT
// ============================================

const TabState = {
    activeTab: 'main',
    tabCounter: 0,
    toolTabCounter: 0,
    maxToolTabs: 4,
    permanentTabs: ['main', 'devtools', 'codes', 'external']
};

/**
 * Get the currently active terminal element
 * @returns {HTMLElement|null}
 */
function getActiveTerminal() {
    return document.getElementById(`terminal-${TabState.activeTab}`);
}

/**
 * Switch to a different tab
 * @param {string} tabId - The tab identifier
 */
function switchTab(tabId) {
    console.log(`[Tabs] Switching to: ${tabId}`);

    // Update tab buttons
    document.querySelectorAll('.terminal-tab').forEach(tab => {
        tab.classList.remove('active');
        if (tab.dataset.tab === tabId) {
            tab.classList.add('active');
        }
    });

    // Update terminal bodies
    document.querySelectorAll('.terminal-body').forEach(body => {
        body.classList.remove('active');
        body.style.display = 'none';
    });

    const targetTerminal = document.getElementById(`terminal-${tabId}`);
    if (targetTerminal) {
        targetTerminal.classList.add('active');
        targetTerminal.style.display = 'block';
    }

    TabState.activeTab = tabId;
    saveTabState();

    return { success: true, activeTab: tabId };
}

/**
 * Add a new terminal tab
 * @param {string} name - Optional tab name
 * @returns {string|null} The new tab ID or null if at limit
 */
function addTab(name = null) {
    // Count existing tool tabs
    const existingToolTabs = Array.from(document.querySelectorAll('.terminal-tab'))
        .filter(tab => !TabState.permanentTabs.includes(tab.dataset.tab));

    // Check if at limit
    if (existingToolTabs.length >= TabState.maxToolTabs) {
        console.warn(`[Tabs] Maximum ${TabState.maxToolTabs} tool tabs allowed`);
        return null;
    }

    TabState.tabCounter++;
    const tabId = `tab-${TabState.tabCounter}`;
    const tabName = name || `Terminal ${TabState.tabCounter}`;

    console.log(`[Tabs] Adding tab: ${tabId} (${tabName})`);

    // Create tab button
    const tabBtn = document.createElement('button');
    tabBtn.className = 'terminal-tab';
    tabBtn.dataset.tab = tabId;
    tabBtn.onclick = () => switchTab(tabId);
    tabBtn.innerHTML = `${tabName} <span class="close-tab" onclick="closeTab(event, '${tabId}')">×</span>`;

    const tabContainer = document.getElementById('terminalTabs');
    if (tabContainer) {
        tabContainer.appendChild(tabBtn);
    }

    // Create terminal body
    const termBody = document.createElement('div');
    termBody.className = 'terminal-body';
    termBody.id = `terminal-${tabId}`;
    termBody.dataset.tab = tabId;
    termBody.innerHTML = `<div class="info">[Ready] New terminal opened</div>`;
    termBody.style.display = 'none';

    const bodyContainer = document.getElementById('terminalBodies');
    if (bodyContainer) {
        bodyContainer.appendChild(termBody);
    }

    // Switch to new tab
    switchTab(tabId);

    return tabId;
}

/**
 * Close a terminal tab
 * @param {Event} event - Click event
 * @param {string} tabId - The tab identifier
 */
function closeTab(event, tabId) {
    if (event) {
        event.stopPropagation();
    }

    // Never allow closing permanent tabs
    if (TabState.permanentTabs.includes(tabId)) {
        console.warn(`[Tabs] Cannot close permanent tab: ${tabId}`);
        return false;
    }

    console.log(`[Tabs] Closing tab: ${tabId}`);

    // Remove tab button
    const tabBtn = document.querySelector(`.terminal-tab[data-tab="${tabId}"]`);
    if (tabBtn) {
        tabBtn.remove();
    }

    // Remove terminal body
    const termBody = document.getElementById(`terminal-${tabId}`);
    if (termBody) {
        termBody.remove();
    }

    // If closing active tab, switch to first remaining tab
    if (TabState.activeTab === tabId) {
        const firstTab = document.querySelector('.terminal-tab');
        if (firstTab) {
            switchTab(firstTab.dataset.tab);
        }
    }

    saveTabState();

    return true;
}

/**
 * Create a workspace tab with custom content
 * @param {string} name - Tab name
 * @param {string} contentHTML - HTML content for the workspace
 * @returns {string|null} The new tab ID or null if at limit
 */
function createWorkspaceTab(name, contentHTML) {
    // Count existing tool tabs
    const existingToolTabs = Array.from(document.querySelectorAll('.terminal-tab'))
        .filter(tab => !TabState.permanentTabs.includes(tab.dataset.tab));

    if (existingToolTabs.length >= TabState.maxToolTabs) {
        console.warn(`[Tabs] Maximum ${TabState.maxToolTabs} tool tabs allowed`);
        alert(`Maximum ${TabState.maxToolTabs} tool tabs allowed. Please close a tab before opening a new one.`);
        return null;
    }

    TabState.toolTabCounter++;
    const tabId = `tool-${TabState.toolTabCounter}`;

    console.log(`[Tabs] Creating workspace tab: ${tabId} (${name})`);

    // Create tab button
    const tabBtn = document.createElement('button');
    tabBtn.className = 'terminal-tab';
    tabBtn.dataset.tab = tabId;
    tabBtn.onclick = () => switchTab(tabId);
    tabBtn.innerHTML = `${name} <span class="close-tab" onclick="closeTab(event, '${tabId}')">×</span>`;

    const tabContainer = document.getElementById('terminalTabs');
    if (tabContainer) {
        tabContainer.appendChild(tabBtn);
    }

    // Create terminal body with custom content
    const termBody = document.createElement('div');
    termBody.className = 'terminal-body';
    termBody.id = `terminal-${tabId}`;
    termBody.dataset.tab = tabId;
    termBody.innerHTML = contentHTML;
    termBody.style.display = 'none';

    const bodyContainer = document.getElementById('terminalBodies');
    if (bodyContainer) {
        bodyContainer.appendChild(termBody);
    }

    // Switch to new tab
    switchTab(tabId);

    return tabId;
}

// ============================================
// LOCALSTORAGE PERSISTENCE
// ============================================

const STORAGE_KEYS = {
    navState: 'trajanus_nav_state',
    tabState: 'trajanus_tab_state',
    platformOrder: 'trajanus_platform_order'
};

/**
 * Save navigation state to localStorage
 */
function saveNavigationState() {
    const state = {
        currentPlatform: PlatformState.currentPlatform,
        currentWorkspace: PlatformState.currentWorkspace,
        history: PlatformState.history,
        timestamp: Date.now()
    };

    try {
        localStorage.setItem(STORAGE_KEYS.navState, JSON.stringify(state));
        console.log('[Storage] Navigation state saved');
    } catch (e) {
        console.error('[Storage] Failed to save navigation state:', e);
    }
}

/**
 * Load navigation state from localStorage
 */
function loadNavigationState() {
    try {
        const stored = localStorage.getItem(STORAGE_KEYS.navState);
        if (stored) {
            const state = JSON.parse(stored);
            PlatformState.currentPlatform = state.currentPlatform;
            PlatformState.currentWorkspace = state.currentWorkspace;
            PlatformState.history = state.history || [];
            console.log('[Storage] Navigation state loaded');
            return state;
        }
    } catch (e) {
        console.error('[Storage] Failed to load navigation state:', e);
    }
    return null;
}

/**
 * Save tab state to localStorage
 */
function saveTabState() {
    const state = {
        activeTab: TabState.activeTab,
        tabCounter: TabState.tabCounter,
        toolTabCounter: TabState.toolTabCounter,
        timestamp: Date.now()
    };

    try {
        localStorage.setItem(STORAGE_KEYS.tabState, JSON.stringify(state));
    } catch (e) {
        console.error('[Storage] Failed to save tab state:', e);
    }
}

/**
 * Load tab state from localStorage
 */
function loadTabState() {
    try {
        const stored = localStorage.getItem(STORAGE_KEYS.tabState);
        if (stored) {
            const state = JSON.parse(stored);
            TabState.activeTab = state.activeTab || 'main';
            TabState.tabCounter = state.tabCounter || 0;
            TabState.toolTabCounter = state.toolTabCounter || 0;
            console.log('[Storage] Tab state loaded');
            return state;
        }
    } catch (e) {
        console.error('[Storage] Failed to load tab state:', e);
    }
    return null;
}

/**
 * Clear all stored state
 */
function clearStoredState() {
    try {
        localStorage.removeItem(STORAGE_KEYS.navState);
        localStorage.removeItem(STORAGE_KEYS.tabState);
        localStorage.removeItem(STORAGE_KEYS.platformOrder);
        console.log('[Storage] All state cleared');
    } catch (e) {
        console.error('[Storage] Failed to clear state:', e);
    }
}

// ============================================
// KEYBOARD SHORTCUTS
// ============================================

/**
 * Initialize keyboard shortcuts
 */
function initKeyboardShortcuts() {
    document.addEventListener('keydown', (event) => {
        // Alt + Left Arrow: Go back
        if (event.altKey && event.key === 'ArrowLeft') {
            event.preventDefault();
            goBack();
            return;
        }

        // Ctrl/Cmd + number: Switch to tab
        if ((event.ctrlKey || event.metaKey) && event.key >= '1' && event.key <= '9') {
            event.preventDefault();
            const tabs = document.querySelectorAll('.terminal-tab');
            const index = parseInt(event.key) - 1;
            if (tabs[index]) {
                switchTab(tabs[index].dataset.tab);
            }
            return;
        }

        // Ctrl/Cmd + T: New tab
        if ((event.ctrlKey || event.metaKey) && event.key === 't') {
            event.preventDefault();
            addTab();
            return;
        }

        // Ctrl/Cmd + W: Close current tab
        if ((event.ctrlKey || event.metaKey) && event.key === 'w') {
            event.preventDefault();
            closeTab(null, TabState.activeTab);
            return;
        }
    });

    console.log('[Keyboard] Shortcuts initialized');
}

// ============================================
// BREADCRUMB GENERATION
// ============================================

/**
 * Generate breadcrumb HTML based on current state
 * @returns {string} Breadcrumb HTML
 */
function generateBreadcrumb() {
    const items = ['<span class="breadcrumb-item" onclick="goToPlatformSelection()">Enterprise Hub</span>'];

    if (PlatformState.currentPlatform) {
        const platform = PlatformState.platforms[PlatformState.currentPlatform];
        if (PlatformState.currentWorkspace) {
            items.push(`<span class="breadcrumb-separator"><i class="fas fa-chevron-right"></i></span>`);
            items.push(`<span class="breadcrumb-item" onclick="goBack()">${platform.name}</span>`);

            const workspace = PlatformState.workspaces[PlatformState.currentWorkspace];
            items.push(`<span class="breadcrumb-separator"><i class="fas fa-chevron-right"></i></span>`);
            items.push(`<span class="breadcrumb-item active">${workspace.name}</span>`);
        } else {
            items.push(`<span class="breadcrumb-separator"><i class="fas fa-chevron-right"></i></span>`);
            items.push(`<span class="breadcrumb-item active">${platform.name}</span>`);
        }
    }

    return items.join('');
}

/**
 * Navigate directly to platform selection
 */
function goToPlatformSelection() {
    console.log('[Nav] Going to platform selection');
    PlatformState.currentPlatform = null;
    PlatformState.currentWorkspace = null;
    PlatformState.history = [];
    saveNavigationState();
    // window.location.href = 'platform-selection.html';
}

// ============================================
// INITIALIZATION
// ============================================

/**
 * Initialize the navigation system
 */
function initNavigation() {
    console.log('[Nav] Initializing navigation system...');

    // Load stored state
    loadNavigationState();
    loadTabState();

    // Initialize keyboard shortcuts
    initKeyboardShortcuts();

    console.log('[Nav] Navigation system ready');
    console.log('[Nav] Current platform:', PlatformState.currentPlatform || 'none');
    console.log('[Nav] Current workspace:', PlatformState.currentWorkspace || 'none');
}

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initNavigation);
} else {
    initNavigation();
}

// ============================================
// EXPORTS (for module usage)
// ============================================

// Make functions available globally
window.PlatformNav = {
    // State
    PlatformState,
    TabState,

    // Navigation
    enterPlatform,
    goBack,
    openWorkspace,
    goToPlatformSelection,

    // Tabs
    switchTab,
    addTab,
    closeTab,
    createWorkspaceTab,
    getActiveTerminal,

    // Storage
    saveNavigationState,
    loadNavigationState,
    saveTabState,
    loadTabState,
    clearStoredState,

    // Utilities
    generateBreadcrumb,
    initKeyboardShortcuts,
    initNavigation
};

console.log('[Nav] Platform Navigation loaded - v4.0.0');
