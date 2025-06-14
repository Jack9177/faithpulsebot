from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import os
import csv
import time

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "fallback-secret-key")

# Log file for chat messages
LOG_FILE = 'chat_logs.csv'

@app.route('/')
def landing_page():
    return redirect('/chat-ui')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '')
    response = f"PulseBot says: Jesus loves you and wants a relationship with you! You said: '{message}'"

    # Log the chat message and response
    with open(LOG_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), message, response])

    return jsonify({"response": response})

@app.route('/chat-ui')
def chat_ui():
    return render_template('chat.html')

@app.route('/salvation')
def salvation():
    prayer = (
        "Dear Jesus, I believe You died for my sins and rose again. "
        "I ask You to come into my life, forgive me, and guide me each day. Amen."
    )
    return jsonify({"prayer": prayer})

@app.route('/admin')
def admin_login():
    if not session.get('logged_in'):
        return render_template('login.html')
    return redirect('/admin-panel')

@app.route('/admin-login', methods=['POST'])
def do_admin_login():
    if request.form['username'] == 'admin' and request.form['password'] == 'password':
        session['logged_in'] = True
        return redirect('/admin-panel')
    return 'Invalid credentials', 401

@app.route('/admin-panel')
def admin_panel():
    if not session.get('logged_in'):
        return redirect('/admin')
    return render_template('admin.html')

@app.route('/admin-logs')
def admin_logs():
    if not session.get('logged_in'):
        return redirect('/admin')

    logs = []
    try:
        with open(LOG_FILE, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            logs = list(reader)
    except FileNotFoundError:
        logs = []

    return render_template('admin_logs.html', logs=logs)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)


# Entry point for Render
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
