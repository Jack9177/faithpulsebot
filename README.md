# PulseBot (Faith-Based Chatbot)

A Flask-based chatbot and admin panel to help users ask questions like:  
**"Tell me about Jesus"** or **"How do I pray?"**

---

## 🚀 Deployment (e.g. Render)

1. Push code to GitHub
2. Create a new Web Service on [Render.com](https://render.com/)
3. Set:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`

---

## 💬 Endpoints

- `POST /chat` — expects `{ "message": "Tell me about Jesus" }`
- `GET /admin` — shows admin login panel

---

## 🧪 Local Development

```bash
pip install -r requirements.txt
python main.py
```

Visit `http://localhost:5000/chat` and `http://localhost:5000/admin`

---

## 🔐 Admin Login

Default credentials (can be moved to `.env` later):

- **Username**: admin
- **Password**: pulsebot123
