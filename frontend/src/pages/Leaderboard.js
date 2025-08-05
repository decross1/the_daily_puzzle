import React, { useState } from 'react';
import './Leaderboard.css';

function Leaderboard() {
  const [activeTab, setActiveTab] = useState('daily');

  // Mock leaderboard data
  const dailyLeaders = [
    { rank: 1, username: 'PuzzleMaster', solveTime: 47, streak: 12 },
    { rank: 2, username: 'QuickSolver', solveTime: 52, streak: 8 },
    { rank: 3, username: 'BrainTeaser', solveTime: 58, streak: 15 },
    { rank: 4, username: 'LogicLord', solveTime: 63, streak: 3 },
    { rank: 5, username: 'NumberNinja', solveTime: 67, streak: 7 },
    { rank: 6, username: 'ThinkFast', solveTime: 72, streak: 2 },
    { rank: 7, username: 'SolveIt', solveTime: 78, streak: 5 },
    { rank: 8, username: 'PuzzlePro', solveTime: 85, streak: 9 }
  ];

  const allTimeLeaders = [
    { rank: 1, username: 'BrainTeaser', totalSolved: 342, avgTime: 45, bestStreak: 28 },
    { rank: 2, username: 'PuzzleMaster', totalSolved: 298, avgTime: 38, bestStreak: 25 },
    { rank: 3, username: 'LogicLord', totalSolved: 267, avgTime: 52, bestStreak: 22 },
    { rank: 4, username: 'QuickSolver', totalSolved: 245, avgTime: 41, bestStreak: 19 },
    { rank: 5, username: 'NumberNinja', totalSolved: 223, avgTime: 48, bestStreak: 16 },
    { rank: 6, username: 'ThinkFast', totalSolved: 201, avgTime: 55, bestStreak: 14 },
    { rank: 7, username: 'SolveIt', totalSolved: 189, avgTime: 49, bestStreak: 12 },
    { rank: 8, username: 'PuzzlePro', totalSolved: 167, avgTime: 58, bestStreak: 11 }
  ];

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const getRankIcon = (rank) => {
    switch(rank) {
      case 1: return '🥇';
      case 2: return '🥈';
      case 3: return '🥉';
      default: return `#${rank}`;
    }
  };

  return (
    <div className="leaderboard-page">
      <div className="leaderboard-container">
        <div className="leaderboard-header">
          <h1>🏆 Leaderboard</h1>
          <p>See how you stack up against other puzzle solvers</p>
        </div>

        <div className="tabs">
          <button 
            className={`tab ${activeTab === 'daily' ? 'active' : ''}`}
            onClick={() => setActiveTab('daily')}
          >
            Today's Rankings
          </button>
          <button 
            className={`tab ${activeTab === 'alltime' ? 'active' : ''}`}
            onClick={() => setActiveTab('alltime')}
          >
            All-Time Leaders
          </button>
        </div>

        {activeTab === 'daily' && (
          <div className="leaderboard-content">
            <div className="leaderboard-info">
              <h3>Today's Fastest Solvers</h3>
              <p>Ranked by solve time for today's puzzle</p>
            </div>
            
            <div className="leaderboard-table">
              <div className="table-header">
                <div className="col-rank">Rank</div>
                <div className="col-username">Player</div>
                <div className="col-time">Solve Time</div>
                <div className="col-streak">Streak</div>
              </div>
              
              {dailyLeaders.map((player) => (
                <div key={player.rank} className={`table-row ${player.rank <= 3 ? 'podium' : ''}`}>
                  <div className="col-rank">
                    <span className="rank-icon">{getRankIcon(player.rank)}</span>
                  </div>
                  <div className="col-username">{player.username}</div>
                  <div className="col-time">{formatTime(player.solveTime)}</div>
                  <div className="col-streak">
                    <span className="streak-badge">{player.streak} days</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'alltime' && (
          <div className="leaderboard-content">
            <div className="leaderboard-info">
              <h3>Hall of Fame</h3>
              <p>All-time leaders based on total puzzles solved</p>
            </div>
            
            <div className="leaderboard-table">
              <div className="table-header">
                <div className="col-rank">Rank</div>
                <div className="col-username">Player</div>
                <div className="col-solved">Solved</div>
                <div className="col-avg">Avg Time</div>
                <div className="col-best">Best Streak</div>
              </div>
              
              {allTimeLeaders.map((player) => (
                <div key={player.rank} className={`table-row ${player.rank <= 3 ? 'podium' : ''}`}>
                  <div className="col-rank">
                    <span className="rank-icon">{getRankIcon(player.rank)}</span>
                  </div>
                  <div className="col-username">{player.username}</div>
                  <div className="col-solved">{player.totalSolved}</div>
                  <div className="col-avg">{formatTime(player.avgTime)}</div>
                  <div className="col-best">
                    <span className="streak-badge">{player.bestStreak} days</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="stats-cards">
          <div className="stat-card">
            <div className="stat-icon">🎯</div>
            <div className="stat-info">
              <h3>Today's Stats</h3>
              <p>87% solve rate</p>
              <p>156 players attempted</p>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">⚡</div>
            <div className="stat-info">
              <h3>Speed Record</h3>
              <p>32 seconds</p>
              <p>Set by PuzzleMaster</p>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">🔥</div>
            <div className="stat-info">
              <h3>Longest Streak</h3>
              <p>45 days</p>
              <p>Current leader: BrainTeaser</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Leaderboard;