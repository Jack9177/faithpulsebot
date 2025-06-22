from flask import Flask, request, jsonify, render_template, redirect, url_for, session, send_file
import os
import logging
import openai

# === App Setup ===
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "fallback-secret")

# === Logging Setup ===
LOG_DIR = 'logs'
LOG_FILE = os.path.join(LOG_DIR, 'pulsebot.log')
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# === OpenAI Setup ===
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_ai_response(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are PulseBot, a helpful and loving Christian assistant who answers using Scripture, truth, and hope."},
                {"role": "user", "content": message}
            ]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print("OpenAI error:", e)
        logging.error(f"OpenAI error: {e}")
        return "Sorry, I'm having trouble answering right now. Please try again later."

# === Routes ===

@app.route('/')
def home():
    return render_template('dashboard.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '').strip()

    if not message:
        return jsonify({"response": "Please enter a message."}), 400

    response = get_ai_response(message)
    logging.info(f"User: {message} | Response: {response}")
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

# === App Runner ===
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
