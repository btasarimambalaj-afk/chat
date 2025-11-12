// Basitleştirilmiş Müşteri App
let userId = localStorage.getItem('user_id');
let userName = localStorage.getItem('user_name') || 'Anonim';
let eventSource = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    if (!userId) {
        showNameModal();
    } else {
        initChat();
    }
    setupEventListeners();
});

// Name Modal
function showNameModal() {
    document.getElementById('nameModal').classList.add('active');
}

document.getElementById('nameSubmitBtn').addEventListener('click', async () => {
    const name = document.getElementById('nameInput').value.trim() || 'Anonim';
    userId = 'user_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    userName = name;
    
    localStorage.setItem('user_id', userId);
    localStorage.setItem('user_name', userName);
    
    await registerUser();
    document.getElementById('nameModal').classList.remove('active');
    initChat();
});

// Register User
async function registerUser() {
    try {
        const res = await fetch('/api/users', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({user_id: userId, name: userName})
        });
        const data = await res.json();
        console.log('Register:', data);
        return data.success;
    } catch (error) {
        console.error('Register error:', error);
        showToast('Kayıt başarısız', 'error');
        return false;
    }
}

// Init Chat
function initChat() {
    loadMessages();
    connectSSE();
}

// Load Messages
async function loadMessages() {
    try {
        const res = await fetch(`/api/messages/${userId}`);
        const data = await res.json();
        
        if (data.success) {
            const container = document.getElementById('messagesContainer');
            container.innerHTML = '<div class="welcome-banner"><div class="welcome-icon">👋</div><div class="welcome-title">Hoş Geldiniz!</div><div class="welcome-text">Size nasıl yardımcı olabiliriz?</div></div>';
            data.messages.forEach(msg => addMessage(msg));
        }
    } catch (error) {
        console.error('Load messages error:', error);
    }
}

// SSE Connection
function connectSSE() {
    if (eventSource) return;
    
    eventSource = new EventSource(`/api/stream/${userId}`);
    
    eventSource.onmessage = (e) => {
        const data = JSON.parse(e.data);
        console.log('SSE:', data);
        
        if (data.type === 'user_deleted') {
            showToast('Oturumunuz sonlandırıldı', 'error');
            localStorage.clear();
            setTimeout(() => window.location.reload(), 2000);
            return;
        }
        
        if (data.type !== 'ping') {
            addMessage(data);
        }
    };
    
    eventSource.onerror = () => {
        console.log('SSE error, reconnecting...');
        eventSource = null;
        setTimeout(connectSSE, 5000);
    };
}

// Add Message
function addMessage(msg) {
    const container = document.getElementById('messagesContainer');
    const div = document.createElement('div');
    div.className = `message ${msg.sender_type}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = msg.sender_type === 'customer' ? userName[0].toUpperCase() : '🛡️';
    
    const content = document.createElement('div');
    content.className = 'message-content';
    
    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    bubble.textContent = msg.content;
    
    const time = document.createElement('div');
    time.className = 'message-time';
    time.textContent = formatTime(msg.created_at);
    
    content.appendChild(bubble);
    content.appendChild(time);
    div.appendChild(avatar);
    div.appendChild(content);
    container.appendChild(div);
    
    container.scrollTop = container.scrollHeight;
}

// Send Message
async function sendMessage() {
    const input = document.getElementById('messageInput');
    const text = input.value.trim();
    
    if (!text) return;
    
    console.log('Sending:', text);
    
    try {
        const res = await fetch('/api/messages', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                user_id: userId,
                sender_type: 'customer',
                message_type: 'text',
                content: text
            })
        });
        
        const data = await res.json();
        console.log('Response:', data);
        
        if (data.success) {
            input.value = '';
            input.style.height = 'auto';
            document.getElementById('sendBtn').disabled = true;
            showToast('Gönderildi', 'success');
        } else {
            showToast(data.error || 'Hata', 'error');
        }
    } catch (error) {
        console.error('Send error:', error);
        showToast('Bağlantı hatası', 'error');
    }
}

// Event Listeners
function setupEventListeners() {
    const input = document.getElementById('messageInput');
    const sendBtn = document.getElementById('sendBtn');
    
    input.addEventListener('input', () => {
        sendBtn.disabled = !input.value.trim();
        input.style.height = 'auto';
        input.style.height = Math.min(input.scrollHeight, 100) + 'px';
    });
    
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            if (input.value.trim()) {
                sendMessage();
            }
        }
    });
    
    sendBtn.addEventListener('click', sendMessage);
}

// Utilities
function formatTime(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('tr-TR', {hour: '2-digit', minute: '2-digit'});
}

function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}
