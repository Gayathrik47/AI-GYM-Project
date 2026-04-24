from flask import Blueprint, request, jsonify
import random

chat_bp = Blueprint('chat', __name__)

# ── Upgraded Response Bank ─────────────────────────────────────────────────────
RESPONSES = {
    "greet": [
        "Hey there, champion! 💪 Ready to crush your fitness goals? Ask me about workouts, nutrition, recovery, habits, or anything fitness-related!",
        "Hello, athlete! I'm FitAI v2 — your upgraded AI fitness coach. Workout plans, diet advice, habit tracking — I've got you covered!",
        "Welcome back! 🔥 What's on your fitness agenda today?",
    ],
    "how_are_you": [
        "Running at 100% and ready to help you hit your fitness goals! What do you need today?",
        "Feeling optimized! 💡 How can I help you train smarter today?",
    ],
    "what_can_you_do": [
        "I can help you with: 💪 Workout plans (Beginner/Intermediate/Advanced), 🥗 Diet plans (Muscle Gain/Weight Loss/Maintenance), 🧠 Behavior AI skip risk prediction, 📊 Admin Analytics dashboard, 💬 Fitness Q&A on any topic. Try the tabs above or just ask me!",
    ],
    "thanks": [
        "You're welcome! Keep showing up — the results will follow. 💪 Anything else?",
        "Happy to help! Now go crush that workout! 🔥",
    ],
    "muscle": [
        "Muscle gain blueprint: (1) Progressive overload every week, (2) 1.8–2.2g protein per kg bodyweight, (3) 7–9h sleep for hormone release, (4) Compound lifts: squat, deadlift, bench, row, press. Consistency over 3–6 months is where the transformation happens! 💪",
        "Muscle = stimulus + nutrition + recovery. Train each muscle 2x/week with 10–20 sets total. Prioritize compound movements and track your lifts to ensure progressive overload.",
    ],
    "weight_loss": [
        "Fat loss formula: 300–500 kcal deficit/day + strength training (preserves muscle) + cardio (boosts deficit). Target 0.5–1% bodyweight loss per week — faster = muscle loss. 🔥",
        "HIIT + compound lifts + high-protein diet = the fat loss trinity. Avoid excessive steady-state cardio alone — it elevates cortisol and can eat muscle mass.",
    ],
    "cardio": [
        "Zone 2 cardio (60–70% max HR, conversational pace): 3–4x/week, 30–45 min — best for fat burning and aerobic base. HIIT (85–95% max HR): 2–3x/week, 20–30 min — metabolic conditioning. Don't combine both daily — recovery matters! 🏃",
        "Best cardio = the type you'll actually do. Running, cycling, rowing, swimming all work. Aim for 150 min/week moderate intensity as a baseline.",
    ],
    "beginner": [
        "Beginner blueprint: (1) 3 full-body workouts/week, (2) Learn squat, hinge, push, pull, carry patterns, (3) 1–2 working sets per exercise to start, (4) Add one set or small weight increase per week. Nail form before adding load! 🌱",
        "Beginner tip: compound movements give the most value. Squat, deadlift, bench, overhead press, rows. Perfect form with lighter weight for 4–6 weeks before increasing.",
    ],
    "intermediate": [
        "Intermediate upgrade: switch to Push/Pull/Legs or Upper/Lower split (4 days/week). Introduce periodization — alternate hypertrophy (8–12 reps) and strength (3–6 reps) phases every 4–6 weeks.",
        "Intermediate plateau? Try: (1) Deload week, (2) Change rep ranges, (3) Slow eccentric (3–4 second lowering), (4) Increase frequency on lagging muscle groups.",
    ],
    "advanced": [
        "Advanced athletes: use daily undulating periodization (DUP), blood-flow restriction for accessories, RPE-based autoregulation, and precise peri-workout nutrition. Small margins matter now. 🏆",
        "At advanced level, focus on: sleep quality over just hours, nutrient timing, addressing specific weak points, and intelligent deloading. Get blood work done yearly to optimize health markers.",
    ],
    "skip": [
        "Feeling like skipping? Use the 10-minute rule — commit to just 10 minutes. Once you're moving, you'll almost always finish. A 20-min workout beats zero every single time! 🚀",
        "Check the Behavior AI tab — enter your mood, sleep, and activity to get a personalized skip risk score and motivation tip tailored to your situation!",
    ],
    "habit": [
        "Habit building formula: same time + same place + low friction = automatic behavior. Prepare your gym bag the night before. Track streaks. Use the Behavior AI tab to monitor your skip risk score! 📊",
        "The #1 secret to consistency: reduce decision fatigue. Schedule workouts like meetings — if it's not in the calendar, it doesn't exist.",
    ],
    "diet": [
        "Fitness diet foundation: (1) Protein 1.6–2.2g/kg bodyweight, (2) Mostly whole foods, (3) Veggies at every meal, (4) Calories matched to goal (surplus/deficit/maintenance). Check the Nutrition tab for a full personalized meal plan! 🥗",
        "Don't over-complicate nutrition. Hit your protein target, eat mostly whole foods, stay in the right calorie range. That's 90% of the battle — the other 10% is optimization.",
    ],
    "protein": [
        "Top protein sources: chicken breast (31g/100g), eggs (6g each), Greek yogurt (10g/100g), tuna (26g/100g), lentils (9g/100g), cottage cheese (11g/100g). Target 1.6–2.2g per kg bodyweight daily. 🥩",
        "Spread protein across 4–6 meals for maximum muscle protein synthesis. Post-workout protein matters but total daily intake matters far more.",
    ],
    "calorie": [
        "TDEE = BMR × Activity Factor. Sedentary ×1.2, Lightly active ×1.375, Moderately active ×1.55, Very active ×1.725. Add 300–500 kcal for muscle gain, subtract 300–500 for fat loss.",
        "Most people underestimate calorie intake by 30–40%. Track everything for 2–3 weeks — it's an eye-opener and often immediately solves 'I can't lose weight' problems.",
    ],
    "supplement": [
        "Evidence-ranked supplements: (1) Creatine monohydrate 3–5g/day ✅, (2) Protein powder (if diet gaps), (3) Vitamin D 2000–4000 IU, (4) Omega-3 2–3g EPA+DHA, (5) Magnesium glycinate 300mg before bed. Everything else is mostly marketing. 💊",
        "Creatine is the most studied safe performance supplement ever. 3–5g/day, no loading needed, taken any time. It increases strength, power, and muscle hydration.",
    ],
    "water": [
        "Hydration target: 35–45ml per kg bodyweight daily, +500–750ml per hour of exercise. Even 2% dehydration reduces strength output and cognitive performance significantly. 💧",
        "Drink 500ml of water first thing in the morning — it boosts alertness and starts your hydration baseline before coffee hits.",
    ],
    "sleep": [
        "Sleep is the #1 free performance enhancer. 7–9h allows: peak testosterone/GH release (muscle growth), memory consolidation, fat metabolism, and cognitive recovery. Cutting sleep for extra training is counterproductive. 😴",
        "Sleep optimization: consistent bedtime, dark + cool room (18–20°C), no screens 1h before bed, magnesium glycinate supplement, and avoid caffeine after 2pm.",
    ],
    "recovery": [
        "Recovery toolkit: (1) 7–9h sleep, (2) Post-workout protein + carb meal within 2h, (3) Active recovery days (light walk, yoga), (4) Foam rolling, (5) Cold shower, (6) Deload week every 4–8 weeks. Recovery = where strength is actually built. 🧊",
        "Signs you need more recovery: persistent soreness >72h, declining performance, irritability, poor sleep. Listen to your body — it's sending a signal.",
    ],
    "deload": [
        "Deload = reduce volume by 40–60% at the same intensity, every 4–8 weeks. It's not lazy — CNS fatigue accumulates even when muscles feel fine. Post-deload PRs are common.",
        "Deload options: (1) Cut sets in half, (2) Drop weight 20% and focus on technique, (3) Full rest week. After a deload you'll often hit new personal records — this is called supercompensation.",
    ],
    "injury": [
        "Injury protocol: (1) Rest the acute phase 48–72h, (2) Ice for inflammation/swelling, (3) Never train through sharp or joint pain, (4) Train around it — keep everything else active, (5) See a physio for persistent issues. ⚠️ Not medical advice — consult a professional!",
        "Most gym injuries: ego lifting, skipped warm-up, overuse, or poor technique. Prevention is always better — warm up 5–10 min, progress weights 2.5–5% at a time, prioritize form.",
    ],
    "bmi": [
        "BMI = weight(kg) / height(m)². Under 18.5 = underweight, 18.5–24.9 = normal, 25–29.9 = overweight, 30+ = obese. Important: BMI ignores muscle mass — muscular athletes often show 'overweight'. Body fat % is far more useful for fitness. 📊",
    ],
    "plateau": [
        "Plateau-busting strategies: (1) Change rep ranges (if doing 3×10, try 5×5 or 4×15), (2) Audit protein intake, (3) Add a deload week, (4) Improve sleep, (5) Add a new movement pattern. Plateaus are solvable if you diagnose the cause.",
        "Strength plateau? Do a 4-week strength block (3–5 reps, heavier weight), then return to hypertrophy work. The cross-training effect often smashes stalls.",
    ],
    "motivation": [
        "Motivation fades — systems don't. Build a system: 'I train at 6am on Mon/Wed/Fri, no exceptions.' Schedule it, prepare the night before, track streaks. Discipline is motivation's more reliable cousin. 🔥",
        "Nobody feels motivated every day — the pros show up anyway. Use the habit tracker, set a non-negotiable minimum (even 15 min counts), and remember: every workout is a vote for the person you're becoming.",
    ],
    "default": [
        "Great topic! Try being more specific — e.g. 'how to build muscle', 'beginner workout plan', 'weight loss diet', or 'how to stay consistent'. I'm best at workout plans, nutrition, recovery, and habit building!",
        "I specialize in fitness and nutrition. Ask about: workouts, diet, supplements, recovery, motivation, or use the tabs for structured plans. What's your specific goal?",
        "Hmm, not sure about that one — try rephrasing! Or explore the Workout, Nutrition, Behavior AI, and Dashboard tabs for structured content. 💪",
    ]
}

# ── Priority-ordered keyword rules ────────────────────────────────────────────
RULES = [
    (["hi", "hello", "hey", "howdy", "sup", "yo", "hiya"], "greet"),
    (["how are you", "how r u", "what's up", "wassup"], "how_are_you"),
    (["what can you", "what do you do", "help me", "capabilities", "what are you"], "what_can_you_do"),
    (["thank", "thanks", "thx", "cheers", "appreciate"], "thanks"),
    (["skip", "don't want to", "cant workout", "too tired to go", "lazy today"], "skip"),
    (["habit", "consistent", "consistency", "streak", "routine", "discipline"], "habit"),
    (["muscle", "bulk", "mass", "hypertrophy", "gain size", "build muscle"], "muscle"),
    (["lose weight", "fat loss", "weight loss", "slim", "cut ", "shred", "burning fat", "lose fat"], "weight_loss"),
    (["cardio", "running", "cycling", "hiit", "endurance", "aerobic", "treadmill", "jogging"], "cardio"),
    (["beginner", "starting out", "new to gym", "newbie", "first time", "never worked out"], "beginner"),
    (["intermediate"], "intermediate"),
    (["advanced", "elite", "experienced lifter"], "advanced"),
    (["plateau", "stuck", "no progress", "not improving", "stalled"], "plateau"),
    (["deload", "rest week", "overtraining", "overtrained"], "deload"),
    (["injury", "injured", "hurt", "pain", "sore", "strain", "sprain"], "injury"),
    (["protein", "whey", "casein", "amino acid"], "protein"),
    (["calorie", "calories", "tdee", "bmr", "energy intake", "how much to eat"], "calorie"),
    (["supplement", "creatine", "pre-workout", "vitamins", "bcaa"], "supplement"),
    (["water", "hydrat", "how much to drink"], "water"),
    (["sleep", "rest day", "insomnia", "fatigue", "tired all"], "sleep"),
    (["recover", "recovery", "soreness", "doms"], "recovery"),
    (["bmi", "body mass index", "body fat percentage"], "bmi"),
    (["diet", "nutrition", "eat", "food", "meal", "macro", "keto", "vegan"], "diet"),
    (["motivat", "inspire", "give up", "quit", "unmotivated", "discouraged"], "motivation"),
]


def get_ai_response(message: str) -> str:
    """Upgraded rule-based NLP with priority keyword matching."""
    msg = message.lower().strip()
    for keywords, category in RULES:
        if any(kw in msg for kw in keywords):
            return random.choice(RESPONSES[category])
    return random.choice(RESPONSES["default"])


@chat_bp.route('/chat', methods=['POST'])
def chat():
    """POST /api/chat"""
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "No message provided"}), 400
    user_message = data['message'].strip()
    if not user_message:
        return jsonify({"error": "Message cannot be empty"}), 400
    if len(user_message) > 500:
        return jsonify({"error": "Message too long (max 500 chars)"}), 400
    return jsonify({"response": get_ai_response(user_message), "status": "success"})
