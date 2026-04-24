from flask import Flask
from flask_cors import CORS
from routes.chat import chat_bp
from routes.workout import workout_bp
from routes.diet import diet_bp
from routes.habit import habit_bp
from routes.analytics import analytics_bp
import os

# CREATE APP FIRST
app = Flask(__name__)
CORS(app)

#  Register routes
app.register_blueprint(chat_bp,      url_prefix='/api')
app.register_blueprint(workout_bp,   url_prefix='/api')
app.register_blueprint(diet_bp,      url_prefix='/api')
app.register_blueprint(habit_bp,     url_prefix='/api')
app.register_blueprint(analytics_bp, url_prefix='/api')

#  Home route
@app.route('/')
def index():
    return {
        "message": "FitAI API v2.0 is running!",
        "version": "2.0"
    }

#  RUN LAST (VERY IMPORTANT)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)