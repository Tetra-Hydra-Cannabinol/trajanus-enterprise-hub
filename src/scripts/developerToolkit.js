// Developer Toolkit v2 - Professional Control Panel

const DevToolkit = {
    // ==================== PATHS ====================
    paths: {
        userGuides: 'G:\\My Drive\\00 - Trajanus USA\\00-Command-Center\\User-Guides',
        livingDocs: 'G:\\My Drive\\00 - Trajanus USA\\03-Living-Documents',
        coreProtocols: 'G:\\My Drive\\00 - Trajanus USA\\01-Core-Protocols',
        documentation: 'G:\\My Drive\\00 - Trajanus USA\\00-Command-Center\\04-Documentation',
        scripts: 'G:\\My Drive\\00 - Trajanus USA\\00-Command-Center\\05-Scripts',
        sessionFiles: 'G:\\My Drive\\00 - Trajanus USA\\07-Session-Journal',
        credentials: 'G:\\My Drive\\00 - Trajanus USA\\00-Command-Center\\001 Credentials',
        commandCenter: 'G:\\My Drive\\00 - Trajanus USA\\00-Command-Center',
        morningDocs: 'G:\\My Drive\\00 - Trajanus USA\\01-Morning-Sessions',
        project: 'C:\\Dev\\trajanus-command-center'
    },

    conversationHistory: [],
    apiKey: null,
    currentTab: 'developer-tools',

    // ==================== INITIALIZATION ====================
    init: function() {
        this.log('TRAJANUS COMMAND CENTER v2.0.0 initialized', 'success');
        this.log('Developer Toolkit loaded', 'info');

        // Check for active session
        const session = localStorage.getItem('current_session');
        if (session) {
            const sessionData = JSON.parse(session);
            this.log(`Active session detected: ${sessionData.id}`, 'info');
        }

        // Load API key
        this.loadApiKey();
    },

    // ==================== CONSOLE LOGGING ====================
    log: function(message, type = 'info') {
        const console = document.getElementById('console-output');
        if (!console) return;

        const now = new Date();
        const timestamp = now.toTimeString().split(' ')[0]; // HH:MM:SS

        const line = document.createElement('div');
        line.className = `console-line ${type}`;
        line.innerHTML = `<span class="timestamp">[${timestamp}]</span> ${message}`;

        console.appendChild(line);
        console.scrollTop = console.scrollHeight;
    },

    // ==================== TAB SWITCHING ====================
    switchTab: function(tabName) {
        // Update tab states
        document.querySelectorAll('.tab').forEach(tab => {
            tab.classList.remove('active');
        });
        event.target.classList.add('active');

        this.currentTab = tabName;
        this.log(`Switched to tab: ${tabName}`, 'info');

        // For now, all tabs show the same content
        // Future: implement different content per tab
    },

    // ==================== NAVIGATION ====================
    navigate: function(toolkit) {
        this.log(`Navigating to: ${toolkit}`, 'info');

        const routes = {
            'command-center': '../index.html',
            'website-builder': '../index.html',
            'pm': 'pm.html',
            'qcm': 'qcm.html',
            'traffic': 'traffic.html'
        };

        if (routes[toolkit]) {
            window.location.href = routes[toolkit];
        }
    },

    toggleDropdown: function(button) {
        const menu = button.nextElementSibling;
        menu.classList.toggle('show');
    },

    // ==================== FOLDER OPERATIONS ====================
    openFolder: async function(folderKey) {
        const path = this.paths[folderKey];
        if (!path) {
            this.log(`Unknown folder: ${folderKey}`, 'error');
            return;
        }

        this.log(`Opening folder: ${folderKey}`, 'info');

        try {
            if (window.__TAURI__) {
                await window.__TAURI__.core.invoke('open_path', { path: path });
                this.log(`Opened: ${path.split('\\').pop()}`, 'success');
            } else {
                this.log(`[DEV] Would open: ${path}`, 'info');
            }
        } catch (error) {
            this.log(`Error opening folder: ${error.message}`, 'error');
        }
    },

    // ==================== SESSION MANAGEMENT ====================
    startSession: async function() {
        const now = new Date();
        const sessionId = now.toISOString().replace(/[:.]/g, '-');

        localStorage.setItem('current_session', JSON.stringify({
            id: sessionId,
            startTime: now.toISOString(),
            objectives: []
        }));

        this.log(`Session started: ${sessionId}`, 'success');
        this.log('Initializing work session...', 'info');

        // Open daily diary
        await this.openDailyDiary();
    },

    endSession: async function() {
        const session = JSON.parse(localStorage.getItem('current_session') || '{}');
        if (!session.id) {
            this.log('No active session to end', 'error');
            return;
        }

        session.endTime = new Date().toISOString();
        localStorage.setItem('last_session', JSON.stringify(session));
        localStorage.removeItem('current_session');

        this.log(`Session ended: ${session.id}`, 'success');
        this.log('Running EOS protocols...', 'info');

        await this.performEOS();
    },

    syncProtocols: async function() {
        this.log('Syncing protocol documents...', 'info');

        try {
            if (window.__TAURI__) {
                await window.__TAURI__.core.invoke('run_powershell_script', {
                    scriptPath: `${this.paths.scripts}\\sync_protocols.ps1`
                });
                this.log('Protocol sync completed', 'success');
            } else {
                this.log('[DEV] Would run sync_protocols.ps1', 'info');
            }
        } catch (error) {
            this.log(`Sync error: ${error.message}`, 'error');
        }
    },

    deepDiveRecall: async function() {
        this.log('Loading full context from memory...', 'info');

        // Use Claude to generate context summary
        const prompt = `Load and summarize the current project context including:
1. Recent session summaries from the session journal
2. Current project state and objectives
3. Outstanding tasks and blockers
4. Key decisions and technical notes

Provide a comprehensive context briefing.`;

        document.getElementById('claude-input').value = prompt;
        await this.sendMessage();
    },

    performEOS: async function() {
        this.log('Executing end-of-session protocols...', 'info');

        try {
            if (window.__TAURI__) {
                await window.__TAURI__.core.invoke('run_powershell_script', {
                    scriptPath: `${this.paths.scripts}\\EOS_Protocol.ps1`
                });
                this.log('EOS protocols completed', 'success');
            } else {
                this.log('[DEV] Would run EOS_Protocol.ps1', 'info');
            }
        } catch (error) {
            this.log(`EOS error: ${error.message}`, 'error');
        }
    },

    updateLivingDocs: async function() {
        this.log('Syncing living documents to Drive...', 'info');

        try {
            if (window.__TAURI__) {
                await window.__TAURI__.core.invoke('run_powershell_script', {
                    scriptPath: `${this.paths.scripts}\\update_living_docs.ps1`
                });
                this.log('Living documents updated', 'success');
            } else {
                this.log('[DEV] Would run update_living_docs.ps1', 'info');
            }
        } catch (error) {
            this.log(`Update error: ${error.message}`, 'error');
        }
    },

    // ==================== LIVING DOCUMENTS ====================
    openDailyDiary: async function() {
        const today = new Date().toISOString().split('T')[0];
        const path = `${this.paths.morningDocs}\\Daily_Diary_${today}.md`;

        this.log(`Opening daily diary: ${today}`, 'info');
        await this.openOrCreateDocument(path, this.getDiaryTemplate(today));
    },

    openTechJournal: async function() {
        const path = `${this.paths.commandCenter}\\Technical_Journal.md`;
        this.log('Opening technical journal', 'info');
        await this.openDocument(path);
    },

    openPOV: async function() {
        const path = `${this.paths.commandCenter}\\Bills_POV.md`;
        this.log('Opening POV document', 'info');
        await this.openDocument(path);
    },

    openProtocols: async function() {
        const path = `${this.paths.commandCenter}\\OPERATIONAL_PROTOCOL.md`;
        this.log('Opening operational protocols', 'info');
        await this.openDocument(path);
    },

    openDocument: async function(path) {
        try {
            if (window.__TAURI__) {
                await window.__TAURI__.core.invoke('open_path', { path: path });
                this.log(`Opened document`, 'success');
            } else {
                this.log(`[DEV] Would open: ${path}`, 'info');
            }
        } catch (error) {
            this.log(`Error opening document: ${error.message}`, 'error');
        }
    },

    openOrCreateDocument: async function(path, template) {
        try {
            if (window.__TAURI__) {
                const exists = await window.__TAURI__.core.invoke('file_exists', { path: path });
                if (!exists) {
                    await window.__TAURI__.core.invoke('write_file', { path: path, content: template });
                    this.log('Created new document', 'info');
                }
                await window.__TAURI__.core.invoke('open_path', { path: path });
                this.log('Opened document', 'success');
            } else {
                this.log(`[DEV] Would open/create: ${path}`, 'info');
            }
        } catch (error) {
            this.log(`Error: ${error.message}`, 'error');
        }
    },

    getDiaryTemplate: function(date) {
        return `# Daily Diary - ${date}

## Session Start


## Objectives


## Accomplishments


## Issues / Blockers


## Notes


## Next Steps

`;
    },

    // ==================== CLAUDE ASSISTANT ====================
    handleKeyDown: function(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            this.sendMessage();
        }
    },

    sendMessage: async function() {
        const input = document.getElementById('claude-input');
        const message = input.value.trim();
        if (!message) return;

        // Add to UI
        this.addMessage(message, 'user');
        input.value = '';

        this.log('Sending message to Claude...', 'info');

        // Get API key
        if (!this.apiKey) {
            await this.loadApiKey();
        }

        if (!this.apiKey) {
            this.addMessage('Error: No API key available. Please add ANTHROPIC_API_KEY to credentials.', 'assistant');
            this.log('API key not found', 'error');
            return;
        }

        // Add to history
        this.conversationHistory.push({ role: 'user', content: message });

        // Stream response
        await this.streamClaudeResponse();
    },

    addMessage: function(content, role) {
        const container = document.getElementById('claude-response');
        const msgEl = document.createElement('div');
        msgEl.className = `message ${role}`;
        msgEl.textContent = content;
        container.appendChild(msgEl);
        container.scrollTop = container.scrollHeight;
        return msgEl;
    },

    loadApiKey: async function() {
        // Try localStorage first
        this.apiKey = localStorage.getItem('anthropic_api_key');
        if (this.apiKey) {
            this.log('API key loaded from storage', 'info');
            return;
        }

        // Try to read from .env file via Tauri
        if (window.__TAURI__) {
            try {
                const envContent = await window.__TAURI__.core.invoke('read_file', {
                    path: `${this.paths.credentials}\\.env`
                });
                const match = envContent.match(/ANTHROPIC_API_KEY=(.+)/);
                if (match) {
                    this.apiKey = match[1].trim();
                    localStorage.setItem('anthropic_api_key', this.apiKey);
                    this.log('API key loaded from .env', 'success');
                }
            } catch (error) {
                this.log('Could not read .env file', 'error');
            }
        }

        // Fallback: prompt user
        if (!this.apiKey) {
            this.apiKey = prompt('Enter your Anthropic API key:');
            if (this.apiKey) {
                localStorage.setItem('anthropic_api_key', this.apiKey);
                this.log('API key saved', 'success');
            }
        }
    },

    streamClaudeResponse: async function() {
        // Create message element for streaming
        const msgEl = this.addMessage('', 'assistant');
        let fullResponse = '';

        try {
            const response = await fetch('https://api.anthropic.com/v1/messages', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'x-api-key': this.apiKey,
                    'anthropic-version': '2023-06-01',
                    'anthropic-dangerous-direct-browser-access': 'true'
                },
                body: JSON.stringify({
                    model: 'claude-sonnet-4-20250514',
                    max_tokens: 4096,
                    stream: true,
                    system: `You are a helpful developer assistant for the Trajanus Command Center.
You help with session management, code review, documentation, and development tasks.
Be concise and professional. Format responses for readability.`,
                    messages: this.conversationHistory
                })
            });

            if (!response.ok) {
                const error = await response.json();
                if (response.status === 401) {
                    localStorage.removeItem('anthropic_api_key');
                    this.apiKey = null;
                }
                throw new Error(error.error?.message || 'API request failed');
            }

            const reader = response.body.getReader();
            const decoder = new TextDecoder();

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value);
                const lines = chunk.split('\n');

                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        const data = line.slice(6);
                        if (data === '[DONE]') continue;

                        try {
                            const parsed = JSON.parse(data);
                            if (parsed.type === 'content_block_delta' && parsed.delta?.text) {
                                fullResponse += parsed.delta.text;
                                msgEl.textContent = fullResponse;

                                // Auto-scroll
                                const container = document.getElementById('claude-response');
                                container.scrollTop = container.scrollHeight;
                            }
                        } catch (e) {
                            // Skip invalid JSON lines
                        }
                    }
                }
            }

            this.conversationHistory.push({ role: 'assistant', content: fullResponse });
            this.log('Response received', 'success');

        } catch (error) {
            msgEl.textContent = 'Error: ' + error.message;
            this.log(`API error: ${error.message}`, 'error');
        }
    }
};

// ==================== INITIALIZE ON LOAD ====================
document.addEventListener('DOMContentLoaded', function() {
    DevToolkit.init();
});
