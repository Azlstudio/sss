// LocalAI Assistant - Web Client
const API_URL = '/api';
let currentDomain = 'general';
let isLoading = false;

// DOM Elements
const chatMessages = document.getElementById('chat-messages');
const inputMessage = document.getElementById('input-message');
const chatForm = document.getElementById('chat-form');
const domainBtns = document.querySelectorAll('.domain-btn');
const btnMemory = document.getElementById('btn-memory');
const btnSettings = document.getElementById('btn-settings');
const memoryModal = document.getElementById('memory-modal');
const settingsModal = document.getElementById('settings-modal');

// Event Listeners
chatForm.addEventListener('submit', handleChat);
domainBtns.forEach(btn => btn.addEventListener('click', handleDomain));
btnMemory.addEventListener('click', showMemory);
btnSettings.addEventListener('click', () => openModal('settings-modal'));

// Auto-resize textarea
inputMessage.addEventListener('input', () => {
    inputMessage.style.height = 'auto';
    inputMessage.style.height = Math.min(inputMessage.scrollHeight, 120) + 'px';
});

// Enter to send, Shift+Enter for newline
inputMessage.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        chatForm.dispatchEvent(new Event('submit'));
    }
});

/**
 * Handle chat submission
 */
async function handleChat(e) {
    e.preventDefault();

    const message = inputMessage.value.trim();
    if (!message || isLoading) return;

    // Add user message
    addMessage('user', message);
    inputMessage.value = '';
    inputMessage.style.height = 'auto';
    isLoading = true;

    try {
        // Send to API
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: message,
                domain: currentDomain
            })
        });

        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }

        const data = await response.json();

        // Update domain if changed
        if (data.domain !== currentDomain) {
            currentDomain = data.domain;
            updateDomainButtons();
        }

        // Add assistant message
        addMessage('assistant', data.response);

        // Show notification if facts were learned
        if (data.facts_learned && data.facts_learned.length > 0) {
            showNotification(`📚 Learned: ${data.facts_learned.join(', ')}`);
        }

    } catch (error) {
        console.error('Error:', error);
        addMessage('assistant', `❌ Error: ${error.message}`);
    } finally {
        isLoading = false;
    }
}

/**
 * Add message to chat
 */
function addMessage(role, content) {
    // Remove welcome message if exists
    const welcome = document.querySelector('.welcome-message');
    if (welcome) {
        welcome.remove();
    }

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.innerHTML = role === 'user' ? '👤' : '🤖';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = content;

    // Format content if it's markdown-like
    if (role === 'assistant') {
        contentDiv.innerHTML = formatContent(content);
    }

    const timeDiv = document.createElement('div');
    timeDiv.className = 'message-time';
    timeDiv.textContent = new Date().toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
    });

    if (role === 'user') {
        messageDiv.appendChild(contentDiv);
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(timeDiv);
    } else {
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(contentDiv);
        messageDiv.appendChild(timeDiv);
    }

    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

/**
 * Format content for display
 */
function formatContent(content) {
    return content
        // Code blocks
        .replace(/```(.*?)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
        // Bold
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        // Italic
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        // Links
        .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank">$1</a>')
        // Line breaks
        .replace(/\n/g, '<br>')
        // Escape HTML
        .split('<br>').join('<br>');
}

/**
 * Handle domain selection
 */
async function handleDomain(e) {
    const domain = e.currentTarget.dataset.domain;
    if (domain === currentDomain) return;

    try {
        const response = await fetch(`${API_URL}/domain`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ domain })
        });

        if (response.ok) {
            currentDomain = domain;
            updateDomainButtons();
            showNotification(`✨ Switched to ${domain.toUpperCase()} domain`);
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('❌ Failed to switch domain');
    }
}

/**
 * Update domain button states
 */
function updateDomainButtons() {
    domainBtns.forEach(btn => {
        btn.classList.toggle('active', btn.dataset.domain === currentDomain);
    });
}

/**
 * Show memory statistics
 */
async function showMemory() {
    openModal('memory-modal');

    try {
        const response = await fetch(`${API_URL}/memory`);
        const data = await response.json();

        const html = `
            <div class="memory-stats">
                <div class="stat-group">
                    <h3>📝 Vector Store (Semantic Memories)</h3>
                    <p>${data.vector_store.total_memories} memories</p>
                </div>
                <div class="stat-group">
                    <h3>📚 Fact Store</h3>
                    <p>${data.fact_store.facts} facts</p>
                    <p>${data.fact_store.preferences} preferences</p>
                    <p>${data.fact_store.projects} projects</p>
                    <p>${data.fact_store.interactions} interactions</p>
                </div>
                <div class="stat-group">
                    <h3>💬 Conversation</h3>
                    <p>${data.conversation.total_messages} messages</p>
                    <p>User: ${data.conversation.user_messages}</p>
                    <p>Assistant: ${data.conversation.assistant_messages}</p>
                </div>
            </div>
        `;

        document.getElementById('memory-content').innerHTML = html;
    } catch (error) {
        document.getElementById('memory-content').innerHTML = `
            <p style="color: #ef4444;">❌ Error loading memory stats</p>
        `;
    }
}

/**
 * Open modal
 */
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.classList.add('active');
}

/**
 * Close modal
 */
function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.classList.remove('active');
}

/**
 * Show notification
 */
function showNotification(message) {
    // Create notification element
    const notif = document.createElement('div');
    notif.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        padding: 12px 16px;
        border-radius: var(--radius-md);
        color: var(--text-primary);
        font-size: 14px;
        animation: slideUp 0.3s ease-out;
        z-index: 999;
        max-width: 300px;
    `;
    notif.textContent = message;
    document.body.appendChild(notif);

    // Remove after 3 seconds
    setTimeout(() => notif.remove(), 3000);
}

/**
 * Initialize
 */
function init() {
    updateDomainButtons();
    console.log('🤖 LocalAI Assistant Web Ready');
}

// Initialize on load
document.addEventListener('DOMContentLoaded', init);

// Handle modal close on outside click
document.querySelectorAll('.modal').forEach(modal => {
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.remove('active');
        }
    });
});

// Settings
const tempSlider = document.getElementById('temp-slider');
const tempValue = document.getElementById('temp-value');
if (tempSlider) {
    tempSlider.addEventListener('input', () => {
        tempValue.textContent = tempSlider.value;
    });
}

const tokensSlider = document.getElementById('tokens-slider');
const tokensValue = document.getElementById('tokens-value');
if (tokensSlider) {
    tokensSlider.addEventListener('input', () => {
        tokensValue.textContent = tokensSlider.value;
    });
}

const themeSelect = document.getElementById('theme-select');
if (themeSelect) {
    themeSelect.addEventListener('change', (e) => {
        if (e.target.value === 'light') {
            document.body.classList.add('light-theme');
            localStorage.setItem('theme', 'light');
        } else {
            document.body.classList.remove('light-theme');
            localStorage.setItem('theme', 'dark');
        }
    });

    // Load saved theme
    const savedTheme = localStorage.getItem('theme') || 'dark';
    themeSelect.value = savedTheme;
    if (savedTheme === 'light') {
        document.body.classList.add('light-theme');
    }
}
