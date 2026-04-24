# ⚡ FitAI v2.0 — AI Gym & Fitness Assistant
### Upgraded College Major Project | React + Flask Full-Stack Application

---

## 🆕 What's New in v2.0

| Module | Status | Description |
|--------|--------|-------------|
| 🧠 Behavior AI | **NEW** | Skip-risk predictor using mood, sleep, stress, activity signals |
| 📊 Admin Dashboard | **NEW** | KPI cards, bar charts, donut chart, leaderboard, activity feed |
| 📈 Analytics API | **NEW** | 6 new endpoints serving dashboard data |
| 💬 Smarter Chatbot | **UPGRADED** | 25+ topic categories, context-aware responses |
| 🗂️ Tab Navigation | **UPGRADED** | Now 5 tabs: AI Coach, Workouts, Nutrition, Behavior AI, Dashboard |

---

## ✨ Full Feature List

### 🤖 AI Chat Coach
- Upgraded rule-based NLP with 25+ fitness topic categories
- Topics: muscle gain, fat loss, cardio, supplements, sleep, recovery, deload, injury, motivation, BMI, plateau-busting, hydration, and more
- Quick suggestion chips for common questions
- Typing indicator and timestamped messages

### 💪 Workout Plans
- Beginner (4 weeks, 3 days/week) — full-body foundation
- Intermediate (6 weeks, 4 days/week) — Push/Pull/Legs split
- Advanced (8 weeks, 5 days/week) — periodized high-volume
- Each plan includes sets, reps, rest periods, and pro tips

### 🥗 Nutrition Plans
- Muscle Gain — ~3280 kcal, 238g protein, 7-meal plan
- Weight Loss — ~1750 kcal, 150g protein, high-satiety foods
- Maintenance — ~1900 kcal, balanced macros
- Full meal-by-meal breakdown with macro badges

### 🧠 Behavior AI — Habit Tracker
- **Skip Risk Predictor**: scores 6 signals (days since workout, workouts/week, mood, sleep, stress, time of day) to predict skip risk (Low / Medium / High)
- Visual risk score bar with color coding
- Personalized warning messages and action tips
- **Workout Logger**: log completed sessions with type, duration, calories — earn achievement badges (Quick Mover / Consistent Athlete / Elite Performer)

### 📊 Admin Dashboard
- **KPI Cards**: Total Workouts, Users, Calories Tracked, Active Today, Avg Session, Streak Record
- **Weekly Bar Chart**: Workout count per day (pure CSS, no library)
- **Donut Chart**: Workout type distribution (SVG-based)
- **Calorie Trend**: 4-week consumed vs. burned dual bar chart
- **Leaderboard**: Top 5 users with streak and level badges
- **Activity Feed**: Live-style recent user actions

---

## 🗂️ Project Structure

```
ai-gym-project/
├── backend/
│   ├── app.py                    ← UPDATED: registers 5 blueprints
│   ├── requirements.txt
│   └── routes/
│       ├── __init__.py
│       ├── chat.py               ← UPGRADED: 25+ topic NLP engine
│       ├── workout.py            ← unchanged
│       ├── diet.py               ← unchanged
│       ├── habit.py              ← NEW: Behavior AI + workout logger
│       └── analytics.py          ← NEW: 6 analytics endpoints
├── frontend/
│   ├── package.json
│   ├── public/index.html
│   └── src/
│       ├── App.js                ← UPDATED: 5-tab navigation
│       ├── App.css               ← UPDATED: +200 lines new styles
│       ├── index.js
│       ├── index.css
│       └── components/
│           ├── Chat.js           ← unchanged (uses upgraded API)
│           ├── Workout.js        ← unchanged
│           ├── Diet.js           ← unchanged
│           ├── HabitTracker.js   ← NEW: Behavior AI UI
│           └── Dashboard.js      ← NEW: Admin dashboard + charts
└── README.md                     ← this file
```

---

## 🌐 API Reference

### Existing Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/chat` | AI chat — upgraded NLP engine |
| GET | `/api/workout/<level>` | Workout plan: `beginner` / `intermediate` / `advanced` |
| GET | `/api/diet/<goal>` | Diet plan: `muscle_gain` / `weight_loss` / `maintenance` |
| GET | `/api/foods` | Food nutrition database |

### New v2.0 Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/habit` | Predict workout skip risk |
| POST | `/api/habit/log` | Log a completed workout, get badge |
| GET | `/api/analytics/all` | All dashboard data in one call |
| GET | `/api/analytics/summary` | KPI summary stats |
| GET | `/api/analytics/weekly` | Workouts per day of week |
| GET | `/api/analytics/distribution` | Workout type breakdown |
| GET | `/api/analytics/calories` | 4-week calorie trend |
| GET | `/api/analytics/users` | Leaderboard |
| GET | `/api/analytics/activity` | Recent activity feed |

### Habit API Example
```bash
# Predict skip risk
curl -X POST http://localhost:5000/api/habit \
  -H "Content-Type: application/json" \
  -d '{
    "days_since_last_workout": 3,
    "workouts_this_week": 1,
    "mood": "bad",
    "sleep_hours": 5.5,
    "stress_level": 8,
    "hour_of_day": 21
  }'

# Response:
{
  "emoji": "🚨",
  "title": "High skip risk!",
  "risk_level": "high",
  "score": 11,
  "message": "Based on your recent activity, you might be tempted to skip today. Don't break the chain!",
  "tip": "Even 10 minutes of movement counts. Start small..."
}
```

---

## 🚀 Setup & Running

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm

### 1️⃣ Backend
```bash
cd ai-gym-project/backend

# Create + activate virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Start server
python app.py
# ✅ http://localhost:5000
```

### 2️⃣ Frontend
```bash
cd ai-gym-project/frontend
npm install
npm start
# ✅ http://localhost:3000
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, Functional Components, Hooks |
| Charts | Pure CSS + SVG (zero chart libraries) |
| Backend | Python Flask 3.0, Blueprints |
| CORS | flask-cors |
| AI Engine | Rule-based NLP (no external API) |
| Styling | Custom CSS, dark theme, responsive |

---

## 🔮 Extending to Real AI

Replace `get_ai_response()` in `routes/chat.py`:
```python
import anthropic
client = anthropic.Anthropic(api_key="YOUR_KEY")

def get_ai_response(message):
    resp = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=400,
        system="You are a professional fitness coach and nutritionist.",
        messages=[{"role": "user", "content": message}]
    )
    return resp.content[0].text
```

---

*FitAI v2.0 — Built with ❤️ as a College Major Project*
