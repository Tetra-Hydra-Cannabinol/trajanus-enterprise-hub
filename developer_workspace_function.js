// DEVELOPER PROJECT WORKSPACE - Full Implementation
function openDeveloperProject() {
    const workspaceHTML = `
        <div style="height: 100%; display: flex; flex-direction: column; background: var(--brown-dark);">
            <!-- HEADER -->
            <div style="padding: 20px; background: rgba(0,0,0,0.3); border-bottom: 1px solid rgba(255,255,255,0.1);">
                <div class="success">[Ready] Developer Project Workspace</div>
                <div class="info">[Info] Development tools, agents, scripts, and automation</div>
            </div>
            
            <!-- DEV TOOLS DASHBOARD - Top Section -->
            <div style="flex: 0 0 auto; padding: 20px; overflow-y: auto; max-height: 50%;">
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 15px;">
                    
                    <!-- FILE MANAGEMENT GROUP -->
                    <div style="background: rgba(168, 90, 27, 0.1); border-left: 3px solid var(--orange-mid); padding: 15px; border-radius: 6px;">
                        <div style="color: var(--orange-light); font-weight: bold; margin-bottom: 10px; font-size: 0.9rem;">FILE MANAGEMENT</div>
                        <button class="session-btn" onclick="openFileBrowser('living-docs')" style="margin: 4px; width: calc(50% - 8px);">Living Documents</button>
                        <button class="session-btn" onclick="openFileBrowser('sessions')" style="margin: 4px; width: calc(50% - 8px);">Session Library</button>
                        <button class="session-btn" onclick="openFileBrowser('templates')" style="margin: 4px; width: calc(50% - 8px);">Templates</button>
                        <button class="session-btn" onclick="openFileBrowser('protocols')" style="margin: 4px; width: calc(50% - 8px);">Core Protocols</button>
                        <button class="session-btn" onclick="openFileBrowser('scripts')" style="margin: 4px; width: calc(50% - 8px);">Scripts Directory</button>
                        <button class="session-btn" onclick="openFileBrowser('documentation')" style="margin: 4px; width: calc(50% - 8px);">Documentation</button>
                    </div>
                    
                    <!-- KNOWMADS AGENTS GROUP -->
                    <div style="background: rgba(168, 90, 27, 0.1); border-left: 3px solid var(--orange-mid); padding: 15px; border-radius: 6px;">
                        <div style="color: var(--orange-light); font-weight: bold; margin-bottom: 10px; font-size: 0.9rem;">KNOWMADS AGENTS</div>
                        <button class="session-btn" onclick="log('Knowmad-1: HTML Surgeon - Ready', 'success', 'devtools')" style="margin: 4px; width: calc(50% - 8px);">Knowmad-1: HTML</button>
                        <button class="session-btn" onclick="log('Knowmad-2: CSS Architect - Ready', 'success', 'devtools')" style="margin: 4px; width: calc(50% - 8px);">Knowmad-2: CSS</button>
                        <button class="session-btn" onclick="log('Knowmad-3: JS Builder - Ready', 'success', 'devtools')" style="margin: 4px; width: calc(50% - 8px);">Knowmad-3: JavaScript</button>
                        <button class="session-btn" onclick="log('Knowmad-4: File Scout - Ready', 'success', 'devtools')" style="margin: 4px; width: calc(50% - 8px);">Knowmad-4: File Scout</button>
                        <button class="session-btn" onclick="log('Knowmad-5: Integration - Ready', 'success', 'devtools')" style="margin: 4px; width: calc(50% - 8px);">Knowmad-5: Validator</button>
                        <button class="session-btn" onclick="log('Knowmad-6: Documentation - Ready', 'success', 'devtools')" style="margin: 4px; width: calc(50% - 8px);">Knowmad-6: Docs</button>
                    </div>
                    
                    <!-- AUTOMATION SCRIPTS GROUP -->
                    <div style="background: rgba(168, 90, 27, 0.1); border-left: 3px solid var(--orange-mid); padding: 15px; border-radius: 6px;">
                        <div style="color: var(--orange-light); font-weight: bold; margin-bottom: 10px; font-size: 0.9rem;">AUTOMATION SCRIPTS</div>
                        <button class="session-btn" onclick="log('Running CONVERT_NEW_FILES_ONLY.ps1...', 'warning', 'devtools')" style="margin: 4px; width: calc(50% - 8px);">Convert Files</button>
                        <button class="session-btn" onclick="log('Running consolidate_folders.py...', 'warning', 'devtools')" style="margin: 4px; width: calc(50% - 8px);">Consolidate Folders</button>
                        <button class="session-btn" onclick="log('Running file_ingestion.py...', 'warning', 'devtools')" style="margin: 4px; width: calc(50% - 8px);">KB Ingestion</button>
                        <button class="session-btn" onclick="log('Running live_crawler.py...', 'warning', 'devtools')" style="margin: 4px; width: calc(50% - 8px);">Live Crawler</button>
                        <button class="session-btn" onclick="log('Running Drive Cleanup...', 'warning', 'devtools')" style="margin: 4px; width: calc(50% - 8px);">Drive Cleanup</button>
                        <button class="session-btn" onclick="log('Script management...', 'info', 'devtools')" style="margin: 4px; width: calc(50% - 8px);">Manage Scripts</button>
                    </div>
                    
                    <!-- SESSION MANAGEMENT GROUP -->
                    <div style="background: rgba(168, 90, 27, 0.1); border-left: 3px solid var(--orange-mid); padding: 15px; border-radius: 6px;">
                        <div style="color: var(--orange-light); font-weight: bold; margin-bottom: 10px; font-size: 0.9rem;">SESSION TOOLS</div>
                        <button class="session-btn" onclick="log('Opening handoff generator...', 'info', 'devtools')" style="margin: 4px; width: calc(50% - 8px);">Mission Brief</button>
                        <button class="session-btn" onclick="log('Loading protocols...', 'info', 'devtools')" style="margin: 4px; width: calc(50% - 8px);">Sync Protocols</button>
                        <button class="session-btn" onclick="log('Starting EOS routine...', 'warning', 'devtools')" style="margin: 4px; width: calc(50% - 8px);">EOS Protocol</button>
                        <button class="session-btn" onclick="log('Updating living docs...', 'info', 'devtools')" style="margin: 4px; width: calc(50% - 8px);">Update Living Docs</button>
                        <button class="session-btn" onclick="log('Generating handoff...', 'info', 'devtools')" style="margin: 4px; width: calc(50% - 8px);">Handoff Generator</button>
                        <button class="session-btn" onclick="log('Context update...', 'info', 'devtools')" style="margin: 4px; width: calc(50% - 8px);">Context Update</button>
                    </div>
                    
                </div>
            </div>
            
            <!-- FULL-WIDTH TERMINAL - Bottom Section -->
            <div style="flex: 1; display: flex; flex-direction: column; border-top: 2px solid var(--orange-mid); min-height: 300px;">
                <div style="background: var(--brown-mid); padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.1);">
                    <div style="color: var(--orange-light); font-weight: 600; font-size: 0.9rem;">INTEGRATED TERMINAL</div>
                </div>
                <div style="flex: 1; padding: 15px; overflow-y: auto; background: rgba(0,0,0,0.2); font-family: 'Courier New', monospace; font-size: 0.9rem;">
                    <div class="success">[Ready] Terminal initialized for Developer Project</div>
                    <div class="info">[Info] Use terminal tabs above for different interfaces</div>
                    <div class="info">[Info] Current tabs: Developer Tools | Codes & Standards | External | Claude Web | Claude Code</div>
                    <div style="margin-top: 15px; color: var(--gray-light);">
                        Terminal workspace ready for commands and operations.<br>
                        Switch between tabs for different tool interfaces.
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Create the workspace tab
    const tabId = createWorkspaceTab('Developer Project', workspaceHTML);
    
    if (tabId) {
        log('Developer Project workspace opened successfully', 'success', 'devtools');
        log('All development tools and agents ready', 'info', tabId);
    }
}
