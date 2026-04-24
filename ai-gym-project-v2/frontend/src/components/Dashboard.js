import React, { useState, useEffect } from 'react';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

// ── Pure CSS bar chart (no library needed) ────────────────────────────────────
function BarChart({ data, valueKey, labelKey, color = '#00d4ff', maxOverride }) {
  const max = maxOverride || Math.max(...data.map(d => d[valueKey]));
  return (
    <div className="bar-chart">
      {data.map((d, i) => (
        <div key={i} className="bar-col">
          <div className="bar-value">{d[valueKey]}</div>
          <div className="bar-track">
            <div
              className="bar-fill"
              style={{
                height: `${(d[valueKey] / max) * 100}%`,
                background: color,
                animationDelay: `${i * 60}ms`,
              }}
            />
          </div>
          <div className="bar-label">{d[labelKey]}</div>
        </div>
      ))}
    </div>
  );
}

// ── Donut / pie slice chart ───────────────────────────────────────────────────
const SLICE_COLORS = ['#00d4ff', '#7c3aed', '#10b981', '#f59e0b', '#ef4444'];

function DonutChart({ data }) {
  let cumulative = 0;
  const total = data.reduce((s, d) => s + d.percentage, 0);
  const r = 54, cx = 70, cy = 70, circumference = 2 * Math.PI * r;

  return (
    <div className="donut-wrapper">
      <svg width="140" height="140" viewBox="0 0 140 140">
        {data.map((d, i) => {
          const pct = d.percentage / total;
          const dash = pct * circumference;
          const gap = circumference - dash;
          const offset = circumference - cumulative * circumference / total;
          cumulative += d.percentage;
          return (
            <circle
              key={i}
              cx={cx} cy={cy} r={r}
              fill="none"
              stroke={SLICE_COLORS[i]}
              strokeWidth="16"
              strokeDasharray={`${dash} ${gap}`}
              strokeDashoffset={offset}
              style={{ transition: 'stroke-dasharray 0.8s ease' }}
            />
          );
        })}
        <text x={cx} y={cy - 6} textAnchor="middle" fill="#e2e8f0" fontSize="13" fontWeight="700">Total</text>
        <text x={cx} y={cy + 12} textAnchor="middle" fill="#94a3b8" fontSize="11">
          {data.reduce((s, d) => s + d.count, 0)}
        </text>
      </svg>
      <div className="donut-legend">
        {data.map((d, i) => (
          <div key={i} className="legend-item">
            <span className="legend-dot" style={{ background: SLICE_COLORS[i] }} />
            <span className="legend-label">{d.type}</span>
            <span className="legend-pct">{d.percentage}%</span>
          </div>
        ))}
      </div>
    </div>
  );
}

// ── Calorie dual bar chart ────────────────────────────────────────────────────
function CalorieChart({ data }) {
  const max = Math.max(...data.flatMap(d => [d.consumed, d.burned]));
  return (
    <div className="calorie-chart">
      {data.map((d, i) => (
        <div key={i} className="cal-col">
          <div className="cal-bars">
            <div className="cal-bar-wrap">
              <div
                className="cal-bar consumed"
                style={{ height: `${(d.consumed / max) * 100}%`, animationDelay: `${i * 80}ms` }}
              />
            </div>
            <div className="cal-bar-wrap">
              <div
                className="cal-bar burned"
                style={{ height: `${(d.burned / max) * 100}%`, animationDelay: `${i * 80 + 40}ms` }}
              />
            </div>
          </div>
          <div className="cal-label">{d.week}</div>
        </div>
      ))}
      <div className="cal-legend">
        <span><span className="legend-dot" style={{ background: '#7c3aed' }} />Consumed</span>
        <span><span className="legend-dot" style={{ background: '#10b981' }} />Burned</span>
      </div>
    </div>
  );
}

// ── KPI card ─────────────────────────────────────────────────────────────────
function KpiCard({ icon, label, value, sub, color }) {
  return (
    <div className="kpi-card" style={{ borderTopColor: color }}>
      <div className="kpi-icon" style={{ background: color + '22', color }}>{icon}</div>
      <div className="kpi-body">
        <div className="kpi-value">{value}</div>
        <div className="kpi-label">{label}</div>
        {sub && <div className="kpi-sub">{sub}</div>}
      </div>
    </div>
  );
}

// ── Main Dashboard ────────────────────────────────────────────────────────────
function Dashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    (async () => {
      try {
        const res = await fetch(`${API_URL}/api/analytics/all`);
        if (!res.ok) throw new Error(`Server error ${res.status}`);
        setData(await res.json());
      } catch (err) {
        setError(`Could not load analytics: ${err.message}. Make sure Flask backend is running.`);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  if (loading) return (
    <div className="loading-state">
      <div className="spinner" />
      <p>Loading dashboard data...</p>
    </div>
  );

  if (error) return <div className="error-msg">⚠️ {error}</div>;

  const { summary, weekly_workouts, workout_distribution, calorie_trend, top_users, recent_activity } = data;

  return (
    <div>
      <div className="section-header">
        <h2>📊 Admin Dashboard</h2>
        <p>Real-time overview of platform activity, workouts, and user engagement</p>
      </div>

      {/* KPI Row */}
      <div className="kpi-grid">
        <KpiCard icon="💪" label="Total Workouts" value={summary.total_workouts.toLocaleString()} sub="All time" color="#00d4ff" />
        <KpiCard icon="👥" label="Total Users" value={summary.total_users} sub="Registered" color="#7c3aed" />
        <KpiCard icon="🔥" label="Calories Tracked" value={(summary.calories_tracked / 1000).toFixed(1) + 'k'} sub="kcal logged" color="#f59e0b" />
        <KpiCard icon="⚡" label="Active Today" value={summary.active_today} sub="Users" color="#10b981" />
        <KpiCard icon="⏱️" label="Avg Session" value={summary.avg_session_minutes + ' min'} sub="Per workout" color="#ec4899" />
        <KpiCard icon="🏆" label="Best Streak" value={summary.streak_record + ' days'} sub="Record" color="#f97316" />
      </div>

      {/* Charts row */}
      <div className="charts-grid">
        {/* Weekly bar chart */}
        <div className="chart-card">
          <h3 className="chart-title">📅 Workouts This Week</h3>
          <BarChart data={weekly_workouts} valueKey="count" labelKey="day" color="#00d4ff" />
        </div>

        {/* Donut chart */}
        <div className="chart-card">
          <h3 className="chart-title">🥧 Workout Types</h3>
          <DonutChart data={workout_distribution} />
        </div>

        {/* Calorie trend */}
        <div className="chart-card wide">
          <h3 className="chart-title">📈 4-Week Calorie Trend</h3>
          <CalorieChart data={calorie_trend} />
        </div>
      </div>

      {/* Bottom row: leaderboard + activity feed */}
      <div className="bottom-grid">

        {/* Leaderboard */}
        <div className="chart-card">
          <h3 className="chart-title">🏅 Top Users</h3>
          <table className="dash-table">
            <thead>
              <tr>
                <th>#</th>
                <th>User</th>
                <th>Workouts</th>
                <th>Streak</th>
                <th>Level</th>
              </tr>
            </thead>
            <tbody>
              {top_users.map((u, i) => (
                <tr key={i}>
                  <td>
                    <span className="rank-badge">{i === 0 ? '🥇' : i === 1 ? '🥈' : i === 2 ? '🥉' : `#${i + 1}`}</span>
                  </td>
                  <td style={{ fontWeight: 600, color: 'var(--text)' }}>{u.name}</td>
                  <td>{u.workouts}</td>
                  <td><span className="streak-pill">🔥 {u.streak}d</span></td>
                  <td>
                    <span className={`level-tag level-${u.level.toLowerCase()}`}>{u.level}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Activity feed */}
        <div className="chart-card">
          <h3 className="chart-title">⚡ Recent Activity</h3>
          <div className="activity-feed">
            {recent_activity.map((a, i) => (
              <div key={i} className="activity-item">
                <div className="activity-dot" />
                <div className="activity-body">
                  <div className="activity-user">{a.user}</div>
                  <div className="activity-action">{a.action}</div>
                  <div className="activity-meta">
                    <span className="activity-time">{a.time}</span>
                    {a.calories > 0 && (
                      <span className="activity-cal">🔥 {a.calories} kcal</span>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

      </div>
    </div>
  );
}

export default Dashboard;
