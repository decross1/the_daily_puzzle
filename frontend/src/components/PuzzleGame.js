import React, { useState } from 'react';
import './PuzzleGame.css';

function PuzzleGame({ puzzle, gameState, userAnswer, onSubmitAnswer }) {
  const [currentAnswer, setCurrentAnswer] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (currentAnswer.trim()) {
      onSubmitAnswer(currentAnswer.trim());
    }
  };

  const getCategoryIcon = (category) => {
    switch (category) {
      case 'math': return '🔢';
      case 'word': return '📝';
      case 'art': return '🎨';
      default: return '🧩';
    }
  };

  return (
    <div className="puzzle-game">
      <div className="category-indicator">
        <span className="category-icon">{getCategoryIcon(puzzle.category)}</span>
        <span className="category-name">{puzzle.category.toUpperCase()}</span>
      </div>

      <div className="question-container">
        <div className="question-card">
          {puzzle.media_url && (
            <div className="media-container">
              <img src={puzzle.media_url} alt="Puzzle media" className="puzzle-media" />
            </div>
          )}
          <p className="question-text">{puzzle.question}</p>
        </div>
      </div>

      {gameState === 'playing' && (
        <form onSubmit={handleSubmit} className="answer-form">
          <div className="input-container">
            <input
              type="text"
              value={currentAnswer}
              onChange={(e) => setCurrentAnswer(e.target.value)}
              placeholder="Enter your answer..."
              className="answer-input"
              autoFocus
              maxLength={200}
            />
          </div>
          <button 
            type="submit" 
            className="submit-button"
            disabled={!currentAnswer.trim()}
          >
            Submit
          </button>
        </form>
      )}

      {gameState !== 'playing' && (
        <div className={`result-container ${gameState}`}>
          <div className="result-header">
            <div className="result-icon">
              {gameState === 'solved' ? '🎉' : '😔'}
            </div>
            <h2 className="result-title">
              {gameState === 'solved' ? 'Correct!' : 'Not quite!'}
            </h2>
          </div>

          <div className="answer-comparison">
            <div className="answer-row your-answer">
              <span className="answer-label">Your answer:</span>
              <span className="answer-value">{userAnswer}</span>
            </div>
            <div className="answer-row correct-answer">
              <span className="answer-label">Correct answer:</span>
              <span className="answer-value">{puzzle.solution}</span>
            </div>
          </div>

          {gameState === 'solved' && (
            <div className="success-message">
              <p>🌟 Great job! You solved today's puzzle!</p>
              <p>Come back tomorrow for a new challenge.</p>
            </div>
          )}

          {gameState === 'failed' && (
            <div className="failure-message">
              <p>Don't worry! Try again tomorrow.</p>
              <p>The AI got you this time, but keep practicing!</p>
            </div>
          )}

          <div className="next-puzzle-info">
            <p className="next-puzzle-text">
              Next puzzle in: <span className="countdown">23:42:15</span>
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

export default PuzzleGame;