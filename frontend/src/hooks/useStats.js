import { useState, useEffect } from 'react';
import { statsAPI } from '../services/api';

export const useStats = () => {
  const [playerStats, setPlayerStats] = useState(null);
  const [stumpTally, setStumpTally] = useState([]);
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Mock data for development
  const mockPlayerStats = {
    totalPlayed: 42,
    winRate: 73,
    currentStreak: 5,
    maxStreak: 12,
    averageTime: 127,
    categoryStats: {
      math: { played: 15, won: 11 },
      word: { played: 14, won: 10 },
      art: { played: 13, won: 9 }
    }
  };

  const mockStumpTally = [
    { model: 'claude4', stumps: 12, total: 28, rate: 43 },
    { model: 'gpt5', stumps: 8, total: 25, rate: 32 },
    { model: 'gemini', stumps: 6, total: 22, rate: 27 }
  ];

  // Fetch all stats data
  const fetchStats = async () => {
    try {
      setLoading(true);
      setError(null);

      const [playerResponse, stumpResponse] = await Promise.allSettled([
        statsAPI.getPlayerStats(),
        statsAPI.getStumpTally()
      ]);

      if (playerResponse.status === 'fulfilled') {
        setPlayerStats(playerResponse.value.data);
      } else {
        console.error('Failed to fetch player stats:', playerResponse.reason);
        setPlayerStats(mockPlayerStats);
      }

      if (stumpResponse.status === 'fulfilled') {
        setStumpTally(stumpResponse.value.data);
      } else {
        console.error('Failed to fetch stump tally:', stumpResponse.reason);
        setStumpTally(mockStumpTally);
      }

    } catch (err) {
      console.error('Failed to fetch stats:', err);
      setError('Failed to load statistics');
      // Use mock data as fallback
      setPlayerStats(mockPlayerStats);
      setStumpTally(mockStumpTally);
    } finally {
      setLoading(false);
    }
  };

  // Fetch leaderboard
  const fetchLeaderboard = async () => {
    try {
      const response = await statsAPI.getLeaderboard();
      setLeaderboard(response.data);
    } catch (err) {
      console.error('Failed to fetch leaderboard:', err);
      // Mock leaderboard data
      setLeaderboard([
        { rank: 1, username: 'PuzzleMaster', wins: 45, streak: 12 },
        { rank: 2, username: 'BrainTeaser', wins: 42, streak: 8 },
        { rank: 3, username: 'LogicLord', wins: 38, streak: 6 }
      ]);
    }
  };

  useEffect(() => {
    fetchStats();
    fetchLeaderboard();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return {
    playerStats,
    stumpTally,
    leaderboard,
    loading,
    error,
    refetch: fetchStats
  };
};