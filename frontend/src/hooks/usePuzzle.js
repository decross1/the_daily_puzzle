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
      setPuzzle({
        id: new Date().toISOString().split('T')[0], // Today's date
        category: 'math',
        difficulty: 0.58,
        generator_model: 'claude-3',
        question: 'Solve for x: 3x² + 7x - 20 = 0',
        solution: 'x = 5/3 or x = -4',
        media_url: null
      });
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
      const isCorrect = answer.toLowerCase().includes('5/3') && answer.toLowerCase().includes('-4');
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