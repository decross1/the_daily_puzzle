import { useState, useEffect } from 'react';
import { puzzleAPI } from '../services/api';

export const usePuzzle = () => {
  const [puzzle, setPuzzle] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [gameState, setGameState] = useState('playing'); // playing, solved, failed
  const [userAnswer, setUserAnswer] = useState('');

  // Fetch today's puzzle
  const fetchDailyPuzzle = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await puzzleAPI.getDailyPuzzle();
      if (response.data && response.data.question) {
        setPuzzle(response.data);
      } else {
        throw new Error('Invalid puzzle data received');
      }
    } catch (err) {
      console.log('API not ready, using mock data for development');
      // Fallback to mock data for development - this is expected until AI generation is implemented
      const useVisualArtDemo = true; // Force visual art demo for testing
      
      if (useVisualArtDemo) {
        console.log('Loading visual art puzzle demo');
        setPuzzle({
          id: new Date().toISOString().split('T')[0],
          category: 'art',
          difficulty: 0.65,
          generator_model: 'claude4',
          question: 'What compositional technique is demonstrated by the grid lines and red focal point?',
          solution: 'Rule of Thirds',
          interaction_type: 'multiple_choice',
          options: ['Rule of Thirds', 'Golden Ratio', 'Leading Lines', 'Symmetrical Balance'],
          visual_content: `<svg width="100%" height="300" viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg">
            <title>Rule of Thirds Grid</title>
            <rect width="100%" height="100%" fill="url(#skyGradient)"/>
            <rect y="400" width="100%" height="200" fill="url(#groundGradient)"/>
            <g stroke="#ffffff" stroke-width="2" opacity="0.7">
              <line x1="267" y1="0" x2="267" y2="600"/>
              <line x1="533" y1="0" x2="533" y2="600"/>
              <line x1="0" y1="200" x2="800" y2="200"/>
              <line x1="0" y1="400" x2="800" y2="400"/>
            </g>
            <g fill="#ff6b35" opacity="0.8">
              <circle cx="267" cy="200" r="8"/>
              <circle cx="533" cy="200" r="8"/>
              <circle cx="267" cy="400" r="8"/>
              <circle cx="533" cy="400" r="8"/>
            </g>
            <rect x="525" y="192" width="16" height="16" fill="#ff0000" opacity="0.9"/>
            <defs>
              <linearGradient id="skyGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" style="stop-color:#87CEEB"/>
                <stop offset="100%" style="stop-color:#E0F6FF"/>
              </linearGradient>
              <linearGradient id="groundGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" style="stop-color:#90EE90"/>
                <stop offset="100%" style="stop-color:#228B22"/>
              </linearGradient>
            </defs>
            <text x="400" y="30" text-anchor="middle" fill="white" font-size="20" font-weight="bold">Rule of Thirds Composition</text>
          </svg>`,
          media_url: null
        });
      } else {
        setPuzzle({
          id: new Date().toISOString().split('T')[0], // Today's date
          category: 'math',
          difficulty: 0.58,
          generator_model: 'claude4',
          question: 'Solve for x: 3x² + 7x - 20 = 0',
          solution: 'x = 5/3 or x = -4',
          media_url: null
        });
      }
      setError(null); // Clear error since fallback is working
    } finally {
      setLoading(false);
    }
  };

  // Submit answer
  const submitAnswer = async (answer) => {
    try {
      setUserAnswer(answer);
      const response = await puzzleAPI.submitAnswer(answer);
      setGameState(response.data.correct ? 'solved' : 'failed');
      return response.data;
    } catch (err) {
      console.error('Failed to submit answer:', err);
      // Fallback validation for development
      let isCorrect = false;
      if (puzzle && puzzle.interaction_type === 'multiple_choice') {
        isCorrect = answer === puzzle.solution;
      } else {
        isCorrect = answer.toLowerCase().includes('5/3') && answer.toLowerCase().includes('-4');
      }
      setGameState(isCorrect ? 'solved' : 'failed');
      return { correct: isCorrect };
    }
  };

  // Reset puzzle state
  const resetPuzzle = () => {
    setGameState('playing');
    setUserAnswer('');
  };

  // Load puzzle on mount
  useEffect(() => {
    fetchDailyPuzzle();
  }, []);

  return {
    puzzle,
    loading,
    error,
    gameState,
    userAnswer,
    submitAnswer,
    resetPuzzle,
    refetch: fetchDailyPuzzle
  };
};