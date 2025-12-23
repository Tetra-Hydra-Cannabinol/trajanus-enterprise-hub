// chat-interface.js - UI logic for Claude chat interface
// Uses electronAPI bridge to call Claude API safely

let chatHistory = [];

// Initialize chat when page loads
document.addEventListener('DOMContentLoaded', () => {
    console.log('Chat interface loaded');
    
    // Check if electronAPI is available
    if (!window.electronAPI) {
        console.error('ERROR: electronAPI not available - preload.js may not be loaded');
        addMessage('System', 'Error: Chat interface not properly initialized. Check console.', 'error');
        return;
    }
    
    console.log('electronAPI available - ready to chat');
    
    // Add initial greeting
    addMessage('Claude', 'Hi! I\'m your AI assistant. How can I help you today?', 'assistant');
    
    // Set up enter key handler for input
    const chatInput = document.getElementById('chatInput');
    if (chatInput) {
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
    }
});

async function sendMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Clear input immediately
    input.value = '';
    
    // Add user message to chat
    addMessage('You', message, 'user');
    
    // Add loading indicator
    const loadingId = addMessage('Claude', 'Thinking...', 'loading');
    
    try {
        // Call Claude API through electron bridge
        const response = await window.electronAPI.callClaudeAPI(message);
        
        // Remove loading message
        removeMessage(loadingId);
        
        if (response.success) {
            // Add Claude's response
            addMessage('Claude', response.message, 'assistant');
            
            // Store in history
            chatHistory.push(
                { role: 'user', content: message },
                { role: 'assistant', content: response.message }
            );
        } else {
            // Show error
            addMessage('System', `Error: ${response.error}`, 'error');
        }
        
    } catch (error) {
        console.error('Error sending message:', error);
        removeMessage(loadingId);
        addMessage('System', `Error: ${error.message}`, 'error');
    }
}

function addMessage(sender, text, type = 'user') {
    const messagesDiv = document.getElementById('chatMessages');
    if (!messagesDiv) {
        console.error('chatMessages div not found');
        return null;
    }
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${type}`;
    messageDiv.id = `msg-${Date.now()}`;
    
    const senderSpan = document.createElement('strong');
    senderSpan.textContent = sender + ': ';
    
    const textSpan = document.createElement('span');
    textSpan.textContent = text;
    
    messageDiv.appendChild(senderSpan);
    messageDiv.appendChild(textSpan);
    
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
    
    return messageDiv.id;
}

function removeMessage(messageId) {
    if (!messageId) return;
    const msg = document.getElementById(messageId);
    if (msg) msg.remove();
}

function toggleChat() {
    const chatPanel = document.querySelector('.chat-panel');
    if (chatPanel) {
        chatPanel.classList.toggle('minimized');
    }
}

function clearChat() {
    const messagesDiv = document.getElementById('chatMessages');
    if (messagesDiv) {
        messagesDiv.innerHTML = '';
        chatHistory = [];
        addMessage('Claude', 'Chat cleared. How can I help you?', 'assistant');
    }
}
