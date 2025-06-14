from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import os

app = Flask(__name__)

# Use an environment variable for better security
app.secret_key = os.environ.get('SECRET_KEY', 'fallback-secret-key')

# Chatbot endpoint
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '')
    response = f"PulseBot says: Jesus loves you and wants a relationship with you! You said: '{message}'"
    return jsonify({"response": response})

# Admin login route
@app.route('/admin')
def admin_login():
    if not session.get('logged_in'):
        return render_template('login.html')
    return redirect('/admin-panel')

# Handle login form POST
@app.route('/admin-login', methods=['POST'])
def do_admin_login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Simple auth — replace with hashed passwords in production
    if username == 'admin' and password == 'password':
        session['logged_in'] = True
        return redirect('/admin-panel')

    return 'Invalid credentials', 401

# Admin dashboard
@app.route('/admin-panel')
def admin_panel():
    if not session.get('logged_in'):
        return redirect('/admin')
    return render_template('admin.html')

# Entry point for Render
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
