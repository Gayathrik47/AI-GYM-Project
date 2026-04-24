from flask import Blueprint, jsonify

workout_bp = Blueprint('workout', __name__)

WORKOUT_PLANS = {
    "beginner": {
        "level": "Beginner",
        "duration": "4 Weeks",
        "frequency": "3 days/week",
        "description": "Perfect for those just starting their fitness journey. Focuses on building a solid foundation of movement patterns and strength.",
        "schedule": [
            {
                "day": "Day 1 – Full Body A",
                "exercises": [
                    {"name": "Bodyweight Squats", "sets": 3, "reps": "12–15", "rest": "60s"},
                    {"name": "Push-Ups (knee or full)", "sets": 3, "reps": "8–12", "rest": "60s"},
                    {"name": "Dumbbell Bent-Over Row", "sets": 3, "reps": "10–12", "rest": "60s"},
                    {"name": "Plank Hold", "sets": 3, "reps": "20–30s", "rest": "45s"},
                    {"name": "Walking Lunges", "sets": 2, "reps": "10 each leg", "rest": "60s"},
                ]
            },
            {
                "day": "Day 2 – Rest / Light Cardio",
                "exercises": [
                    {"name": "30-min Walk or Light Jog", "sets": 1, "reps": "30 min", "rest": "N/A"},
                    {"name": "Stretching / Yoga", "sets": 1, "reps": "15 min", "rest": "N/A"},
                ]
            },
            {
                "day": "Day 3 – Full Body B",
                "exercises": [
                    {"name": "Goblet Squat", "sets": 3, "reps": "12", "rest": "60s"},
                    {"name": "Dumbbell Shoulder Press", "sets": 3, "reps": "10–12", "rest": "60s"},
                    {"name": "Lat Pulldown / Band Pull", "sets": 3, "reps": "12", "rest": "60s"},
                    {"name": "Glute Bridge", "sets": 3, "reps": "15", "rest": "45s"},
                    {"name": "Dead Bug (Core)", "sets": 3, "reps": "8 each side", "rest": "45s"},
                ]
            },
        ],
        "tips": [
            "Focus on proper form before increasing weight",
            "Stay hydrated — drink 2–3 liters of water daily",
            "Get 7–9 hours of sleep for optimal recovery",
            "Don't skip warm-up (5 min light cardio + dynamic stretches)"
        ]
    },
    "intermediate": {
        "level": "Intermediate",
        "duration": "6 Weeks",
        "frequency": "4 days/week",
        "description": "For those with 3–12 months of training experience. Introduces push/pull/legs split for greater volume and muscle development.",
        "schedule": [
            {
                "day": "Day 1 – Push (Chest, Shoulders, Triceps)",
                "exercises": [
                    {"name": "Barbell Bench Press", "sets": 4, "reps": "8–10", "rest": "90s"},
                    {"name": "Incline Dumbbell Press", "sets": 3, "reps": "10–12", "rest": "75s"},
                    {"name": "Overhead Shoulder Press", "sets": 3, "reps": "10", "rest": "75s"},
                    {"name": "Lateral Raises", "sets": 3, "reps": "15", "rest": "60s"},
                    {"name": "Tricep Dips / Pushdowns", "sets": 3, "reps": "12", "rest": "60s"},
                ]
            },
            {
                "day": "Day 2 – Pull (Back, Biceps)",
                "exercises": [
                    {"name": "Pull-Ups / Assisted Pull-Ups", "sets": 4, "reps": "6–8", "rest": "90s"},
                    {"name": "Barbell Row", "sets": 4, "reps": "8–10", "rest": "90s"},
                    {"name": "Seated Cable Row", "sets": 3, "reps": "12", "rest": "75s"},
                    {"name": "Face Pulls", "sets": 3, "reps": "15", "rest": "60s"},
                    {"name": "Dumbbell Bicep Curls", "sets": 3, "reps": "12", "rest": "60s"},
                ]
            },
            {
                "day": "Day 3 – Legs",
                "exercises": [
                    {"name": "Barbell Back Squat", "sets": 4, "reps": "8–10", "rest": "2 min"},
                    {"name": "Romanian Deadlift", "sets": 3, "reps": "10", "rest": "90s"},
                    {"name": "Leg Press", "sets": 3, "reps": "12–15", "rest": "90s"},
                    {"name": "Leg Curl", "sets": 3, "reps": "12", "rest": "60s"},
                    {"name": "Standing Calf Raises", "sets": 4, "reps": "15–20", "rest": "60s"},
                ]
            },
            {
                "day": "Day 4 – HIIT / Core",
                "exercises": [
                    {"name": "Burpees", "sets": 4, "reps": "30s on / 30s off", "rest": "30s"},
                    {"name": "Mountain Climbers", "sets": 4, "reps": "30s", "rest": "30s"},
                    {"name": "Ab Wheel Rollout", "sets": 3, "reps": "10", "rest": "60s"},
                    {"name": "Russian Twists", "sets": 3, "reps": "20 total", "rest": "45s"},
                    {"name": "Hanging Leg Raises", "sets": 3, "reps": "12", "rest": "60s"},
                ]
            },
        ],
        "tips": [
            "Track your lifts to ensure progressive overload week-to-week",
            "Increase weight by 2.5–5% when you complete all sets with good form",
            "Eat in a slight calorie surplus to maximize muscle gain",
            "Consider creatine supplementation (3–5g/day) for strength gains"
        ]
    },
    "advanced": {
        "level": "Advanced",
        "duration": "8 Weeks",
        "frequency": "5 days/week",
        "description": "Designed for experienced lifters (1+ years). Uses advanced periodization with high volume and intensity techniques.",
        "schedule": [
            {
                "day": "Day 1 – Chest & Triceps (Heavy)",
                "exercises": [
                    {"name": "Barbell Bench Press", "sets": 5, "reps": "5 (heavy)", "rest": "2–3 min"},
                    {"name": "Incline DB Press", "sets": 4, "reps": "8–10", "rest": "90s"},
                    {"name": "Cable Flyes", "sets": 3, "reps": "12–15", "rest": "60s"},
                    {"name": "Close-Grip Bench Press", "sets": 4, "reps": "8", "rest": "90s"},
                    {"name": "Overhead Tricep Extension", "sets": 3, "reps": "10–12", "rest": "60s"},
                ]
            },
            {
                "day": "Day 2 – Back & Biceps (Heavy)",
                "exercises": [
                    {"name": "Deadlift", "sets": 5, "reps": "3–5 (heavy)", "rest": "3 min"},
                    {"name": "Weighted Pull-Ups", "sets": 4, "reps": "6–8", "rest": "2 min"},
                    {"name": "T-Bar Row", "sets": 4, "reps": "8–10", "rest": "90s"},
                    {"name": "Preacher Curl", "sets": 3, "reps": "10", "rest": "60s"},
                    {"name": "Hammer Curls", "sets": 3, "reps": "12", "rest": "60s"},
                ]
            },
            {
                "day": "Day 3 – Legs (Quad Dominant)",
                "exercises": [
                    {"name": "Barbell Back Squat", "sets": 5, "reps": "5 (heavy)", "rest": "3 min"},
                    {"name": "Front Squat", "sets": 3, "reps": "6–8", "rest": "2 min"},
                    {"name": "Leg Press (wide stance)", "sets": 4, "reps": "12", "rest": "90s"},
                    {"name": "Sissy Squats / Leg Extension", "sets": 3, "reps": "15", "rest": "60s"},
                    {"name": "Seated Calf Raises", "sets": 5, "reps": "15", "rest": "60s"},
                ]
            },
            {
                "day": "Day 4 – Shoulders & Arms",
                "exercises": [
                    {"name": "Seated DB Shoulder Press", "sets": 4, "reps": "8–10", "rest": "90s"},
                    {"name": "Arnold Press", "sets": 3, "reps": "10–12", "rest": "75s"},
                    {"name": "Lateral Raises (Drop set)", "sets": 4, "reps": "12+12+12", "rest": "60s"},
                    {"name": "EZ-Bar Curl", "sets": 4, "reps": "8–10", "rest": "75s"},
                    {"name": "Skull Crushers", "sets": 4, "reps": "8–10", "rest": "75s"},
                ]
            },
            {
                "day": "Day 5 – Legs (Posterior Chain) + Core",
                "exercises": [
                    {"name": "Romanian Deadlift", "sets": 4, "reps": "8–10", "rest": "90s"},
                    {"name": "Bulgarian Split Squat", "sets": 4, "reps": "10 each", "rest": "90s"},
                    {"name": "Lying Leg Curl", "sets": 4, "reps": "12", "rest": "75s"},
                    {"name": "Glute-Ham Raise", "sets": 3, "reps": "8–10", "rest": "60s"},
                    {"name": "Ab Circuit (Plank/V-ups/Twists)", "sets": 3, "reps": "15 each", "rest": "60s"},
                ]
            },
        ],
        "tips": [
            "Use RPE (Rate of Perceived Exertion) scale for autoregulation",
            "Implement deload weeks every 6–8 weeks to prevent overtraining",
            "Prioritize sleep quality — use a consistent sleep schedule",
            "Consider working with a coach for advanced programming"
        ]
    }
}


@workout_bp.route('/workout/<level>', methods=['GET'])
def get_workout(level):
    """Return workout plan for given level."""
    level = level.lower()
    if level not in WORKOUT_PLANS:
        return jsonify({"error": f"Level '{level}' not found. Choose: beginner, intermediate, advanced"}), 404
    return jsonify(WORKOUT_PLANS[level])


@workout_bp.route('/workout', methods=['GET'])
def get_all_workouts():
    """Return summary of all workout levels."""
    summary = {k: {"level": v["level"], "duration": v["duration"], "frequency": v["frequency"], "description": v["description"]}
               for k, v in WORKOUT_PLANS.items()}
    return jsonify(summary)
