# 🚀 Career Path - Premium AI Career Recommendation System

A sophisticated, production-ready platform with **full authentication**, **interactive assessment**, **intelligent recommendations**, and **AI mentor chatbot**.

Built with **React 18**, **Flask**, **SQLAlchemy**, **Framer Motion**, and modern glassmorphism design.

---

## ✨ Features at a Glance

### 🔐 **Authentication System**
- User signup with email/password
- Secure JWT token-based login
- Password hashing with bcrypt
- Persistent sessions
- Protected routes

### 🎯 **Career Assessment**
- 10-step interactive questionnaire
- Smooth animations between questions
- Skill sliders (1-5 rating)
- Multi-domain selection
- Real-time form validation

### 🤖 **Intelligent Recommendations**
- 7 detailed career paths
- Advanced weighted scoring algorithm
- Skill gap analysis
- Learning roadmaps (5-7 steps each)
- Beginner & intermediate projects
- Explainable reasoning

### 💬 **AI Mentor Chatbot**
- Context-aware responses
- Sentiment analysis (positive/negative/neutral)
- 10+ intent patterns recognized
- Conversation history
- Quick action suggestions
- Typing indicators

### 🎨 **Premium Design**
- Glassmorphism aesthetic
- Smooth animations (Framer Motion)
- Dark modern theme
- Responsive design (mobile/tablet/desktop)
- Gradient accents
- Professional typography

---

## 🚀 Quick Start (3 Steps)

### Step 1: Run Setup Script

**On Windows:**
```bash
setup.bat
```

**On macOS/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

This automatically:
- ✅ Checks Python 3.11+ and Node.js
- ✅ Creates virtual environment
- ✅ Installs all dependencies
- ✅ Sets up environment variables

### Step 2: Open Two Terminals

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate.bat      # Windows
python app.py
```

Expected: `Running on http://127.0.0.1:5000`

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

Expected: Browser opens to http://localhost:3000

### Step 3: Start Using!

1. Click **"Sign Up"** to create account
2. Fill **10-question assessment**
3. Get **AI-powered recommendations**
4. Chat with **AI mentor**

---

## 📁 Project Structure

```
v2/
├── backend/
│   ├── app.py                       ← Flask API server
│   ├── models.py                    ← Database models
│   ├── recommendation_engine.py    ← AI recommendation logic
│   ├── chatbot.py                  ← AI mentor chatbot
│   ├── requirements.txt
│   ├── .env.example
│   └── venv/                        ← (Created by setup)
│
├── frontend/
│   ├── package.json
│   ├── .env.example
│   ├── public/index.html
│   └── src/
│       ├── App.js                   ← Main router
│       ├── AuthContext.js           ← Auth state
│       ├── pages/
│       │   ├── LoginPage.js
│       │   ├── SignupPage.js
│       │   └── Dashboard.js
│       ├── components/
│       │   ├── Navigation.js
│       │   ├── Questionnaire.js
│       │   ├── RecommendationCard.js
│       │   └── ChatBot.js
│       ├── services/api.js          ← Axios client
│       └── styles/                  ← CSS files
│
├── setup.bat                        ← Windows setup
├── setup.sh                         ← Mac/Linux setup
├── SETUP_GUIDE.md                  ← Full setup docs
└── README.md                        ← This file
```

---

## 🔌 API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/auth/signup` | Create new account |
| POST | `/auth/login` | Login user |
| GET | `/auth/me` | Get current user |
| POST | `/auth/logout` | Logout user |
| POST | `/profile/update` | Update user profile |
| GET | `/profile` | Get user profile |
| POST | `/recommendations` | Get recommendations |
| POST | `/chat` | Send message to chatbot |
| GET | `/chat/history` | Get chat history |
| GET | `/health` | API health check |
| GET | `/career-paths` | All career paths |
| GET | `/domains` | All domains |

---

## 🎯 Career Paths Included

1. **AI Engineer** - Machine learning, deep learning, AI systems
2. **Full Stack Developer** - Web applications, frontend, backend
3. **Cybersecurity Specialist** - Security, penetration testing
4. **Data Analyst** - Data analysis, visualization, insights
5. **UI/UX Designer** - User experience, design systems
6. **Research Engineer** - Research, academic, innovation
7. **Startup Builder** - Entrepreneurship, product development

---

## 🛠️ Technology Stack

### Frontend
- **React 18** - User interface
- **React Router v6** - Navigation
- **Framer Motion** - Smooth animations
- **Axios** - API client
- **CSS3** - Styling & design system

### Backend
- **Flask 3.0** - REST API framework
- **SQLAlchemy** - ORM & database
- **Flask-JWT** - Authentication
- **NLTK** - NLP & sentiment analysis
- **bcrypt** - Password hashing

### Database
- **SQLite** (development)
- **PostgreSQL** (production ready)

---

## 🔐 User Authentication Flow

```
Sign Up → Check Email Exists → Hash Password → Create User
    ↓
Stored in Database with JWT Token
    ↓
Login → Verify Credentials → Generate JWT Token
    ↓
Token Stored in localStorage
    ↓
Protected Routes Check Token → Redirect if Expired
    ↓
Logout → Clear Token → Redirect to Login
```

---

## 📊 Recommendation Algorithm

```
User Assessment Input
    ↓
Skill Scoring (40% weight)
Domain Alignment (25% weight)
Career Goal Fit (15% weight)
Personality Match (15% weight)
Experience Bonus (5% weight)
    ↓
Generate Weighted Score for Each Path
    ↓
Sort & Select Top 3
    ↓
Generate Explanations & Guidance
    ↓
Display to User
```

---

## 🧪 Test the Application

### Create Test Account

**Via UI:**
1. Go to http://localhost:3000/signup
2. Fill form:
   - Name: `John Doe`
   - Email: `john@example.com`
   - Password: `password123`
3. Click "Create Account"

### Complete Assessment

1. Answer 10 questions about skills
2. Select domains of interest
3. Click "Complete"

### View Recommendations

- See 3 career recommendations
- Expand each card for details
- Check learning roadmaps
- See projects and timelines

### Chat with Mentor

- Ask about recommendations
- Get learning guidance
- Request project ideas
- Get encouragement

---

## 🐛 Troubleshooting

### Python/Node Issues

**"Python not found"**
```bash
# Install Python 3.11+
python --version  # Should show 3.11+
```

**"npm not found"**
```bash
# Install Node.js 14+
node --version  # Should show v14+
```

### Port Already in Use

**Port 5000 (Backend):**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID {PID} /F

# macOS/Linux
lsof -ti:5000 | xargs kill -9
```

**Port 3000 (Frontend):**
```bash
npm start -- --port 3001
```

### Connection Errors

**Test backend health:**
```bash
curl http://localhost:5000/api/health
```

Should return: `{"status": "healthy"}`

**Check CORS settings in `.env`:**
```
CORS_ORIGINS=http://localhost:3000
```

### Database Issues

```bash
# Reset database
cd backend
rm career_recommendation.db
python app.py  # Recreates database
```

---

## 📚 Full Documentation

See `SETUP_GUIDE.md` for:
- Detailed setup instructions
- API documentation
- Architecture explanation
- Production deployment
- Advanced configuration

---

## 🎨 Design System

### Colors
- **Primary Gradient**: #667eea → #764ba2
- **Secondary Gradient**: #f093fb → #f5576c
- **Background Dark**: #0a0e27
- **Card Glass**: rgba(30, 41, 59, 0.7)
- **Text Primary**: #f1f5f9
- **Text Secondary**: #cbd5e1

### Typography
- **Headings**: 1.5rem - 2.5rem, weight 700
- **Body**: 1rem, weight 400-500
- **Small**: 0.875rem, muted

### Spacing
- **xs**: 0.25rem
- **sm**: 0.5rem
- **md**: 1rem
- **lg**: 1.5rem
- **xl**: 2rem

### Animations
- **Fast**: 150ms
- **Base**: 300ms
- **Slow**: 500ms
- **Easing**: cubic-bezier(0.4, 0, 0.2, 1)

---

## 📦 Deployment

### Backend (Flask)

**Using Gunicorn:**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

**Heroku:**
```bash
git push heroku main
```

### Frontend (React)

**Build:**
```bash
npm run build
```

**Deploy to Vercel:**
```bash
vercel
```

**Deploy to Netlify:**
Connect GitHub repo in Netlify dashboard

---

## 🤝 Contributing

This is a complete, production-ready system. Feel free to:
- Add more career paths
- Enhance chatbot responses
- Improve design
- Add more features

---

## 📄 License

This project is open source and available under the MIT License.

---

## 🎉 You're Ready!

Everything is set up and ready to go.

**Next steps:**
1. Run `setup.bat` or `setup.sh`
2. Open 2 terminals
3. Start backend and frontend
4. Visit http://localhost:3000
5. Create account and explore!

---

## 📞 Support

If you encounter issues:
1. Check `SETUP_GUIDE.md` Troubleshooting section
2. Verify Python 3.11+ and Node.js 14+
3. Check error messages in terminal
4. Ensure both servers are running

---

**Built with ❤️ | Production Quality | Ready to Deploy**

**Enjoy your AI-powered career guidance system!** 🚀
