# 🚀 Career Path - Complete Setup Guide

Premium AI-powered career recommendation system with full authentication, multi-step questionnaire, recommendations, and mentor chatbot.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Backend Setup](#backend-setup)
- [Frontend Setup](#frontend-setup)
- [Running the Application](#running-the-application)
- [Features](#features)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)

---

## ✅ Prerequisites

### Required
- **Python 3.11+** (or 3.12)
- **Node.js 14+** and npm
- **Git** (optional)

### Verify Installation
```bash
python --version    # Should show Python 3.11+
node --version      # Should show v14+
npm --version       # Should show 8+
```

---

## 📁 Project Structure

```
career_recommendation/v2/
├── backend/
│   ├── .env.example             # Environment variables template
│   ├── models.py               # Database models (User, Profile, etc.)
│   ├── recommendation_engine.py # AI recommendation logic
│   ├── chatbot.py              # Mentor chatbot logic
│   ├── app.py                  # Flask API server
│   └── requirements.txt         # Python dependencies
│
├── frontend/
│   ├── .env.example            # Environment variables template
│   ├── package.json            # Node dependencies
│   ├── public/
│   │   └── index.html          # HTML entry point
│   └── src/
│       ├── App.js              # Main application component
│       ├── index.js            # React entry point
│       ├── contexts/
│       │   └── AuthContext.js  # Authentication state management
│       ├── pages/
│       │   ├── LoginPage.js    # Login page
│       │   ├── SignupPage.js   # Signup page
│       │   └── Dashboard.js    # Main dashboard
│       ├── components/
│       │   ├── Navigation.js   # Top navigation bar
│       │   ├── Questionnaire.js # Multi-step assessment
│       │   ├── RecommendationsView.js # Recommendations display
│       │   ├── RecommendationCard.js  # Individual card
│       │   └── ChatBot.js      # Mentor chatbot
│       ├── services/
│       │   └── api.js          # API client with axios
│       └── styles/
│           ├── design-system.css # Global design system
│           ├── auth.css        # Auth pages styles
│           ├── navigation.css  # Navigation styles
│           ├── questionnaire.css
│           ├── recommendations.css
│           ├── chatbot.css     # Chat interface styles
│           └── dashboard.css
└── README.md                    # This file
```

---

## 🏗️ Backend Setup

### Step 1: Navigate to Backend

```bash
cd career_recommendation/v2/backend
```

### Step 2: Create Virtual Environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate.bat
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip setuptools
pip install -r requirements.txt
```

### Step 4: Setup Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your settings (optional for development)
```

### Step 5: Initialize Database

```bash
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

### Step 6: Run Backend Server

```bash
python app.py
```

**Expected Output:**
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

✅ **Backend is running on http://localhost:5000**

---

## 🎨 Frontend Setup

### Step 1: Navigate to Frontend

```bash
cd ../frontend
```

### Step 2: Install Dependencies

```bash
npm install
```

This will install all packages including React, Framer Motion, Axios, etc.

### Step 3: Setup Environment Variables

```bash
# Copy the example file
cp .env.example .env

# The default values should work for development
```

### Step 4: Start React Development Server

```bash
npm start
```

**Expected Output:**
```
Compiled successfully!

You can now view career-recommendation-app in the browser.

  Local:            http://localhost:3000
```

✅ **Frontend is running on http://localhost:3000**

Browser will automatically open. If not, navigate to http://localhost:3000

---

## 🚀 Running the Application

### Quick Start (All in One)

You need **2 terminal windows** open simultaneously:

**Terminal 1 - Backend:**
```bash
cd career_recommendation/v2/backend
source venv/bin/activate  # or: venv\Scripts\activate.bat (Windows)
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd career_recommendation/v2/frontend
npm start
```

Then open http://localhost:3000 in your browser.

---

## ✨ Features

### 1. **Authentication System**
- ✅ User signup with email/password
- ✅ Secure login with JWT tokens
- ✅ Password hashing with bcrypt
- ✅ Persistent sessions
- ✅ Protected routes

### 2. **Career Assessment**
- ✅ 10-step interactive questionnaire
- ✅ Animated transitions between questions
- ✅ Real-time skill sliders (1-5 rating)
- ✅ Multi-domain selection
- ✅ Career goals and preferences
- ✅ Form validation

### 3. **Recommendation Engine**
- ✅ 7 career paths with detailed info
- ✅ Advanced weighted scoring algorithm
- ✅ Skill gap analysis
- ✅ Learning roadmaps (5-7 steps per path)
- ✅ Beginner and intermediate projects
- ✅ Explainable reasoning

### 4. **Professional Design**
- ✅ Glassmorphism aesthetic
- ✅ Smooth animations (Framer Motion)
- ✅ Responsive design (mobile/tablet/desktop)
- ✅ Dark modern theme
- ✅ Gradient accents
- ✅ Premium UI/UX

### 5. **AI Mentor Chatbot**
- ✅ Context-aware responses
- ✅ Sentiment analysis
- ✅ 10+ intent patterns
- ✅ Conversation history
- ✅ Quick action prompts
- ✅ Typing indicators

### 6. **Data Management**
- ✅ SQLAlchemy ORM
- ✅ User profiles with versioning
- ✅ Assessment history tracking
- ✅ Conversation logging
- ✅ Recommendation archiving

---

## 📚 API Documentation

### Base URL
```
http://localhost:5000/api
```

### Authentication Endpoints

**Signup**
```
POST /auth/signup
Body: { email, password, name }
Response: { success, access_token, user }
```

**Login**
```
POST /auth/login
Body: { email, password }
Response: { success, access_token, user }
```

**Get Current User**
```
GET /auth/me
Header: Authorization: Bearer {token}
Response: { success, user, profile }
```

### Profile Endpoints

**Update Profile**
```
POST /profile/update
Body: { coding_proficiency, math_comfort, creativity, ... }
Response: { success, profile }
```

**Get Profile**
```
GET /profile
Response: { success, profile }
```

### Recommendation Endpoints

**Get Recommendations**
```
POST /recommendations
Body: { questionnaire data }
Response: { success, recommendations: [...] }
```

**Fetch Recommendations**
```
GET /recommendations
Response: { success, recommendations: [...] }
```

### Chatbot Endpoints

**Send Message**
```
POST /chat
Body: { message }
Response: { success, response, sentiment, intent }
```

**Get Chat History**
```
GET /chat/history?limit=50
Response: { success, messages: [...] }
```

### Info Endpoints

**Health Check**
```
GET /health
Response: { status, message }
```

**Career Paths**
```
GET /career-paths
Response: { success, career_paths: [...] }
```

**Domains**
```
GET /domains
Response: { success, domains: [...] }
```

---

## 🧪 Testing the Application

### Test User Account (After Signup)

1. Open http://localhost:3000
2. Click "Sign Up" or navigate to `/signup`
3. Create an account:
   - Name: `John Doe`
   - Email: `john@example.com`
   - Password: `password123`

### Test Login

1. Go to http://localhost:3000/login
2. Use your credentials
3. Or try demo: Email: `demo@example.com`, Password: `demo12345`

### Complete the Assessment

1. Fill the 10-question questionnaire
2. Answer honestly about your skills
3. Get personalized recommendations
4. Explore each recommendation by expanding cards
5. Chat with the AI mentor

---

## 🔧 Troubleshooting

### "Port 5000 already in use"

Find and kill the process:
**Windows:**
```bash
netstat -ano | findstr :5000
taskkill /PID {PID} /F
```

**macOS/Linux:**
```bash
lsof -ti:5000 | xargs kill -9
```

### "Cannot connect to backend"

Check if Flask is running:
```bash
curl http://localhost:5000/api/health
```

Should return:
```json
{ "status": "healthy" }
```

### "ModuleNotFoundError" in Python

Ensure virtual environment is activated:
```bash
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate.bat  # Windows
```

Then reinstall:
```bash
pip install -r requirements.txt
```

### "npm ERR! Missing dependencies"

```bash
rm -rf node_modules package-lock.json
npm install
```

### Port 3000 in use

```bash
npm start -- --port 3001
```

Or find process:
**Windows:**
```bash
netstat -ano | findstr :3000
taskkill /PID {PID} /F
```

---

## 🎓 Understanding the Architecture

### Frontend Flow
```
Login/Signup → AuthContext → Protected Routes → Dashboard
                                ↓
                    Questionnaire → Recommendations → ChatBot
```

### Backend Flow
```
Request → Auth Middleware → Route Handler → Domain Logic → Database
                              ↓
                    Recommendation Engine
                    Chatbot
                    Sentiment Analysis
```

### Data Flow
```
User Input → Questionnaire → API → Backend Processing → Database
                                    ↓
                          Recommendation Engine
                          Chatbot Logic
                                    ↓
                              Frontend Display
```

---

## 📝 Environment Variables

### Backend (.env)
```
FLASK_ENV=development
FLASK_DEBUG=1
JWT_SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///career_recommendation.db
CORS_ORIGINS=http://localhost:3000
```

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:5000/api
```

---

## 🚀 Production Deployment

### Backend (Flask)

**Using Gunicorn:**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

**Update settings:**
- Set `FLASK_ENV=production`
- Change `JWT_SECRET_KEY` to strong random key
- Update `DATABASE_URL` to PostgreSQL
- Update `CORS_ORIGINS` to your domain

### Frontend (React)

**Build:**
```bash
npm run build
```

Produces optimized `build/` directory.

**Deploy:**
- Vercel: `vercel` command
- Netlify: Connect GitHub repo
- AWS S3 + CloudFront: Upload build files
- Docker: Create Docker image

---

## 📞 Support & Help

### Common Issues

1. **Connection refused**: Ensure both servers are running
2. **CORS error**: Check CORS_ORIGINS in backend .env
3. **Authentication failed**: Clear localStorage and cookies
4. **Build errors**: Delete `node_modules` and reinstall

### Getting Help

1. Check terminal error messages
2. Verify Python/Node versions
3. Read Flask/React documentation
4. Check API endpoints with curl/Postman

---

## 🎉 You're All Set!

Your premium career recommendation system is ready to use!

**Next Steps:**
1. Open http://localhost:3000
2. Create account
3. Complete assessment
4. View recommendations
5. Chat with mentor

**Enjoy your career guidance journey!** 🚀

---

*Built with ❤️ | React + Flask | AI-Powered Career Guidance*
