from flask import Blueprint, jsonify
import random

analytics_bp = Blueprint('analytics', __name__)

# ── Static/Dummy Analytics Data ───────────────────────────────────────────────
# In a real app these would come from a database.
# For the college project, we use realistic static + slightly randomised data.

BASE_STATS = {
    "total_workouts": 142,
    "total_users": 38,
    "calories_tracked": 184320,
    "active_today": 12,
    "avg_session_minutes": 47,
    "streak_record": 21,
}

WEEKLY_WORKOUTS = [
    {"day": "Mon", "count": 18},
    {"day": "Tue", "count": 22},
    {"day": "Wed", "count": 15},
    {"day": "Thu", "count": 27},
    {"day": "Fri", "count": 31},
    {"day": "Sat", "count": 20},
    {"day": "Sun", "count": 9},
]

WORKOUT_DISTRIBUTION = [
    {"type": "Strength", "percentage": 42, "count": 60},
    {"type": "Cardio",   "percentage": 28, "count": 40},
    {"type": "HIIT",     "percentage": 18, "count": 25},
    {"type": "Yoga",     "percentage": 8,  "count": 11},
    {"type": "Other",    "percentage": 4,  "count": 6},
]

CALORIE_TREND = [
    {"week": "Wk 1", "consumed": 14200, "burned": 3100},
    {"week": "Wk 2", "consumed": 13800, "burned": 3400},
    {"week": "Wk 3", "consumed": 14500, "burned": 3250},
    {"week": "Wk 4", "consumed": 13600, "burned": 3700},
]

TOP_USERS = [
    {"name": "Alex M.",   "workouts": 24, "streak": 18, "level": "Advanced"},
    {"name": "Priya S.",  "workouts": 21, "streak": 14, "level": "Intermediate"},
    {"name": "Jordan K.", "workouts": 19, "streak": 21, "level": "Advanced"},
    {"name": "Sam R.",    "workouts": 17, "streak": 9,  "level": "Beginner"},
    {"name": "Chris T.",  "workouts": 15, "streak": 12, "level": "Intermediate"},
]

RECENT_ACTIVITY = [
    {"user": "Alex M.",   "action": "Completed Advanced Chest Day",     "time": "2 min ago",  "calories": 410},
    {"user": "Priya S.",  "action": "Logged Muscle Gain Meal Plan",      "time": "14 min ago", "calories": 650},
    {"user": "Jordan K.", "action": "Completed HIIT Core Session",       "time": "31 min ago", "calories": 280},
    {"user": "Sam R.",    "action": "Asked AI: best beginner workout",    "time": "45 min ago", "calories": 0},
    {"user": "Chris T.",  "action": "Completed Intermediate Push Day",   "time": "1 hr ago",   "calories": 370},
    {"user": "Maya L.",   "action": "Logged Weight Loss Diet Plan",      "time": "2 hrs ago",  "calories": 490},
]


@analytics_bp.route('/analytics/summary', methods=['GET'])
def get_summary():
    """GET /api/analytics/summary — top-level KPI stats."""
    return jsonify(BASE_STATS)


@analytics_bp.route('/analytics/weekly', methods=['GET'])
def get_weekly():
    """GET /api/analytics/weekly — workouts per day of week."""
    return jsonify(WEEKLY_WORKOUTS)


@analytics_bp.route('/analytics/distribution', methods=['GET'])
def get_distribution():
    """GET /api/analytics/distribution — workout type breakdown."""
    return jsonify(WORKOUT_DISTRIBUTION)


@analytics_bp.route('/analytics/calories', methods=['GET'])
def get_calories():
    """GET /api/analytics/calories — 4-week calorie trend."""
    return jsonify(CALORIE_TREND)


@analytics_bp.route('/analytics/users', methods=['GET'])
def get_top_users():
    """GET /api/analytics/users — leaderboard."""
    return jsonify(TOP_USERS)


@analytics_bp.route('/analytics/activity', methods=['GET'])
def get_activity():
    """GET /api/analytics/activity — recent activity feed."""
    return jsonify(RECENT_ACTIVITY)


@analytics_bp.route('/analytics/all', methods=['GET'])
def get_all():
    """GET /api/analytics/all — everything in one call (used by dashboard)."""
    return jsonify({
        "summary": BASE_STATS,
        "weekly_workouts": WEEKLY_WORKOUTS,
        "workout_distribution": WORKOUT_DISTRIBUTION,
        "calorie_trend": CALORIE_TREND,
        "top_users": TOP_USERS,
        "recent_activity": RECENT_ACTIVITY,
    })
