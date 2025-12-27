// Trajanus Enterprise Hub - Workspace Controller

const Workspace = {
    outputContent: '',

    init: function() {
        this.initReviewPanel();
        this.initClaudePanel();
    },

    // Panel 3: Review/Modify
    initReviewPanel: function() {
        const panel = document.getElementById('review-modify');
        if (!panel) return;

        panel.innerHTML = `
            <h2>Review / Modify</h2>
            <div class="panel-content">
                <div class="output-area" id="output-area" contenteditable="true"></div>
                <div class="output-actions">
                    <button class="btn" onclick="Workspace.copyOutput()">Copy</button>
                    <button class="btn" onclick="Workspace.exportOutput('md')">Export MD</button>
                    <button class="btn" onclick="Workspace.exportOutput('txt')">Export TXT</button>
                    <button class="btn" onclick="Workspace.clearOutput()">Clear</button>
                </div>
            </div>
        `;
    },

    // Panel 4: Claude Assistant
    initClaudePanel: function() {
        const panel = document.getElementById('claude-assistant');
        if (!panel) return;

        panel.innerHTML = `
            <h2>Claude Assistant</h2>
            <div class="chat-container">
                <div class="context-indicator" id="context-indicator">
                    No documents selected for context
                </div>
                <div class="chat-messages" id="chat-messages"></div>
                <div class="chat-input-area">
                    <textarea class="chat-input" id="chat-input"
                              placeholder="Type your message..."
                              rows="3"
                              onkeydown="Workspace.handleKeyDown(event)"></textarea>
                    <button class="btn btn-primary" onclick="Workspace.sendMessage()">Send</button>
                </div>
            </div>
        `;

        // Update context indicator
        if (typeof FileManager !== 'undefined') {
            FileManager.updateContextIndicator();
        }
    },

    handleKeyDown: function(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            this.sendMessage();
        }
    },

    sendMessage: async function() {
        const input = document.getElementById('chat-input');
        const message = input.value.trim();
        if (!message) return;

        // Add user message to chat
        this.addChatMessage(message, 'user');
        input.value = '';

        // Get context
        const selectedDocs = typeof FileManager !== 'undefined'
            ? FileManager.getSelectedContent()
            : [];

        const template = typeof Templates !== 'undefined'
            ? Templates.getCurrentTemplate()
            : null;

        const systemPrompt = typeof Templates !== 'undefined'
            ? Templates.getSystemPrompt()
            : '';

        // Build context string
        let contextStr = '';
        if (selectedDocs.length > 0) {
            contextStr = '\n\nContext Documents:\n' + selectedDocs.map(doc =>
                `--- ${doc.name} ---\n${doc.content}\n`
            ).join('\n');
        }

        // Show thinking indicator
        const thinkingId = this.addChatMessage('Thinking...', 'assistant');

        try {
            const response = await this.callClaude(systemPrompt, message + contextStr);

            // Update thinking message with response
            this.updateChatMessage(thinkingId, response);

            // Also put in output area
            this.setOutput(response);
        } catch (error) {
            this.updateChatMessage(thinkingId, 'Error: ' + error.message);
        }
    },

    addChatMessage: function(content, role) {
        const messagesEl = document.getElementById('chat-messages');
        if (!messagesEl) return null;

        const id = 'msg-' + Date.now();
        const messageEl = document.createElement('div');
        messageEl.id = id;
        messageEl.className = `chat-message ${role}`;
        messageEl.textContent = content;
        messagesEl.appendChild(messageEl);
        messagesEl.scrollTop = messagesEl.scrollHeight;
        return id;
    },

    updateChatMessage: function(id, content) {
        const messageEl = document.getElementById(id);
        if (messageEl) {
            messageEl.textContent = content;
        }
    },

    callClaude: async function(systemPrompt, userMessage) {
        // Check for API key in localStorage or prompt user
        let apiKey = localStorage.getItem('anthropic_api_key');

        if (!apiKey) {
            apiKey = prompt('Enter your Anthropic API key:');
            if (apiKey) {
                localStorage.setItem('anthropic_api_key', apiKey);
            } else {
                throw new Error('API key required');
            }
        }

        const response = await fetch('https://api.anthropic.com/v1/messages', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'x-api-key': apiKey,
                'anthropic-version': '2023-06-01',
                'anthropic-dangerous-direct-browser-access': 'true'
            },
            body: JSON.stringify({
                model: 'claude-sonnet-4-20250514',
                max_tokens: 4096,
                system: systemPrompt || 'You are a helpful assistant.',
                messages: [
                    { role: 'user', content: userMessage }
                ]
            })
        });

        if (!response.ok) {
            const error = await response.json();
            if (response.status === 401) {
                localStorage.removeItem('anthropic_api_key');
            }
            throw new Error(error.error?.message || 'API request failed');
        }

        const data = await response.json();
        return data.content[0].text;
    },

    // Output Panel Functions
    setOutput: function(content) {
        this.outputContent = content;
        const outputArea = document.getElementById('output-area');
        if (outputArea) {
            outputArea.textContent = content;
        }
    },

    getOutput: function() {
        const outputArea = document.getElementById('output-area');
        return outputArea ? outputArea.textContent : this.outputContent;
    },

    copyOutput: function() {
        const content = this.getOutput();
        navigator.clipboard.writeText(content).then(() => {
            this.showNotification('Copied to clipboard');
        }).catch(err => {
            console.error('Failed to copy:', err);
        });
    },

    exportOutput: function(format) {
        const content = this.getOutput();
        if (!content) {
            this.showNotification('Nothing to export');
            return;
        }

        const filename = `output_${Date.now()}.${format}`;
        const blob = new Blob([content], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);

        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.click();

        URL.revokeObjectURL(url);
        this.showNotification(`Exported as ${filename}`);
    },

    clearOutput: function() {
        this.outputContent = '';
        const outputArea = document.getElementById('output-area');
        if (outputArea) {
            outputArea.textContent = '';
        }
    },

    showNotification: function(message) {
        // Simple notification - could be enhanced
        const notification = document.createElement('div');
        notification.className = 'notification';
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: var(--accent-blue);
            color: white;
            padding: 0.75rem 1.5rem;
            border-radius: 4px;
            z-index: 1000;
            animation: fadeIn 0.2s ease;
        `;
        document.body.appendChild(notification);

        setTimeout(() => {
            notification.remove();
        }, 2000);
    }
};

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('review-modify') || document.getElementById('claude-assistant')) {
        Workspace.init();
    }
});
