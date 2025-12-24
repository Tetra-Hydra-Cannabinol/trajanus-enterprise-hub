// inject-chat.js - Loads working chat on button click

function openChatPanel() {
    // Check if already exists
    if (document.getElementById('injectedChatPanel')) {
        console.log('Chat already open');
        return;
    }
    
    // Inject CSS
    const style = document.createElement('style');
    style.textContent = `
        #injectedChatPanel {
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 400px;
            height: 500px;
            background: rgba(31, 20, 16, 0.98);
            border: 2px solid #cc6e1f;
            border-radius: 10px;
            display: flex;
            flex-direction: column;
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.5);
            z-index: 10000;
        }
        
        .injected-chat-header {
            background: linear-gradient(90deg, #a85a1b, #cc6e1f);
            padding: 12px 15px;
            border-radius: 8px 8px 0 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .injected-chat-header h3 {
            color: #fff;
            font-size: 14px;
            margin: 0;
            letter-spacing: 2px;
        }
        
        .injected-close-btn {
            background: none;
            border: none;
            color: #fff;
            font-size: 20px;
            cursor: pointer;
            padding: 0;
        }
        
        .injected-chat-messages {
            flex: 1;
            padding: 15px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        
        .injected-message {
            padding: 10px 12px;
            border-radius: 8px;
            max-width: 85%;
            font-size: 13px;
            line-height: 1.5;
            word-wrap: break-word;
        }
        
        .injected-message.user {
            background: #cc6e1f;
            color: #fff;
            align-self: flex-end;
        }
        
        .injected-message.assistant {
            background: rgba(255, 255, 255, 0.1);
            color: #FFF8F0;
            align-self: flex-start;
        }
        
        .injected-input-container {
            padding: 12px 15px;
            background: rgba(0, 0, 0, 0.3);
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            display: flex;
            gap: 10px;
        }
        
        .injected-input {
            flex: 1;
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 6px;
            padding: 10px 12px;
            color: #fff;
            font-size: 13px;
            resize: none;
            font-family: inherit;
        }
        
        .injected-send-btn {
            background: #cc6e1f;
            border: none;
            border-radius: 6px;
            color: #fff;
            padding: 10px 20px;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
        }
        
        .injected-send-btn:hover {
            background: #e8922a;
        }
    `;
    document.head.appendChild(style);
    
    // Create chat HTML
    const chatPanel = document.createElement('div');
    chatPanel.id = 'injectedChatPanel';
    chatPanel.innerHTML = `
        <div class="injected-chat-header">
            <h3>CLAUDE ASSISTANT</h3>
            <button class="injected-close-btn" onclick="closeChatPanel()">×</button>
        </div>
        
        <div class="injected-chat-messages" id="injectedMessages">
            <div class="injected-message assistant">
                Chat loaded! Type a message to test.
            </div>
        </div>
        
        <div class="injected-input-container">
            <textarea id="injectedInput" class="injected-input" placeholder="Type message..." rows="2"></textarea>
            <button class="injected-send-btn" onclick="sendInjectedMessage()">Send</button>
        </div>
    `;
    
    document.body.appendChild(chatPanel);
    
    console.log('Chat panel injected successfully');
}

function sendInjectedMessage() {
    const input = document.getElementById('injectedInput');
    const messages = document.getElementById('injectedMessages');
    
    const text = input.value.trim();
    if (!text) return;
    
    // Add user message
    const userMsg = document.createElement('div');
    userMsg.className = 'injected-message user';
    userMsg.textContent = text;
    messages.appendChild(userMsg);
    
    input.value = '';
    messages.scrollTop = messages.scrollHeight;
    
    // Add response
    setTimeout(() => {
        const botMsg = document.createElement('div');
        botMsg.className = 'injected-message assistant';
        botMsg.textContent = 'Chat is working! You said: "' + text + '"';
        messages.appendChild(botMsg);
        messages.scrollTop = messages.scrollHeight;
    }, 500);
}

function closeChatPanel() {
    const panel = document.getElementById('injectedChatPanel');
    if (panel) panel.remove();
}

console.log('inject-chat.js loaded - ready to open chat');
