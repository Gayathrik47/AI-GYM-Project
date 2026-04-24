from flask import Blueprint, jsonify, request

diet_bp = Blueprint('diet', __name__)

DIET_PLANS = {
    "muscle_gain": {
        "goal": "Muscle Gain",
        "calories": "Surplus: +300–500 kcal above TDEE",
        "macros": {"protein": "2.0–2.2g per kg", "carbs": "4–6g per kg", "fats": "0.8–1.0g per kg"},
        "description": "Designed to maximize muscle protein synthesis while minimizing fat gain.",
        "meal_plan": [
            {
                "meal": "Breakfast (7:00 AM)",
                "foods": ["4 whole eggs scrambled", "2 slices whole grain toast", "1 cup oatmeal with banana", "1 glass milk"],
                "approx_calories": 650,
                "protein": "35g"
            },
            {
                "meal": "Mid-Morning Snack (10:00 AM)",
                "foods": ["Greek yogurt (200g)", "Mixed berries", "1 tbsp honey", "10 almonds"],
                "approx_calories": 280,
                "protein": "18g"
            },
            {
                "meal": "Lunch (1:00 PM)",
                "foods": ["200g grilled chicken breast", "1.5 cups brown rice", "1 cup mixed vegetables", "1 tbsp olive oil"],
                "approx_calories": 700,
                "protein": "50g"
            },
            {
                "meal": "Pre-Workout (4:00 PM)",
                "foods": ["1 banana", "1 scoop whey protein shake", "1 tbsp peanut butter"],
                "approx_calories": 350,
                "protein": "30g"
            },
            {
                "meal": "Post-Workout (6:30 PM)",
                "foods": ["1 scoop whey protein + milk", "1 cup white rice or sweet potato"],
                "approx_calories": 450,
                "protein": "35g"
            },
            {
                "meal": "Dinner (8:00 PM)",
                "foods": ["200g salmon or lean beef", "Large salad with olive oil dressing", "1 cup quinoa", "Steamed broccoli"],
                "approx_calories": 650,
                "protein": "45g"
            },
            {
                "meal": "Before Bed (10:00 PM)",
                "foods": ["Cottage cheese (150g)", "Casein protein shake (optional)"],
                "approx_calories": 200,
                "protein": "25g"
            },
        ],
        "total_approx": {"calories": 3280, "protein": "238g"},
        "tips": [
            "Eat every 3–4 hours to maintain positive nitrogen balance",
            "Don't skip breakfast — it jumpstarts muscle protein synthesis",
            "Carb-load slightly on training days, reduce on rest days",
            "Stay consistent — muscle gain takes months, not weeks"
        ]
    },
    "weight_loss": {
        "goal": "Weight Loss (Fat Loss)",
        "calories": "Deficit: -300–500 kcal below TDEE",
        "macros": {"protein": "2.2–2.5g per kg", "carbs": "2–3g per kg", "fats": "0.8g per kg"},
        "description": "High-protein, moderate-carb diet to preserve muscle while losing body fat.",
        "meal_plan": [
            {
                "meal": "Breakfast (7:30 AM)",
                "foods": ["3 egg whites + 1 whole egg", "1 slice whole grain toast", "1 cup black coffee or green tea", "Half an avocado"],
                "approx_calories": 350,
                "protein": "25g"
            },
            {
                "meal": "Mid-Morning Snack (10:30 AM)",
                "foods": ["Apple or pear", "15g almonds", "Green tea"],
                "approx_calories": 180,
                "protein": "5g"
            },
            {
                "meal": "Lunch (1:00 PM)",
                "foods": ["150g grilled chicken or tuna", "Large green salad (no croutons)", "2 tbsp balsamic dressing", "1 small sweet potato"],
                "approx_calories": 450,
                "protein": "42g"
            },
            {
                "meal": "Afternoon Snack (3:30 PM)",
                "foods": ["Greek yogurt (150g, low-fat)", "Cucumber slices"],
                "approx_calories": 150,
                "protein": "15g"
            },
            {
                "meal": "Pre/Post Workout (5:30 PM)",
                "foods": ["Whey protein shake (water)", "Banana (optional, pre-workout)"],
                "approx_calories": 200,
                "protein": "25g"
            },
            {
                "meal": "Dinner (7:30 PM)",
                "foods": ["180g white fish (tilapia/cod)", "2 cups roasted vegetables", "1/2 cup brown rice or cauliflower rice", "Lemon-herb dressing"],
                "approx_calories": 420,
                "protein": "38g"
            },
        ],
        "total_approx": {"calories": 1750, "protein": "150g"},
        "tips": [
            "Drink 3+ liters of water daily to manage hunger",
            "Eat vegetables freely — they are filling and low calorie",
            "Avoid liquid calories (soda, juice, alcohol)",
            "Don't cut too aggressively — losing >1kg/week burns muscle"
        ]
    },
    "maintenance": {
        "goal": "Maintenance & General Health",
        "calories": "At TDEE (Total Daily Energy Expenditure)",
        "macros": {"protein": "1.6–1.8g per kg", "carbs": "3–5g per kg", "fats": "1.0–1.2g per kg"},
        "description": "Balanced diet for sustaining current physique and promoting long-term health.",
        "meal_plan": [
            {
                "meal": "Breakfast (8:00 AM)",
                "foods": ["2 whole eggs", "Overnight oats with chia seeds", "Mixed berries", "Black coffee"],
                "approx_calories": 500,
                "protein": "22g"
            },
            {
                "meal": "Lunch (12:30 PM)",
                "foods": ["Turkey or chicken wrap (whole wheat)", "Mixed salad", "Fruit (orange or apple)"],
                "approx_calories": 550,
                "protein": "38g"
            },
            {
                "meal": "Snack (4:00 PM)",
                "foods": ["Handful of mixed nuts", "String cheese or yogurt"],
                "approx_calories": 250,
                "protein": "12g"
            },
            {
                "meal": "Dinner (7:00 PM)",
                "foods": ["150g chicken, beef, or fish", "1 cup pasta or rice", "Steamed vegetables", "Olive oil dressing"],
                "approx_calories": 600,
                "protein": "42g"
            },
        ],
        "total_approx": {"calories": 1900, "protein": "114g"},
        "tips": [
            "Eat whole, minimally processed foods as the foundation",
            "80/20 rule: eat healthy 80% of the time, enjoy treats 20%",
            "Monitor your weight weekly and adjust portions accordingly",
            "Include variety in your diet for all micronutrients"
        ]
    }
}

FOOD_DATABASE = {
    "High Protein Foods": [
        {"food": "Chicken Breast (100g)", "protein": "31g", "calories": 165},
        {"food": "Eggs (1 whole)", "protein": "6g", "calories": 78},
        {"food": "Greek Yogurt (100g)", "protein": "10g", "calories": 59},
        {"food": "Cottage Cheese (100g)", "protein": "11g", "calories": 98},
        {"food": "Tuna (100g, canned)", "protein": "26g", "calories": 116},
        {"food": "Salmon (100g)", "protein": "25g", "calories": 208},
        {"food": "Lentils (100g cooked)", "protein": "9g", "calories": 116},
        {"food": "Tofu (100g)", "protein": "8g", "calories": 76},
    ],
    "Complex Carbs": [
        {"food": "Brown Rice (100g cooked)", "carbs": "23g", "calories": 112},
        {"food": "Sweet Potato (100g)", "carbs": "20g", "calories": 86},
        {"food": "Oats (100g dry)", "carbs": "66g", "calories": 389},
        {"food": "Quinoa (100g cooked)", "carbs": "21g", "calories": 120},
        {"food": "Whole Wheat Bread (1 slice)", "carbs": "12g", "calories": 69},
    ],
    "Healthy Fats": [
        {"food": "Avocado (100g)", "fats": "15g", "calories": 160},
        {"food": "Almonds (30g)", "fats": "14g", "calories": 174},
        {"food": "Olive Oil (1 tbsp)", "fats": "14g", "calories": 119},
        {"food": "Walnuts (30g)", "fats": "18g", "calories": 196},
    ]
}


@diet_bp.route('/diet/<goal>', methods=['GET'])
def get_diet(goal):
    """Return diet plan for given goal."""
    goal = goal.lower()
    if goal not in DIET_PLANS:
        return jsonify({"error": f"Goal '{goal}' not found. Choose: muscle_gain, weight_loss, maintenance"}), 404
    return jsonify(DIET_PLANS[goal])


@diet_bp.route('/diet', methods=['GET'])
def get_all_diets():
    """Return summary of all diet goals."""
    summary = {k: {"goal": v["goal"], "calories": v["calories"], "description": v["description"]}
               for k, v in DIET_PLANS.items()}
    return jsonify(summary)


@diet_bp.route('/foods', methods=['GET'])
def get_foods():
    """Return food database."""
    return jsonify(FOOD_DATABASE)
