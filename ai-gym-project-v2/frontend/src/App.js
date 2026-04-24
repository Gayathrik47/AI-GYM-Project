import React, { useState } from 'react';
import Chat from './components/Chat';
import Workout from './components/Workout';
import Diet from './components/Diet';
import HabitTracker from './components/HabitTracker';   // NEW
import Dashboard from './components/Dashboard';         // NEW
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('chat');

  const tabs = [
    { id: 'chat',    label: 'AI Coach',     icon: '🤖' },
    { id: 'workout', label: 'Workouts',     icon: '💪' },
    { id: 'diet',    label: 'Nutrition',    icon: '🥗' },
    { id: 'habit',   label: 'Behavior AI',  icon: '🧠' },  // NEW
    { id: 'dash',    label: 'Dashboard',    icon: '📊' },  // NEW
  ];

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="header-inner">
          <div className="logo">
            <span className="logo-icon"></span>
            <div>
              <h1 className="logo-title">FitAI</h1>
              <p className="logo-sub">Your AI-Powered Fitness Coach</p>
            </div>
          </div>
          
        </div>
      </header>

      {/* Tab Navigation */}
      <nav className="tab-nav">
        {tabs.map(tab => (
          <button
            key={tab.id}
            className={`tab-btn ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => setActiveTab(tab.id)}
          >
            <span className="tab-icon">{tab.icon}</span>
            <span className="tab-label">{tab.label}</span>
          </button>
        ))}
      </nav>

      {/* Main Content */}
      <main className="main-content">
        {activeTab === 'chat'    && <Chat />}
        {activeTab === 'workout' && <Workout />}
        {activeTab === 'diet'    && <Diet />}
        {activeTab === 'habit'   && <HabitTracker />}
        {activeTab === 'dash'    && <Dashboard />}
      </main>

      <footer className="footer">
        <p>FitAI v2.0 — AI Gym & Fitness Assistant | React + Flask | College Major Project</p>
      </footer>
    </div>
  );
}

export default App;
