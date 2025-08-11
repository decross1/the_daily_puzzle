import React, { useState } from 'react';
import PuzzleGame from './components/PuzzleGame';
import StatsModal from './components/StatsModal';
import InfoModal from './components/InfoModal';
import { usePuzzle } from './hooks/usePuzzle';
import './App.css';

function App() {
  const [showStats, setShowStats] = useState(false);
  const [showInfo, setShowInfo] = useState(false);
  const { puzzle, loading, error, gameState, userAnswer, submitAnswer } = usePuzzle();

  const getDifficultyTier = (difficulty) => {
    if (difficulty < 0.4) return { label: 'Mini', color: '#28a745' };
    if (difficulty < 0.7) return { label: 'Mid', color: '#ffc107' };
    return { label: 'Beast', color: '#dc3545' };
  };

  if (loading) {
    return (
      <div className="app-loading">
        <div className="loading-spinner"></div>
        <p>Loading today's puzzle...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="app-loading">
        <p>Error: {error}</p>
        <p>Using sample puzzle for development.</p>
      </div>
    );
  }

  if (!puzzle) {
    return (
      <div className="app-loading">
        <p>No puzzle available today.</p>
      </div>
    );
  }

  const difficultyTier = getDifficultyTier(puzzle.difficulty);

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1 className="app-title">The Daily Puzzle</h1>
          <div className="header-actions">
            <button 
              className="icon-button"
              onClick={() => setShowInfo(true)}
              aria-label="How to play"
            >
              ❓
            </button>
            <button 
              className="icon-button"
              onClick={() => setShowStats(true)}
              aria-label="Statistics"
            >
              📊
            </button>
          </div>
        </div>
      </header>

      <main className="app-main">
        <div className="puzzle-info">
          <div className="date-info">
            <span className="puzzle-date">{puzzle.id}</span>
            <span className="puzzle-number">Puzzle #{puzzle.id.replace(/-/g, '')}</span>
          </div>
          
          <div className="difficulty-info">
            <span 
              className="difficulty-badge"
              style={{ backgroundColor: difficultyTier.color }}
            >
              {difficultyTier.label}
            </span>
            <span className="generator-info">by {puzzle.generator_model}</span>
          </div>
        </div>

        <PuzzleGame
          puzzle={puzzle}
          gameState={gameState}
          userAnswer={userAnswer}
          onSubmitAnswer={submitAnswer}
        />
        
        {process.env.NODE_ENV === 'development' && (
          <div style={{ 
            textAlign: 'center', 
            padding: '1rem', 
            color: '#6b7280', 
            fontSize: '0.875rem',
            borderTop: '1px solid #e5e5e5',
            marginTop: '2rem'
          }}>
            🔧 Development Mode: Using sample puzzle data until AI generation is implemented
          </div>
        )}
      </main>

      {showStats && (
        <StatsModal
          isOpen={showStats}
          onClose={() => setShowStats(false)}
          puzzle={puzzle}
          gameState={gameState}
        />
      )}

      {showInfo && (
        <InfoModal
          isOpen={showInfo}
          onClose={() => setShowInfo(false)}
        />
      )}
    </div>
  );
}

export default App;