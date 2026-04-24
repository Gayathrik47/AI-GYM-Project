import React, { useState } from 'react';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const MOOD_OPTIONS = [
  { value: 'good', label: '😊 Good', color: '#10b981' },
  { value: 'neutral', label: '😐 Neutral', color: '#f59e0b' },
  { value: 'bad', label: '😞 Bad', color: '#ef4444' },
];

const DEFAULT_FORM = {
  days_since_last_workout: 1,
  workouts_this_week: 3,
  mood: 'neutral',
  sleep_hours: 7,
  stress_level: 5,
  hour_of_day: new Date().getHours(),
};

const LOG_DEFAULT = {
  workout_type: 'strength',
  duration_minutes: 45,
  calories_burned: 300,
};

const RISK_COLORS = { low: '#10b981', medium: '#f59e0b', high: '#ef4444' };
const RISK_BG = {
  low: 'rgba(16,185,129,0.08)',
  medium: 'rgba(245,158,11,0.08)',
  high: 'rgba(239,68,68,0.08)',
};
const RISK_BORDER = {
  low: 'rgba(16,185,129,0.35)',
  medium: 'rgba(245,158,11,0.35)',
  high: 'rgba(239,68,68,0.35)',
};

function HabitTracker() {
  const [form, setForm] = useState(DEFAULT_FORM);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const [logForm, setLogForm] = useState(LOG_DEFAULT);
  const [logResult, setLogResult] = useState(null);
  const [logLoading, setLogLoading] = useState(false);

  // ── Predict skip risk ────────────────────────────────────────────────────────
  const handlePredict = async () => {
    setLoading(true);
    setError('');
    setResult(null);
    try {
      const res = await fetch(`${API_URL}/api/habit`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });
      if (!res.ok) throw new Error(`Server error ${res.status}`);
      const data = await res.json();
      setResult(data);
    } catch (err) {
      setError(`Connection error: ${err.message}. Make sure Flask is running on port 5000.`);
    } finally {
      setLoading(false);
    }
  };

  // ── Log a completed workout ──────────────────────────────────────────────────
  const handleLog = async () => {
    setLogLoading(true);
    setLogResult(null);
    try {
      const res = await fetch(`${API_URL}/api/habit/log`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(logForm),
      });
      if (!res.ok) throw new Error(`Server error ${res.status}`);
      const data = await res.json();
      setLogResult(data);
    } catch (err) {
      setLogResult({ error: err.message });
    } finally {
      setLogLoading(false);
    }
  };

  const set = (key, val) => setForm(f => ({ ...f, [key]: val }));

  return (
    <div>
      <div className="section-header">
        <h2>🧠 Behavior AI — Habit Tracker</h2>
        <p>Predict your workout skip risk and stay consistent with AI-powered nudges</p>
      </div>

      <div className="habit-grid">
        {/* ── LEFT: Predictor form ── */}
        <div className="habit-card">
          <h3 className="habit-card-title">📊 Skip Risk Predictor</h3>
          <p className="habit-card-sub">Fill in your current state to get a skip-risk score</p>

          {/* Days since last workout */}
          <div className="form-group">
            <label className="form-label">Days since last workout</label>
            <div className="range-row">
              <input
                type="range" min="0" max="7"
                value={form.days_since_last_workout}
                onChange={e => set('days_since_last_workout', +e.target.value)}
                className="range-input"
              />
              <span className="range-val">{form.days_since_last_workout}d</span>
            </div>
          </div>

          {/* Workouts this week */}
          <div className="form-group">
            <label className="form-label">Workouts completed this week</label>
            <div className="range-row">
              <input
                type="range" min="0" max="7"
                value={form.workouts_this_week}
                onChange={e => set('workouts_this_week', +e.target.value)}
                className="range-input accent2"
              />
              <span className="range-val">{form.workouts_this_week}</span>
            </div>
          </div>

          {/* Mood */}
          <div className="form-group">
            <label className="form-label">Current mood</label>
            <div className="mood-row">
              {MOOD_OPTIONS.map(m => (
                <button
                  key={m.value}
                  className={`mood-btn ${form.mood === m.value ? 'active' : ''}`}
                  style={form.mood === m.value ? { borderColor: m.color, background: m.color + '22', color: m.color } : {}}
                  onClick={() => set('mood', m.value)}
                >
                  {m.label}
                </button>
              ))}
            </div>
          </div>

          {/* Sleep hours */}
          <div className="form-group">
            <label className="form-label">Sleep last night</label>
            <div className="range-row">
              <input
                type="range" min="3" max="10" step="0.5"
                value={form.sleep_hours}
                onChange={e => set('sleep_hours', +e.target.value)}
                className="range-input green"
              />
              <span className="range-val">{form.sleep_hours}h</span>
            </div>
          </div>

          {/* Stress level */}
          <div className="form-group">
            <label className="form-label">Stress level (1 = calm, 10 = overwhelmed)</label>
            <div className="range-row">
              <input
                type="range" min="1" max="10"
                value={form.stress_level}
                onChange={e => set('stress_level', +e.target.value)}
                className="range-input red"
              />
              <span className="range-val">{form.stress_level}/10</span>
            </div>
          </div>

          {/* Hour of day */}
          <div className="form-group">
            <label className="form-label">Hour of day (24h)</label>
            <div className="range-row">
              <input
                type="range" min="0" max="23"
                value={form.hour_of_day}
                onChange={e => set('hour_of_day', +e.target.value)}
                className="range-input"
              />
              <span className="range-val">{String(form.hour_of_day).padStart(2,'0')}:00</span>
            </div>
          </div>

          <button className="predict-btn" onClick={handlePredict} disabled={loading}>
            {loading ? '⏳ Analyzing...' : '🔍 Predict My Skip Risk'}
          </button>

          {error && <div className="error-msg" style={{ marginTop: 14 }}>⚠️ {error}</div>}
        </div>

        {/* ── RIGHT: Result + Log ── */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>

          {/* Result card */}
          {result ? (
            <div className="result-card"
              style={{ background: RISK_BG[result.risk_level], border: `1px solid ${RISK_BORDER[result.risk_level]}` }}>
              <div className="result-emoji">{result.emoji}</div>
              <div className="result-title" style={{ color: RISK_COLORS[result.risk_level] }}>
                {result.title}
              </div>
              <p className="result-message">{result.message}</p>
              <div className="result-tip">💡 {result.tip}</div>

              {/* Score bar */}
              <div className="score-section">
                <div className="score-label-row">
                  <span>Risk Score</span>
                  <span style={{ color: RISK_COLORS[result.risk_level], fontWeight: 700 }}>
                    {result.score}/15
                  </span>
                </div>
                <div className="score-bar-bg">
                  <div className="score-bar-fill"
                    style={{
                      width: `${Math.min((result.score / 15) * 100, 100)}%`,
                      background: RISK_COLORS[result.risk_level],
                    }}
                  />
                </div>
                <div className="score-ticks">
                  <span style={{ color: '#10b981' }}>Low</span>
                  <span style={{ color: '#f59e0b' }}>Medium</span>
                  <span style={{ color: '#ef4444' }}>High</span>
                </div>
              </div>

              {/* Inputs summary */}
              <div className="inputs-grid">
                {Object.entries(result.inputs_used).map(([k, v]) => (
                  <div key={k} className="input-pill">
                    <span className="input-pill-key">{k.replace(/_/g, ' ')}</span>
                    <span className="input-pill-val">{String(v)}</span>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div className="empty-result">
              <div style={{ fontSize: '3rem', marginBottom: 12 }}>🎯</div>
              <p>Fill in your details and click <strong>Predict My Skip Risk</strong> to get your personalized behavior analysis.</p>
            </div>
          )}

          {/* ── Log Workout card ── */}
          <div className="habit-card">
            <h3 className="habit-card-title">✅ Log Completed Workout</h3>

            <div className="log-form-row">
              <div className="form-group" style={{ flex: 1 }}>
                <label className="form-label">Workout type</label>
                <select
                  className="select-input"
                  value={logForm.workout_type}
                  onChange={e => setLogForm(f => ({ ...f, workout_type: e.target.value }))}
                >
                  {['strength','cardio','hiit','yoga','sports','other'].map(t => (
                    <option key={t} value={t}>{t.charAt(0).toUpperCase() + t.slice(1)}</option>
                  ))}
                </select>
              </div>
              <div className="form-group" style={{ flex: 1 }}>
                <label className="form-label">Duration (min)</label>
                <input
                  type="number" min="1" max="300"
                  className="number-input"
                  value={logForm.duration_minutes}
                  onChange={e => setLogForm(f => ({ ...f, duration_minutes: +e.target.value }))}
                />
              </div>
              <div className="form-group" style={{ flex: 1 }}>
                <label className="form-label">Calories burned</label>
                <input
                  type="number" min="0" max="2000"
                  className="number-input"
                  value={logForm.calories_burned}
                  onChange={e => setLogForm(f => ({ ...f, calories_burned: +e.target.value }))}
                />
              </div>
            </div>

            <button className="log-btn" onClick={handleLog} disabled={logLoading}>
              {logLoading ? '⏳ Logging...' : '📝 Log Workout'}
            </button>

            {logResult && !logResult.error && (
              <div className="log-result">
                <div className="log-badge">{logResult.badge}</div>
                <p className="log-message">{logResult.message}</p>
                <p className="log-tip">🔗 {logResult.streak_tip}</p>
              </div>
            )}
            {logResult?.error && (
              <div className="error-msg" style={{ marginTop: 12 }}>⚠️ {logResult.error}</div>
            )}
          </div>

        </div>
      </div>
    </div>
  );
}

export default HabitTracker;
