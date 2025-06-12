from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key'

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '')
    response = f"PulseBot says: Jesus loves you and wants a relationship with you! You said: '{message}'"
    return jsonify({"response": response})

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

if __name__ == '__main__':
    app.run(debug=True)
