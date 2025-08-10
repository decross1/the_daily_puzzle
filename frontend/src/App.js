import React, { useState, useEffect } from 'react';
import PuzzleGame from './components/PuzzleGame';
import StatsModal from './components/StatsModal';
import InfoModal from './components/InfoModal';
import './App.css';

function App() {
  const [showStats, setShowStats] = useState(false);
  const [showInfo, setShowInfo] = useState(false);
  const [puzzle, setPuzzle] = useState(null);
  const [gameState, setGameState] = useState('playing'); // playing, solved, failed
  const [userAnswer, setUserAnswer] = useState('');

  // Mock puzzle data - will be replaced with API call
  useEffect(() => {
    setPuzzle({
      id: '2025-08-10',
      category: 'math',
      difficulty: 0.58,
      generator_model: 'claude-3',
      question: 'Solve for x: 3x² + 7x - 20 = 0',
      solution: 'x = 5/3 or x = -4',
      media_url: null
    });
  }, []);

  const handleSubmitAnswer = (answer) => {
    setUserAnswer(answer);
    // Mock validation - will be replaced with API call
    const isCorrect = answer.toLowerCase().includes('5/3') && answer.toLowerCase().includes('-4');
    setGameState(isCorrect ? 'solved' : 'failed');
  };

  const getDifficultyTier = (difficulty) => {
    if (difficulty < 0.4) return { label: 'Mini', color: '#28a745' };
    if (difficulty < 0.7) return { label: 'Mid', color: '#ffc107' };
    return { label: 'Beast', color: '#dc3545' };
  };

  if (!puzzle) {
    return (
      <div className="app-loading">
        <div className="loading-spinner"></div>
        <p>Loading today's puzzle...</p>
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
          onSubmitAnswer={handleSubmitAnswer}
        />
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