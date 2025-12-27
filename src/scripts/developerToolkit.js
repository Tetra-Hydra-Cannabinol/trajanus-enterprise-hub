// Developer Toolkit - Control Panel Functions

const DevToolkit = {
    // Paths
    paths: {
        commandCenter: 'G:\\My Drive\\00 - Trajanus USA\\00-Command-Center',
        scripts: 'G:\\My Drive\\00 - Trajanus USA\\00-Command-Center\\05-Scripts',
        credentials: 'G:\\My Drive\\00 - Trajanus USA\\00-Command-Center\\001 Credentials',
        documents: 'G:\\My Drive\\00 - Trajanus USA\\01-Morning-Sessions',
        project: 'C:\\Dev\\trajanus-command-center'
    },

    conversationHistory: [],
    apiKey: null,

    // ==================== UTILITIES ====================

    openCommandCenter: async function() {
        await this.openFolder(this.paths.commandCenter);
    },

    openScriptsFolder: async function() {
        await this.openFolder(this.paths.scripts);
    },

    openTerminal: async function() {
        try {
            if (window.__TAURI__) {
                await window.__TAURI__.shell.open('powershell.exe', ['-NoExit', '-Command', `cd "${this.paths.project}"`]);
            } else {
                // Fallback for browser testing
                this.showStatus('Terminal: Would open PowerShell at ' + this.paths.project);
            }
        } catch (error) {
            this.showStatus('Error opening terminal: ' + error.message, 'error');
        }
    },

    gitPush: async function() {
        this.showStatus('Running git push...');
        try {
            if (window.__TAURI__) {
                const result = await window.__TAURI__.invoke('git_push', { path: this.paths.project });
                this.showStatus('Git push complete: ' + result, 'success');
            } else {
                this.showStatus('Git push: Would run in Tauri environment');
            }
        } catch (error) {
            this.showStatus('Git push failed: ' + error.message, 'error');
        }
    },

    openFolder: async function(path) {
        try {
            if (window.__TAURI__) {
                await window.__TAURI__.shell.open(path);
            } else {
                this.showStatus('Would open: ' + path);
            }
        } catch (error) {
            this.showStatus('Error opening folder: ' + error.message, 'error');
        }
    },

    // ==================== LIVING DOCUMENTS ====================

    openDailyDiary: async function() {
        const today = new Date().toISOString().split('T')[0];
        const path = `${this.paths.documents}\\Daily_Diary_${today}.md`;
        await this.openOrCreateDocument(path, this.getDiaryTemplate(today));
    },

    openTechJournal: async function() {
        const path = `${this.paths.commandCenter}\\Technical_Journal.md`;
        await this.openDocument(path);
    },

    openPOV: async function() {
        const path = `${this.paths.commandCenter}\\Bills_POV.md`;
        await this.openDocument(path);
    },

    openProtocols: async function() {
        const path = `${this.paths.commandCenter}\\OPERATIONAL_PROTOCOL.md`;
        await this.openDocument(path);
    },

    openDocument: async function(path) {
        try {
            if (window.__TAURI__) {
                await window.__TAURI__.shell.open(path);
            } else {
                this.showStatus('Would open: ' + path);
            }
        } catch (error) {
            this.showStatus('Error opening document: ' + error.message, 'error');
        }
    },

    openOrCreateDocument: async function(path, template) {
        try {
            if (window.__TAURI__) {
                // Check if file exists, create if not
                const exists = await window.__TAURI__.invoke('file_exists', { path: path });
                if (!exists) {
                    await window.__TAURI__.invoke('write_file', { path: path, content: template });
                }
                await window.__TAURI__.shell.open(path);
            } else {
                this.showStatus('Would open/create: ' + path);
            }
        } catch (error) {
            this.showStatus('Error: ' + error.message, 'error');
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

    // ==================== SCRIPTS ====================

    eosProtocol: async function() {
        this.showStatus('Running EOS Protocol...');
        // This would trigger the end-of-session protocol
        await this.runScript('EOS_Protocol.ps1');
    },

    convertFiles: async function() {
        this.showStatus('Running file conversion...');
        await this.runScript('CONVERT_NEW_FILES_ONLY.ps1');
    },

    batchIngest: async function() {
        this.showStatus('Running batch ingest...');
        await this.runPythonScript('batch_ingest_files.py');
    },

    kbQuery: async function() {
        // Open KB query in Claude Assistant
        const input = document.getElementById('claude-input');
        if (input) {
            input.value = 'Search the knowledge base for: ';
            input.focus();
            input.setSelectionRange(input.value.length, input.value.length);
        }
    },

    runScript: async function(scriptName) {
        try {
            if (window.__TAURI__) {
                const result = await window.__TAURI__.invoke('run_powershell_script', {
                    scriptPath: `${this.paths.scripts}\\${scriptName}`
                });
                this.showStatus(`${scriptName} completed`, 'success');
                return result;
            } else {
                this.showStatus(`Would run: ${scriptName}`);
            }
        } catch (error) {
            this.showStatus(`Script error: ${error.message}`, 'error');
        }
    },

    runPythonScript: async function(scriptName) {
        try {
            if (window.__TAURI__) {
                const result = await window.__TAURI__.invoke('run_python_script', {
                    scriptPath: `${this.paths.scripts}\\${scriptName}`
                });
                this.showStatus(`${scriptName} completed`, 'success');
                return result;
            } else {
                this.showStatus(`Would run: ${scriptName}`);
            }
        } catch (error) {
            this.showStatus(`Script error: ${error.message}`, 'error');
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

        this.showStatus('Session started: ' + sessionId, 'success');

        // Open daily diary
        await this.openDailyDiary();
    },

    endSession: async function() {
        const session = JSON.parse(localStorage.getItem('current_session') || '{}');
        if (!session.id) {
            this.showStatus('No active session', 'error');
            return;
        }

        session.endTime = new Date().toISOString();
        localStorage.setItem('last_session', JSON.stringify(session));
        localStorage.removeItem('current_session');

        // Trigger EOS protocol
        await this.eosProtocol();

        this.showStatus('Session ended', 'success');
    },

    sessionSummary: async function() {
        const session = JSON.parse(localStorage.getItem('current_session') || localStorage.getItem('last_session') || '{}');

        if (!session.id) {
            this.showStatus('No session data available', 'error');
            return;
        }

        // Ask Claude to generate summary
        const prompt = `Generate a session summary for session ${session.id}.
Start time: ${session.startTime}
${session.endTime ? 'End time: ' + session.endTime : 'Session still active'}

Please provide a professional summary including:
1. Duration
2. Key activities (infer from context)
3. Recommendations for next session`;

        document.getElementById('claude-input').value = prompt;
        await this.sendMessage();
    },

    handoffDoc: async function() {
        const prompt = `Generate a handoff document for the next developer session. Include:
1. Current project state
2. Pending tasks
3. Known issues
4. Environment setup notes
5. Next priority items

Format as a professional handoff document.`;

        document.getElementById('claude-input').value = prompt;
        await this.sendMessage();
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

        // Get API key
        if (!this.apiKey) {
            await this.loadApiKey();
        }

        if (!this.apiKey) {
            this.addMessage('Error: No API key available. Please add ANTHROPIC_API_KEY to credentials.', 'assistant');
            return;
        }

        // Add to history
        this.conversationHistory.push({ role: 'user', content: message });

        // Show thinking
        const thinkingEl = this.addMessage('Thinking...', 'assistant');

        try {
            const response = await this.callClaudeAPI();
            thinkingEl.textContent = response;
            this.conversationHistory.push({ role: 'assistant', content: response });
        } catch (error) {
            thinkingEl.textContent = 'Error: ' + error.message;
        }
    },

    addMessage: function(content, role) {
        const container = document.getElementById('claude-response');
        const msgEl = document.createElement('div');
        msgEl.className = 'message ' + role;
        msgEl.textContent = content;
        container.appendChild(msgEl);
        container.scrollTop = container.scrollHeight;
        return msgEl;
    },

    loadApiKey: async function() {
        // Try localStorage first
        this.apiKey = localStorage.getItem('anthropic_api_key');
        if (this.apiKey) return;

        // Try to read from .env file via Tauri
        if (window.__TAURI__) {
            try {
                const envContent = await window.__TAURI__.invoke('read_file', {
                    path: `${this.paths.credentials}\\.env`
                });
                const match = envContent.match(/ANTHROPIC_API_KEY=(.+)/);
                if (match) {
                    this.apiKey = match[1].trim();
                    localStorage.setItem('anthropic_api_key', this.apiKey);
                }
            } catch (error) {
                console.error('Could not read .env file:', error);
            }
        }

        // Fallback: prompt user
        if (!this.apiKey) {
            this.apiKey = prompt('Enter your Anthropic API key:');
            if (this.apiKey) {
                localStorage.setItem('anthropic_api_key', this.apiKey);
            }
        }
    },

    callClaudeAPI: async function() {
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
                system: `You are a helpful developer assistant for the Trajanus Enterprise Hub.
You help with session management, code review, documentation, and development tasks.
Be concise and professional.`,
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

        const data = await response.json();
        return data.content[0].text;
    },

    // ==================== UTILITIES ====================

    showStatus: function(message, type = 'info') {
        // Remove existing status
        const existing = document.querySelector('.status-message');
        if (existing) existing.remove();

        const statusEl = document.createElement('div');
        statusEl.className = 'status-message ' + type;
        statusEl.textContent = message;
        document.body.appendChild(statusEl);

        setTimeout(() => statusEl.remove(), 3000);
    }
};

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    // Check for active session
    const session = localStorage.getItem('current_session');
    if (session) {
        DevToolkit.showStatus('Active session detected', 'info');
    }
});
