import React, { useState, useEffect } from 'react';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const LEVELS = [
  { id: 'beginner', label: 'Beginner', icon: '🌱' },
  { id: 'intermediate', label: 'Intermediate', icon: '🔥' },
  { id: 'advanced', label: 'Advanced', icon: '⚡' },
];

function Workout() {
  const [selectedLevel, setSelectedLevel] = useState('beginner');
  const [plan, setPlan] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchPlan = async (level) => {
    setLoading(true);
    setError('');
    setPlan(null);
    try {
      const res = await fetch(`${API_URL}/api/workout/${level}`);
      if (!res.ok) throw new Error(`Server error: ${res.status}`);
      const data = await res.json();
      setPlan(data);
    } catch (err) {
      setError(`Could not load workout plan: ${err.message}. Make sure Flask backend is running.`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPlan(selectedLevel);
  }, [selectedLevel]);

  return (
    <div>
      <div className="section-header">
        <h2>💪 Workout Plans</h2>
        <p>Science-backed training programs for every fitness level</p>
      </div>

      {/* Level selector */}
      <div className="level-selector">
        {LEVELS.map(lvl => (
          <button
            key={lvl.id}
            className={`level-btn ${selectedLevel === lvl.id ? 'active' : ''}`}
            onClick={() => setSelectedLevel(lvl.id)}
          >
            <span>{lvl.icon}</span>
            {lvl.label}
          </button>
        ))}
      </div>

      {/* Loading state */}
      {loading && (
        <div className="loading-state">
          <div className="spinner" />
          <p>Loading workout plan...</p>
        </div>
      )}

      {/* Error state */}
      {error && <div className="error-msg">⚠️ {error}</div>}

      {/* Workout plan */}
      {plan && !loading && (
        <div className="workout-plan">
          {/* Meta info */}
          <div className="plan-meta">
            <div className="meta-card">
              <div className="meta-label">Level</div>
              <div className="meta-value">{plan.level}</div>
            </div>
            <div className="meta-card">
              <div className="meta-label">Duration</div>
              <div className="meta-value">{plan.duration}</div>
            </div>
            <div className="meta-card">
              <div className="meta-label">Frequency</div>
              <div className="meta-value">{plan.frequency}</div>
            </div>
          </div>

          {/* Description */}
          <div className="plan-description">
            ℹ️ &nbsp;{plan.description}
          </div>

          {/* Schedule */}
          {plan.schedule && plan.schedule.map((day, i) => (
            <div className="day-card" key={i}>
              <div className="day-header">{day.day}</div>
              <table className="exercises-table">
                <thead>
                  <tr>
                    <th>Exercise</th>
                    <th>Sets</th>
                    <th>Reps</th>
                    <th>Rest</th>
                  </tr>
                </thead>
                <tbody>
                  {day.exercises.map((ex, j) => (
                    <tr key={j}>
                      <td>{ex.name}</td>
                      <td>{ex.sets}</td>
                      <td>{ex.reps}</td>
                      <td>{ex.rest}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ))}

          {/* Tips */}
          {plan.tips && (
            <div className="tips-section">
              <h3>💡 Pro Tips</h3>
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

export default Workout;
