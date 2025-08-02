from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Mock PM data (based on your Standard Chartered experience)
MOCK_TASKS = [
    {
        "id": "BANK-001",
        "title": "Straight2Bank Portal Login Optimization", 
        "status": "In Progress",
        "assignee": "Dev Team Alpha",
        "priority": "High",
        "blockers": ["Waiting for security review"],
        "sprint": "Sprint 24"
    },
    {
        "id": "BANK-002", 
        "title": "Dashboard Performance Improvement",
        "status": "Code Review",
        "assignee": "Sarah Johnson",
        "priority": "Medium", 
        "blockers": [],
        "sprint": "Sprint 24"
    },
    {
        "id": "BANK-003",
        "title": "Regional Release Pipeline",
        "status": "Testing",
        "assignee": "Mike Chen", 
        "priority": "High",
        "blockers": ["Database migration pending"],
        "sprint": "Sprint 25"
    }
]

# Simple HTML template for testing
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>PM Assistant - MVP</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        .chat-box { border: 1px solid #ddd; height: 400px; overflow-y: scroll; padding: 20px; margin: 20px 0; }
        .message { margin: 10px 0; padding: 10px; border-radius: 8px; }
        .user { background: #007bff; color: white; text-align: right; }
        .bot { background: #f8f9fa; border-left: 4px solid #007bff; }
        .input-area { display: flex; margin-top: 20px; }
        .input-area input { flex: 1; padding: 12px; font-size: 16px; }
        .input-area button { padding: 12px 24px; background: #007bff; color: white; border: none; cursor: pointer; }
        .task-card { background: #fff; border: 1px solid #eee; padding: 15px; margin: 10px 0; border-radius: 8px; }
        .high-priority { border-left: 4px solid #dc3545; }
        .medium-priority { border-left: 4px solid #ffc107; }
    </style>
</head>
<body>
    <h1>🤖 PM Assistant MVP</h1>
    <p><strong>Try asking:</strong> "What's the status of login?" or "Who's working on dashboard?" or "Show me high priority tasks"</p>
    
    <div id="chat-box" class="chat-box">
        <div class="message bot">Hi! I'm your PM Assistant. Ask me about task status, assignments, or sprint progress.</div>
    </div>
    
    <div class="input-area">
        <input type="text" id="user-input" placeholder="Ask about task status, assignments, or blockers...">
        <button onclick="sendMessage()">Send</button>
    </div>

    <script>
        function sendMessage() {
            const input = document.getElementById('user-input');
            const message = input.value.trim();
            if (!message) return;

            addMessage(message, 'user');
            input.value = '';

            fetch('/api/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: message})
            })
            .then(response => response.json())
            .then(data => {
                addMessage(data.response, 'bot');
            })
            .catch(error => {
                addMessage('Sorry, there was an error. Please try again.', 'bot');
            });
        }

        function addMessage(text, sender) {
            const chatBox = document.getElementById('chat-box');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}`;
            messageDiv.innerHTML = text;
            chatBox.appendChild(messageDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        document.getElementById('user-input').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') sendMessage();
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/health')
def health():
    return jsonify({"status": "PM Assistant is running!", "version": "1.0"})

@app.route('/api/tasks')
def get_tasks():
    return jsonify(MOCK_TASKS)

@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '').lower()
    
    # Simple keyword-based responses (before adding AI)
    if 'login' in user_message:
        task = next((t for t in MOCK_TASKS if 'login' in t['title'].lower()), None)
        if task:
            blockers_text = f", 🚨 Blocked by: {', '.join(task['blockers'])}" if task['blockers'] else ""
            response = f"<div class='task-card high-priority'><strong>{task['title']}</strong><br/>Status: {task['status']}<br/>Assignee: {task['assignee']}<br/>Priority: {task['priority']}{blockers_text}</div>"
        else:
            response = "No login-related tasks found."
    
    elif 'dashboard' in user_message:
        task = next((t for t in MOCK_TASKS if 'dashboard' in t['title'].lower()), None)
        if task:
            response = f"<div class='task-card medium-priority'><strong>{task['title']}</strong><br/>Status: {task['status']}<br/>Assignee: {task['assignee']}<br/>Priority: {task['priority']}</div>"
        else:
            response = "No dashboard-related tasks found."
    
    elif 'high priority' in user_message or 'priority' in user_message:
        high_priority_tasks = [t for t in MOCK_TASKS if t['priority'] == 'High']
        if high_priority_tasks:
            response = "<strong>🔥 High Priority Tasks:</strong><br/>"
            for task in high_priority_tasks:
                blockers_text = f"<br/>🚨 Blockers: {', '.join(task['blockers'])}" if task['blockers'] else ""
                response += f"<div class='task-card high-priority'>{task['title']} - {task['status']} ({task['assignee']}){blockers_text}</div>"
        else:
            response = "No high priority tasks found."
    
    elif 'who' in user_message and 'working' in user_message:
        response = "<strong>👥 Current Assignments:</strong><br/>"
        for task in MOCK_TASKS:
            response += f"<div class='task-card'>{task['assignee']}: {task['title']} ({task['status']})</div>"
    
    elif 'blocked' in user_message or 'blocker' in user_message:
        blocked_tasks = [t for t in MOCK_TASKS if t['blockers']]
        if blocked_tasks:
            response = "<strong>🚨 Blocked Tasks:</strong><br/>"
            for task in blocked_tasks:
                response += f"<div class='task-card high-priority'>{task['title']}<br/>Assignee: {task['assignee']}<br/>Blockers: {', '.join(task['blockers'])}</div>"
        else:
            response = "🎉 No blocked tasks! Everything is moving smoothly."
    
    else:
        response = """I can help you with:<br/>
        • <strong>"What's the status of login?"</strong> - Check specific task status<br/>
        • <strong>"Who's working on dashboard?"</strong> - Find task assignments<br/>
        • <strong>"Show me high priority tasks"</strong> - View priority items<br/>
        • <strong>"What's blocked?"</strong> - See current blockers<br/>
        • <strong>"Who's working on what?"</strong> - Team assignments overview"""

    return jsonify({"response": response})

if __name__ == '__main__':
    print("🚀 Starting PM Assistant...")
    print("💡 Open your browser to: http://localhost:5000")
    app.run(debug=True, port=5000)