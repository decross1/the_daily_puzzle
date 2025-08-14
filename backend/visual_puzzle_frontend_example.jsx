/**
 * Visual Art Puzzle Frontend Component Example
 * 
 * Shows how the visual art puzzles would be rendered in the React frontend
 * with interactive elements and user engagement.
 */

import React, { useState } from 'react';

const VisualArtPuzzle = ({ puzzleData }) => {
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [showSolution, setShowSolution] = useState(false);

  const handleAnswer = (answer) => {
    setSelectedAnswer(answer);
    setShowSolution(true);
  };

  const isCorrect = selectedAnswer === puzzleData.solution;

  return (
    <div className="visual-art-puzzle">
      {/* Puzzle Header */}
      <div className="puzzle-header">
        <h2>🎨 Daily Art Puzzle</h2>
        <div className="puzzle-meta">
          <span className="difficulty">Difficulty: {puzzleData.difficulty}</span>
          <span className="type">Type: {puzzleData.puzzle_type}</span>
        </div>
      </div>

      {/* Visual Content - The Key Innovation */}
      <div className="visual-content-container">
        {puzzleData.visual_content && (
          <div 
            className="interactive-visual"
            dangerouslySetInnerHTML={{ __html: puzzleData.visual_content }}
          />
        )}
      </div>

      {/* Question */}
      <div className="question-section">
        <p className="question-text">{puzzleData.question}</p>
      </div>

      {/* Interactive Answer Section */}
      <div className="answer-section">
        {puzzleData.interaction_type === 'multiple_choice' && (
          <div className="multiple-choice">
            {['Red, Blue, Yellow', 'Red, Green, Blue', 'Yellow, Orange, Purple'].map((option, index) => (
              <button
                key={index}
                className={`choice-button ${selectedAnswer === option ? 'selected' : ''}`}
                onClick={() => handleAnswer(option)}
                disabled={showSolution}
              >
                {option}
              </button>
            ))}
          </div>
        )}

        {puzzleData.interaction_type === 'click_to_identify' && (
          <div className="click-interaction">
            <p>👆 Click on the visual elements that demonstrate the technique</p>
            <div className="visual-overlay">
              {/* Interactive overlay for clicking on visual elements */}
            </div>
          </div>
        )}

        {puzzleData.interaction_type === 'drag_drop_analysis' && (
          <div className="drag-drop">
            <p>🖱️ Drag the labels to the correct areas of the artwork</p>
            <div className="draggable-labels">
              <div className="label" draggable>Light Source</div>
              <div className="label" draggable>Shadow Area</div>
              <div className="label" draggable>Highlight</div>
            </div>
          </div>
        )}
      </div>

      {/* Solution and Explanation */}
      {showSolution && (
        <div className={`solution-section ${isCorrect ? 'correct' : 'incorrect'}`}>
          <div className="result-indicator">
            {isCorrect ? '✅ Correct!' : '❌ Not quite right'}
          </div>
          
          <div className="correct-answer">
            <strong>Answer:</strong> {puzzleData.solution}
          </div>
          
          <div className="explanation">
            <p><strong>Explanation:</strong> {puzzleData.explanation}</p>
          </div>

          {puzzleData.hints && (
            <div className="hints">
              <strong>Hints:</strong>
              <ul>
                {puzzleData.hints.map((hint, index) => (
                  <li key={index}>{hint}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {/* Educational Value Display */}
      <div className="educational-section">
        <h3>🎓 What You're Learning</h3>
        <div className="learning-points">
          {puzzleData.puzzle_type === 'color_theory' && (
            <ul>
              <li>Primary vs Secondary colors</li>
              <li>Color relationships and harmonies</li>
              <li>Visual color mixing principles</li>
            </ul>
          )}
          {puzzleData.puzzle_type === 'composition' && (
            <ul>
              <li>Rule of thirds composition</li>
              <li>Leading lines in artwork</li>
              <li>Visual balance and focal points</li>
            </ul>
          )}
          {puzzleData.puzzle_type === 'style_recognition' && (
            <ul>
              <li>Art movement characteristics</li>
              <li>Historical context and influence</li>
              <li>Technique identification</li>
            </ul>
          )}
        </div>
      </div>
    </div>
  );
};

// Example usage with different puzzle types
const App = () => {
  const [currentPuzzle, setCurrentPuzzle] = useState(0);
  
  const examplePuzzles = [
    {
      // Color Theory Puzzle
      puzzle_type: 'color_theory',
      difficulty: 0.2,
      question: 'Which colors are the PRIMARY colors in this color wheel?',
      solution: 'Red, Blue, Yellow',
      explanation: 'Primary colors cannot be created by mixing other colors. They are the foundation for all other colors.',
      hints: ['Think about colors that cannot be mixed from others', 'These are the starting point of the color wheel'],
      interaction_type: 'multiple_choice',
      visual_content: `<svg width="400" height="300"><!-- Color wheel SVG --></svg>`
    },
    {
      // Composition Puzzle  
      puzzle_type: 'composition',
      difficulty: 0.5,
      question: 'Where should the main subject be placed according to the Rule of Thirds?',
      solution: 'On the intersection lines',
      explanation: 'The Rule of Thirds divides an image into nine equal parts. Placing subjects at the intersection points creates more dynamic, visually interesting compositions.',
      hints: ['Look at the grid overlay', 'Notice where the lines intersect'],
      interaction_type: 'click_to_identify',
      visual_content: `<svg width="400" height="300"><!-- Rule of thirds grid SVG --></svg>`
    }
  ];

  return (
    <div className="app">
      <div className="puzzle-navigation">
        <button onClick={() => setCurrentPuzzle(0)}>Color Theory</button>
        <button onClick={() => setCurrentPuzzle(1)}>Composition</button>
      </div>
      
      <VisualArtPuzzle puzzleData={examplePuzzles[currentPuzzle]} />
      
      {/* Benefits Display */}
      <div className="benefits-section">
        <h2>🎨 Why Visual Art Puzzles?</h2>
        <div className="benefits-grid">
          <div className="benefit">
            <strong>🖼️ Visual Learning</strong>
            <p>Learn art concepts through actual visual examples</p>
          </div>
          <div className="benefit">
            <strong>🎯 Interactive Engagement</strong>
            <p>Click, drag, and explore rather than just read</p>
          </div>
          <div className="benefit">
            <strong>📱 Mobile Friendly</strong>
            <p>SVG graphics work perfectly on all devices</p>
          </div>
          <div className="benefit">
            <strong>🎓 Educational Value</strong>
            <p>Actual art education, not just trivia</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;

/* 
Enhanced CSS Styles for Visual Puzzles

.visual-art-puzzle {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Inter', sans-serif;
}

.puzzle-header {
  text-align: center;
  margin-bottom: 30px;
}

.puzzle-meta {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 10px;
}

.visual-content-container {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 20px;
  margin: 20px 0;
  text-align: center;
}

.interactive-visual svg {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
}

.question-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 20px;
  border-radius: 12px;
  margin: 20px 0;
}

.answer-section {
  margin: 20px 0;
}

.multiple-choice {
  display: grid;
  gap: 12px;
  max-width: 600px;
  margin: 0 auto;
}

.choice-button {
  padding: 15px 20px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 16px;
}

.choice-button:hover {
  border-color: #667eea;
  background: #f8f9ff;
}

.choice-button.selected {
  border-color: #667eea;
  background: #667eea;
  color: white;
}

.solution-section {
  padding: 20px;
  border-radius: 12px;
  margin: 20px 0;
}

.solution-section.correct {
  background: #d4edda;
  border: 1px solid #c3e6cb;
}

.solution-section.incorrect {
  background: #f8d7da;
  border: 1px solid #f5c6cb;
}

.educational-section {
  background: #fff3cd;
  border: 1px solid #ffeaa7;
  border-radius: 12px;
  padding: 20px;
  margin: 20px 0;
}

.benefits-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.benefit {
  padding: 15px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

@media (max-width: 768px) {
  .visual-art-puzzle {
    padding: 15px;
  }
  
  .benefits-grid {
    grid-template-columns: 1fr;
  }
}
*/