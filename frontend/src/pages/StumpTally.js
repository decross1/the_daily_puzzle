import React, { useState } from 'react';
import './StumpTally.css';

function StumpTally() {
  const [selectedPeriod, setSelectedPeriod] = useState('month');

  // Mock stump tally data
  const modelStats = {
    month: [
      { 
        model: 'Claude-3', 
        stumps: 8, 
        attempts: 30, 
        stumpRate: 26.7,
        bestCategory: 'Word',
        recentStumps: ['Logic Riddle', 'Anagram Challenge', 'Word Association']
      },
      { 
        model: 'GPT-4o', 
        stumps: 6, 
        attempts: 30, 
        stumpRate: 20.0,
        bestCategory: 'Math',
        recentStumps: ['Complex Algebra', 'Number Theory', 'Calculus Problem']
      },
      { 
        model: 'Gemini', 
        stumps: 4, 
        attempts: 30, 
        stumpRate: 13.3,
        bestCategory: 'Art',
        recentStumps: ['Visual Pattern', 'Music Theory', 'Art History']
      }
    ],
    year: [
      { 
        model: 'Claude-3', 
        stumps: 89, 
        attempts: 365, 
        stumpRate: 24.4,
        bestCategory: 'Word',
        recentStumps: ['Logic Riddle', 'Anagram Challenge', 'Word Association']
      },
      { 
        model: 'GPT-4o', 
        stumps: 72, 
        attempts: 365, 
        stumpRate: 19.7,
        bestCategory: 'Math',
        recentStumps: ['Complex Algebra', 'Number Theory', 'Calculus Problem']
      },
      { 
        model: 'Gemini', 
        stumps: 58, 
        attempts: 365, 
        stumpRate: 15.9,
        bestCategory: 'Art',
        recentStumps: ['Visual Pattern', 'Music Theory', 'Art History']
      }
    ]
  };

  const currentStats = modelStats[selectedPeriod];

  const getModelIcon = (model) => {
    switch(model.toLowerCase()) {
      case 'claude-3': return '🤖';
      case 'gpt-4o': return '🧠';
      case 'gemini': return '💎';
      default: return '🔬';
    }
  };

  const getStumpRateColor = (rate) => {
    if (rate >= 25) return '#dc3545'; // High stump rate - red
    if (rate >= 15) return '#ffc107'; // Medium stump rate - yellow
    return '#28a745'; // Low stump rate - green
  };

  const getRankBadge = (index) => {
    switch(index) {
      case 0: return { icon: '👑', title: 'Stump Master' };
      case 1: return { icon: '🥈', title: 'Runner Up' };
      case 2: return { icon: '🥉', title: 'Third Place' };
      default: return { icon: '🤖', title: 'Participant' };
    }
  };

  return (
    <div className="stump-tally-page">
      <div className="stump-container">
        <div className="stump-header">
          <h1>🏴‍☠️ Stump Tally</h1>
          <p>Track which AI models are best at stumping human players</p>
        </div>

        <div className="period-selector">
          <button 
            className={`period-btn ${selectedPeriod === 'month' ? 'active' : ''}`}
            onClick={() => setSelectedPeriod('month')}
          >
            This Month
          </button>
          <button 
            className={`period-btn ${selectedPeriod === 'year' ? 'active' : ''}`}
            onClick={() => setSelectedPeriod('year')}
          >
            This Year
          </button>
        </div>

        <div className="models-grid">
          {currentStats.map((model, index) => {
            const badge = getRankBadge(index);
            return (
              <div key={model.model} className={`model-card rank-${index + 1}`}>
                <div className="model-header">
                  <div className="model-info">
                    <span className="model-icon">{getModelIcon(model.model)}</span>
                    <h3>{model.model}</h3>
                  </div>
                  <div className="rank-badge">
                    <span className="rank-icon">{badge.icon}</span>
                    <span className="rank-title">{badge.title}</span>
                  </div>
                </div>

                <div className="model-stats">
                  <div className="main-stat">
                    <span className="stat-number">{model.stumps}</span>
                    <span className="stat-label">Total Stumps</span>
                  </div>
                  
                  <div className="stat-row">
                    <div className="stat-item">
                      <span className="stat-value">{model.attempts}</span>
                      <span className="stat-label">Attempts</span>
                    </div>
                    <div className="stat-item">
                      <span 
                        className="stat-value stump-rate"
                        style={{ color: getStumpRateColor(model.stumpRate) }}
                      >
                        {model.stumpRate}%
                      </span>
                      <span className="stat-label">Stump Rate</span>
                    </div>
                  </div>

                  <div className="best-category">
                    <span className="category-label">Best Category:</span>
                    <span className="category-value">{model.bestCategory}</span>
                  </div>
                </div>

                <div className="recent-stumps">
                  <h4>Recent Stumps</h4>
                  <ul>
                    {model.recentStumps.map((stump, idx) => (
                      <li key={idx}>{stump}</li>
                    ))}
                  </ul>
                </div>
              </div>
            );
          })}
        </div>

        <div className="stump-info">
          <div className="info-section">
            <h3>How the Stump Tally Works</h3>
            <div className="info-grid">
              <div className="info-card">
                <div className="info-icon">🎯</div>
                <h4>Stump Scoring</h4>
                <p>When less than 50% of players solve a puzzle, it counts as a "stump" for the generating AI model.</p>
              </div>
              <div className="info-card">
                <div className="info-icon">⚖️</div>
                <h4>Fair Rotation</h4>
                <p>AI models take turns generating puzzles, ensuring equal opportunities to challenge players.</p>
              </div>
              <div className="info-card">
                <div className="info-icon">📊</div>
                <h4>Performance Tracking</h4>
                <p>Track stump rates by category to see which models excel at different types of challenges.</p>
              </div>
              <div className="info-card">
                <div className="info-icon">🔄</div>
                <h4>Dynamic Balance</h4>
                <p>Difficulty adjusts based on stump rate - too many stumps make tomorrow's puzzle easier.</p>
              </div>
            </div>
          </div>

          <div className="achievement-section">
            <h3>🏆 Current Champions</h3>
            <div className="champions">
              <div className="champion">
                <span className="champion-icon">🔥</span>
                <div className="champion-info">
                  <strong>Highest Stump Rate</strong>
                  <p>Claude-3 with {currentStats[0].stumpRate}% success rate</p>
                </div>
              </div>
              <div className="champion">
                <span className="champion-icon">🎯</span>
                <div className="champion-info">
                  <strong>Most Stumps</strong>
                  <p>{currentStats[0].model} with {currentStats[0].stumps} total stumps</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default StumpTally;