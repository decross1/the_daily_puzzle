import React, { useState, useEffect } from 'react';
import './VisualArtPuzzle.css';

const VisualArtPuzzle = () => {
  const [puzzleData, setPuzzleData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [showSolution, setShowSolution] = useState(false);
  const [difficulty, setDifficulty] = useState(0.5);

  const generatePuzzle = async () => {
    setLoading(true);
    setSelectedAnswer(null);
    setShowSolution(false);
    
    try {
      const response = await fetch('/api/puzzle/visual-art/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          difficulty: difficulty,
          puzzle_type: 'auto'
        })
      });
      
      const data = await response.json();
      
      if (data.success) {
        setPuzzleData(data.puzzle);
      } else {
        console.error('Failed to generate puzzle:', data.error);
        alert('Failed to generate puzzle: ' + data.message);
      }
    } catch (error) {
      console.error('Error generating puzzle:', error);
      alert('Error generating puzzle: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleAnswer = (answer) => {
    setSelectedAnswer(answer);
    setShowSolution(true);
  };

  const getPuzzleOptions = (puzzleData) => {
    // Generate options based on puzzle type
    if (puzzleData.puzzle_type === 'color_theory') {
      return ['Red, Blue, Yellow', 'Red, Green, Blue', 'Yellow, Orange, Purple', 'Purple, Green, Orange'];
    } else if (puzzleData.puzzle_type === 'composition') {
      return ['On the intersection lines', 'In the center', 'Along the edges', 'In the corners'];
    } else if (puzzleData.puzzle_type === 'style_recognition') {
      return ['Impressionism', 'Cubism', 'Abstract Expressionism', 'Renaissance'];
    } else {
      // Fallback options
      return [puzzleData.solution, 'Option B', 'Option C', 'Option D'];
    }
  };

  const isCorrect = selectedAnswer === puzzleData?.solution;

  useEffect(() => {
    // Generate initial puzzle
    generatePuzzle();
  }, []);

  return (
    <div className="visual-art-puzzle-container">
      {/* Header Controls */}
      <div className="puzzle-controls">
        <h1>🎨 Visual Art Puzzle Generator</h1>
        
        <div className="control-panel">
          <div className="difficulty-control">
            <label>Difficulty: {difficulty.toFixed(1)}</label>
            <input
              type="range"
              min="0.1"
              max="0.9"
              step="0.1"
              value={difficulty}
              onChange={(e) => setDifficulty(parseFloat(e.target.value))}
              className="difficulty-slider"
            />
            <div className="difficulty-labels">
              <span>Mini</span>
              <span>Mid</span>
              <span>Beast</span>
            </div>
          </div>
          
          <button 
            onClick={generatePuzzle} 
            disabled={loading}
            className="generate-button"
          >
            {loading ? '🔄 Generating...' : '🎲 Generate New Puzzle'}
          </button>
        </div>
      </div>

      {/* Loading State */}
      {loading && (
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>🎨 Creating your visual art puzzle...</p>
          <p className="loading-detail">Using sophisticated difficulty calibration</p>
        </div>
      )}

      {/* Puzzle Content */}
      {puzzleData && !loading && (
        <div className="puzzle-content">
          {/* Puzzle Metadata */}
          <div className="puzzle-header">
            <div className="puzzle-meta">
              <span className="puzzle-id">ID: {puzzleData.id}</span>
              <span className="puzzle-type">Type: {puzzleData.puzzle_type}</span>
              <span className="difficulty-badge">
                Difficulty: {puzzleData.difficulty.toFixed(2)}
              </span>
              <span className="format-badge">
                Format: {puzzleData.puzzle_format}
              </span>
            </div>
          </div>

          {/* Visual Content - The Main Innovation */}
          {puzzleData.visual_content && (
            <div className="visual-content-container">
              <h3>🖼️ Interactive Visual</h3>
              <div 
                className="interactive-visual"
                dangerouslySetInnerHTML={{ __html: puzzleData.visual_content }}
              />
            </div>
          )}

          {/* Question Section */}
          <div className="question-section">
            <h3>❓ Question</h3>
            <p className="question-text">{puzzleData.question}</p>
          </div>

          {/* Interactive Answer Section */}
          <div className="answer-section">
            <h3>💭 Your Answer</h3>
            
            {puzzleData.interaction_type === 'multiple_choice' && (
              <div className="multiple-choice">
                {getPuzzleOptions(puzzleData).map((option, index) => (
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
                <p>👆 Click on the visual elements above that demonstrate the technique</p>
                <button 
                  className="submit-button"
                  onClick={() => handleAnswer(puzzleData.solution)}
                >
                  Submit Analysis
                </button>
              </div>
            )}

            {puzzleData.interaction_type === 'drag_drop_analysis' && (
              <div className="drag-drop">
                <p>🖱️ This would have draggable elements for complex analysis</p>
                <button 
                  className="submit-button"
                  onClick={() => handleAnswer(puzzleData.solution)}
                >
                  Submit Analysis
                </button>
              </div>
            )}
          </div>

          {/* Solution and Explanation */}
          {showSolution && (
            <div className={`solution-section ${isCorrect ? 'correct' : 'incorrect'}`}>
              <div className="result-indicator">
                {isCorrect ? '✅ Correct! Excellent!' : '❌ Not quite right'}
              </div>
              
              <div className="correct-answer">
                <strong>💡 Answer:</strong> {puzzleData.solution}
              </div>
              
              <div className="explanation">
                <strong>📖 Explanation:</strong>
                <p>{puzzleData.explanation}</p>
              </div>

              {puzzleData.hints && puzzleData.hints.length > 0 && (
                <div className="hints">
                  <strong>💭 Hints:</strong>
                  <ul>
                    {puzzleData.hints.map((hint, index) => (
                      <li key={index}>{hint}</li>
                    ))}
                  </ul>
                </div>
              )}

              {puzzleData.difficulty_justification && (
                <div className="difficulty-explanation">
                  <strong>🎯 Difficulty Analysis:</strong>
                  <p>{puzzleData.difficulty_justification}</p>
                </div>
              )}
            </div>
          )}

          {/* Educational Value */}
          <div className="educational-section">
            <h3>🎓 What You're Learning</h3>
            <div className="learning-content">
              {puzzleData.puzzle_type === 'color_theory' && (
                <div className="learning-points">
                  <h4>Color Theory Fundamentals:</h4>
                  <ul>
                    <li>🎨 Primary vs Secondary color relationships</li>
                    <li>🌈 Color harmonies and visual balance</li>
                    <li>👁️ How the eye perceives color mixing</li>
                    <li>🎯 Application in art and design</li>
                  </ul>
                </div>
              )}
              
              {puzzleData.puzzle_type === 'composition' && (
                <div className="learning-points">
                  <h4>Composition Principles:</h4>
                  <ul>
                    <li>📐 Rule of thirds and visual balance</li>
                    <li>➡️ Leading lines and eye movement</li>
                    <li>🎯 Focal points and visual hierarchy</li>
                    <li>⚖️ Symmetry and dynamic tension</li>
                  </ul>
                </div>
              )}
              
              {puzzleData.puzzle_type === 'style_recognition' && (
                <div className="learning-points">
                  <h4>Art Movement Knowledge:</h4>
                  <ul>
                    <li>🏛️ Historical context and development</li>
                    <li>🎨 Characteristic techniques and approaches</li>
                    <li>👥 Key artists and influences</li>
                    <li>🌍 Cultural and social impact</li>
                  </ul>
                </div>
              )}
            </div>
          </div>

          {/* Visual Elements Debug Info */}
          {puzzleData.visual_elements && Object.keys(puzzleData.visual_elements).length > 0 && (
            <details className="debug-section">
              <summary>🔧 Technical Details</summary>
              <div className="debug-content">
                <h4>Visual Elements:</h4>
                <pre>{JSON.stringify(puzzleData.visual_elements, null, 2)}</pre>
                
                <h4>Interaction Type:</h4>
                <p>{puzzleData.interaction_type}</p>
                
                <h4>Estimated Solve Time:</h4>
                <p>{puzzleData.estimated_solve_time} seconds</p>
              </div>
            </details>
          )}
        </div>
      )}

      {/* Benefits of Visual Puzzles */}
      <div className="benefits-section">
        <h2>🌟 Why Visual Art Puzzles?</h2>
        <div className="benefits-grid">
          <div className="benefit-card">
            <div className="benefit-icon">🖼️</div>
            <h3>Visual Learning</h3>
            <p>Learn art concepts through actual visual examples rather than just descriptions</p>
          </div>
          
          <div className="benefit-card">
            <div className="benefit-icon">🎯</div>
            <h3>Interactive Engagement</h3>
            <p>Click, explore, and interact with art elements for deeper understanding</p>
          </div>
          
          <div className="benefit-card">
            <div className="benefit-icon">📱</div>
            <h3>Mobile Friendly</h3>
            <p>SVG graphics scale perfectly across all devices and screen sizes</p>
          </div>
          
          <div className="benefit-card">
            <div className="benefit-icon">🎓</div>
            <h3>Educational Value</h3>
            <p>Actual art education with progressive difficulty, not just trivia</p>
          </div>
          
          <div className="benefit-card">
            <div className="benefit-icon">⚡</div>
            <h3>No External APIs</h3>
            <p>Core puzzles generated programmatically for reliability</p>
          </div>
          
          <div className="benefit-card">
            <div className="benefit-icon">🧠</div>
            <h3>Sophisticated AI</h3>
            <p>Claude-powered difficulty calibration with multi-dimensional scaling</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default VisualArtPuzzle;