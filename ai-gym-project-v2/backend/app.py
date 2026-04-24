from flask import Flask
from flask_cors import CORS
from routes.chat import chat_bp
from routes.workout import workout_bp
from routes.diet import diet_bp
from routes.habit import habit_bp          # NEW: Behavior AI
from routes.analytics import analytics_bp  # NEW: Analytics

app = Flask(__name__)
CORS(app)

# ── Register Blueprints ────────────────────────────────────────────────────────
app.register_blueprint(chat_bp,      url_prefix='/api')
app.register_blueprint(workout_bp,   url_prefix='/api')
app.register_blueprint(diet_bp,      url_prefix='/api')
app.register_blueprint(habit_bp,     url_prefix='/api')      # NEW
app.register_blueprint(analytics_bp, url_prefix='/api')      # NEW

@app.route('/')
def index():
    return {
        "message": "FitAI API v2.0 is running!",
        "version": "2.0",
        "new_endpoints": [
            "POST /api/habit",
            "POST /api/habit/log",
            "GET  /api/analytics/all",
        ]
    }

if __name__ == '__main__':
    app.run(debug=True, port=5000)
