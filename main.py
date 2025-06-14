from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'default-secret-key')  # Set securely in Render

# Root Route: Suggest landing or redirect
@app.route('/')
def home():
    return render_template('chat.html')  # Or use redirect(url_for('admin_login'))

# Chat Endpoint (API)
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '')
    response = f"PulseBot says: Jesus loves you and wants a relationship with you! You said: '{message}'"
    return jsonify({"response": response})

# Admin Login Page
@app.route('/admin')
def admin_login():
    if not session.get('logged_in'):
        return render_template('login.html')
    return redirect(url_for('admin_panel'))

# Admin Login Form Processor
@app.route('/admin-login', methods=['POST'])
def do_admin_login():
    if request.form['username'] == 'admin' and request.form['password'] == 'password':
        session['logged_in'] = True
        return redirect(url_for('admin_panel'))
    return 'Invalid credentials', 401

# Admin Panel View
@app.route('/admin-panel')
def admin_panel():
    if not session.get('logged_in'):
        return redirect(url_for('admin_login'))
    return render_template('admin.html')

# Start the app with production-ready host/port binding
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


# Entry point for Render
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
