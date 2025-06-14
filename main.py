from flask import Flask, request, jsonify, render_template, redirect, url_for, session, send_file
import os
import logging
from datetime import datetime

# App setup
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "fallback-secret")

# Logging setup
LOG_DIR = 'logs'
LOG_FILE = os.path.join(LOG_DIR, 'pulsebot.log')
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Routes

@app.route('/')
def home():
    return render_template('dashboard.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '')
    response = f"PulseBot says: Jesus loves you and wants a relationship with you! You said: '{message}'"

    logging.info(f"Chat message: {message}")
    return jsonify({"response": response})

@app.route('/pray')
def pray():
    prayer = (
        "Dear Jesus, I acknowledge that I am a sinner. "
        "I believe You died for my sins and rose again. "
        "I invite You into my heart as my Lord and Savior. "
        "Thank You for saving me. Amen."
    )
    return render_template("dashboard.html", prayer=prayer)

@app.route('/admin')
def admin_login():
    if not session.get('logged_in'):
        return render_template('login.html')
    return redirect(url_for('admin_panel'))

@app.route('/admin-login', methods=['POST'])
def do_admin_login():
    if request.form['username'] == 'admin' and request.form['password'] == 'password':
        session['logged_in'] = True
        logging.info("Admin logged in")
        return redirect(url_for('admin_panel'))
    logging.warning("Failed admin login attempt")
    return 'Invalid credentials', 401

@app.route('/admin-panel')
def admin_panel():
    if not session.get('logged_in'):
        return redirect(url_for('admin_login'))
    return render_template('admin.html')

@app.route('/admin/logs')
def view_logs():
    if not session.get('logged_in'):
        return redirect(url_for('admin_login'))
    return send_file(LOG_FILE, mimetype='text/plain', as_attachment=False)

# Run
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


# Entry point for Render
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
