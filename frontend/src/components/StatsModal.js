import React from 'react';
import './StatsModal.css';

function StatsModal({ isOpen, onClose, puzzle, gameState }) {
  if (!isOpen) return null;

  // Mock stats data - will be replaced with API data
  const playerStats = {
    totalPlayed: 42,
    winRate: 73,
    currentStreak: 5,
    maxStreak: 12,
    averageTime: 127, // seconds
    categoryStats: {
      math: { played: 15, won: 11 },
      word: { played: 14, won: 10 },
      art: { played: 13, won: 9 }
    }
  };

  const stumpTally = [
    { model: 'claude-3', stumps: 12, total: 28, rate: 43 },
    { model: 'gpt4o', stumps: 8, total: 25, rate: 32 },
    { model: 'gemini', stumps: 6, total: 22, rate: 27 }
  ];

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Statistics</h2>
          <button className="close-button" onClick={onClose}>×</button>
        </div>

        <div className="stats-container">
          <section className="player-stats">
            <h3>Your Performance</h3>
            <div className="stats-grid">
              <div className="stat-item">
                <span className="stat-number">{playerStats.totalPlayed}</span>
                <span className="stat-label">Played</span>
              </div>
              <div className="stat-item">
                <span className="stat-number">{playerStats.winRate}%</span>
                <span className="stat-label">Win Rate</span>
              </div>
              <div className="stat-item">
                <span className="stat-number">{playerStats.currentStreak}</span>
                <span className="stat-label">Current Streak</span>
              </div>
              <div className="stat-item">
                <span className="stat-number">{playerStats.maxStreak}</span>
                <span className="stat-label">Max Streak</span>
              </div>
            </div>

            <div className="average-time">
              <span className="time-label">Average Solve Time:</span>
              <span className="time-value">{formatTime(playerStats.averageTime)}</span>
            </div>
          </section>

          <section className="category-breakdown">
            <h3>Category Performance</h3>
            <div className="category-stats">
              {Object.entries(playerStats.categoryStats).map(([category, stats]) => {
                const rate = Math.round((stats.won / stats.played) * 100);
                return (
                  <div key={category} className="category-stat">
                    <div className="category-header">
                      <span className="category-name">{category.toUpperCase()}</span>
                      <span className="category-rate">{rate}%</span>
                    </div>
                    <div className="category-bar">
                      <div 
                        className="category-fill"
                        style={{ width: `${rate}%` }}
                      ></div>
                    </div>
                    <span className="category-count">{stats.won}/{stats.played}</span>
                  </div>
                );
              })}
            </div>
          </section>

          <section className="stump-tally">
            <h3>AI Stump Leaderboard</h3>
            <p className="stump-description">
              Which AI models are best at stumping humans?
            </p>
            <div className="stump-list">
              {stumpTally.map((model, index) => (
                <div key={model.model} className="stump-item">
                  <div className="rank-badge">{index + 1}</div>
                  <div className="model-info">
                    <span className="model-name">{model.model}</span>
                    <span className="model-stats">
                      {model.stumps}/{model.total} puzzles ({model.rate}%)
                    </span>
                  </div>
                  <div className="stump-bar">
                    <div 
                      className="stump-fill"
                      style={{ width: `${model.rate}%` }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          </section>

          {gameState !== 'playing' && (
            <section className="share-section">
              <h3>Share Today's Result</h3>
              <button className="share-button">
                📋 Copy Result to Clipboard
              </button>
            </section>
          )}
        </div>
      </div>
    </div>
  );
}

export default StatsModal;