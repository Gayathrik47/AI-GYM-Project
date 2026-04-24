from flask import Blueprint, request, jsonify
from datetime import datetime

habit_bp = Blueprint('habit', __name__)

# ── Behavior AI Logic ──────────────────────────────────────────────────────────
# Rule-based predictor: scores user activity signals and returns a skip-risk
# level (low / medium / high) plus a tailored warning message.

RISK_MESSAGES = {
    "low": {
        "emoji": "✅",
        "title": "You're on track!",
        "message": "Great consistency! Keep it up — you're building an unstoppable habit.",
        "tip": "Maintain your current routine and aim to add one extra active minute each day."
    },
    "medium": {
        "emoji": "⚠️",
        "title": "Slight skip risk detected",
        "message": "Your activity pattern shows some gaps. A short workout is always better than none.",
        "tip": "Try a 15-minute express workout today to maintain your streak."
    },
    "high": {
        "emoji": "🚨",
        "title": "High skip risk!",
        "message": "Based on your recent activity, you might be tempted to skip today. Don't break the chain!",
        "tip": "Even 10 minutes of movement counts. Start small — once you begin, you'll likely continue."
    }
}

def predict_skip_risk(data: dict) -> dict:
    """
    Score-based skip risk predictor.

    Input fields (all optional with sensible defaults):
        days_since_last_workout  (int, default 1)
        workouts_this_week       (int, default 3)
        mood                     (str: 'good'|'neutral'|'bad', default 'neutral')
        sleep_hours              (float, default 7)
        stress_level             (int 1-10, default 5)
        hour_of_day              (int 0-23, default current hour)
    """
    # --- Extract inputs with defaults ---
    days_since = int(data.get("days_since_last_workout", 1))
    workouts_week = int(data.get("workouts_this_week", 3))
    mood = str(data.get("mood", "neutral")).lower()
    sleep_hours = float(data.get("sleep_hours", 7))
    stress = int(data.get("stress_level", 5))
    hour = int(data.get("hour_of_day", datetime.now().hour))

    score = 0  # Higher score = higher skip risk

    # Days since last workout
    if days_since >= 3:
        score += 3
    elif days_since == 2:
        score += 1

    # Workouts this week (target = 3–5)
    if workouts_week == 0:
        score += 4
    elif workouts_week == 1:
        score += 2
    elif workouts_week >= 5:
        score -= 1  # overtraining risk handled separately

    # Mood
    if mood == "bad":
        score += 3
    elif mood == "neutral":
        score += 1
    elif mood == "good":
        score -= 1

    # Sleep quality
    if sleep_hours < 5:
        score += 3
    elif sleep_hours < 6.5:
        score += 2
    elif sleep_hours >= 8:
        score -= 1

    # Stress level (1–10)
    if stress >= 8:
        score += 3
    elif stress >= 6:
        score += 1

    # Time of day — late night is risky
    if hour >= 22 or hour < 6:
        score += 2

    # Classify
    if score <= 2:
        risk = "low"
    elif score <= 5:
        risk = "medium"
    else:
        risk = "high"

    result = RISK_MESSAGES[risk].copy()
    result["risk_level"] = risk
    result["score"] = score
    result["inputs_used"] = {
        "days_since_last_workout": days_since,
        "workouts_this_week": workouts_week,
        "mood": mood,
        "sleep_hours": sleep_hours,
        "stress_level": stress,
        "hour_of_day": hour
    }
    return result


# ── Routes ─────────────────────────────────────────────────────────────────────

@habit_bp.route('/habit', methods=['POST'])
def predict_habit():
    """
    POST /api/habit
    Body (JSON, all fields optional):
    {
        "days_since_last_workout": 2,
        "workouts_this_week": 1,
        "mood": "bad",
        "sleep_hours": 5.5,
        "stress_level": 8,
        "hour_of_day": 21
    }
    """
    data = request.get_json() or {}
    result = predict_skip_risk(data)
    return jsonify(result)


@habit_bp.route('/habit/log', methods=['POST'])
def log_activity():
    """
    POST /api/habit/log
    Accepts a completed workout log and returns encouragement.
    Body: { "workout_type": "strength", "duration_minutes": 45, "calories_burned": 320 }
    """
    data = request.get_json() or {}
    workout_type = data.get("workout_type", "workout")
    duration = data.get("duration_minutes", 0)
    calories = data.get("calories_burned", 0)

    if duration <= 0:
        return jsonify({"error": "duration_minutes must be > 0"}), 400

    if duration < 20:
        badge = "🥉 Quick Mover"
    elif duration < 45:
        badge = "🥈 Consistent Athlete"
    else:
        badge = "🥇 Elite Performer"

    return jsonify({
        "status": "logged",
        "badge": badge,
        "message": f"Amazing! You completed a {duration}-minute {workout_type} session and burned ~{calories} kcal. {badge}",
        "streak_tip": "Log tomorrow's workout to build your streak!"
    })
