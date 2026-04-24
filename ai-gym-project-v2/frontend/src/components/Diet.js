import React, { useState, useEffect } from 'react';

const API_URL = "https://ai-gym-project-ey72.onrender.com";

const GOALS = [
  { id: 'muscle_gain', label: 'Muscle Gain', icon: '💪' },
  { id: 'weight_loss', label: 'Weight Loss', icon: '🔥' },
  { id: 'maintenance', label: 'Maintenance', icon: '⚖️' },
];

function Diet() {
  const [selectedGoal, setSelectedGoal] = useState('muscle_gain');
  const [plan, setPlan] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchPlan = async (goal) => {
    setLoading(true);
    setError('');
    setPlan(null);
    try {
      const res = await fetch(`${API_URL}/api/diet/${goal}`);
      if (!res.ok) throw new Error(`Server error: ${res.status}`);
      const data = await res.json();
      setPlan(data);
    } catch (err) {
      setError(`Could not load diet plan: ${err.message}. Make sure Flask backend is running.`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPlan(selectedGoal);
  }, [selectedGoal]);

  return (
    <div>
      <div className="section-header">
        <h2>🥗 Nutrition Plans</h2>
        <p>Personalized meal plans tailored to your fitness goals</p>
      </div>

      {/* Goal selector */}
      <div className="goal-selector">
        {GOALS.map(goal => (
          <button
            key={goal.id}
            className={`goal-btn ${selectedGoal === goal.id ? 'active' : ''}`}
            onClick={() => setSelectedGoal(goal.id)}
          >
            <span>{goal.icon}</span>
            {goal.label}
          </button>
        ))}
      </div>

      {/* Loading */}
      {loading && (
        <div className="loading-state">
          <div className="spinner" />
          <p>Loading nutrition plan...</p>
        </div>
      )}

      {/* Error */}
      {error && <div className="error-msg">⚠️ {error}</div>}

      {/* Diet plan */}
      {plan && !loading && (
        <div className="workout-plan">
          {/* Calories info */}
          <div className="plan-description">
            🎯 &nbsp;<strong>Calorie Target:</strong> {plan.calories}
          </div>

          {/* Macros */}
          <div className="macros-card">
            <div className="macro-item">
              <div className="macro-label">Protein</div>
              <div className="macro-value protein">{plan.macros?.protein || '—'}</div>
            </div>
            <div className="macro-item">
              <div className="macro-label">Carbohydrates</div>
              <div className="macro-value carbs">{plan.macros?.carbs || '—'}</div>
            </div>
            <div className="macro-item">
              <div className="macro-label">Healthy Fats</div>
              <div className="macro-value fats">{plan.macros?.fats || '—'}</div>
            </div>
            {plan.total_approx && (
              <div className="macro-item">
                <div className="macro-label">Daily Total</div>
                <div className="macro-value cals">{plan.total_approx.calories} kcal</div>
              </div>
            )}
          </div>

          {/* Meal plan */}
          {plan.meal_plan && (
            <>
              <h3 style={{ marginBottom: '16px', color: 'var(--text)', fontWeight: 700 }}>
                🍽️ Daily Meal Plan
              </h3>
              <div className="meal-cards">
                {plan.meal_plan.map((meal, i) => (
                  <div className="meal-card" key={i}>
                    <div className="meal-card-header">
                      <div className="meal-name">{meal.meal}</div>
                      <div className="meal-stats">
                        <span className="stat-badge cal">~{meal.approx_calories} kcal</span>
                        <span className="stat-badge prot">{meal.protein} protein</span>
                      </div>
                    </div>
                    <div className="meal-foods">
                      <ul>
                        {meal.foods.map((food, j) => (
                          <li key={j}>{food}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                ))}
              </div>
            </>
          )}

          {/* Tips */}
          {plan.tips && (
            <div className="tips-section">
              <h3>💡 Nutrition Tips</h3>
              <div className="tips-grid">
                {plan.tips.map((tip, i) => (
                  <div className="tip-card" key={i}>{tip}</div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default Diet;
