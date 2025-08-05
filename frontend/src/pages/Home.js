import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css';

function Home() {
  return (
    <div className="home">
      <section className="hero">
        <div className="hero-content">
          <h1>Welcome to The Daily Puzzle</h1>
          <p className="hero-subtitle">
            AI models compete to stump human players with daily challenges across Math, Word, and Art puzzles
          </p>
          <div className="hero-stats">
            <div className="stat">
              <span className="stat-number">0.58</span>
              <span className="stat-label">Difficulty Level</span>
            </div>
            <div className="stat">
              <span className="stat-number">Mid</span>
              <span className="stat-label">Challenge Tier</span>
            </div>
            <div className="stat">
              <span className="stat-number">Claude-3</span>
              <span className="stat-label">Today's Generator</span>
            </div>
          </div>
          <Link to="/puzzle" className="cta-button">
            Solve Today's Puzzle
          </Link>
        </div>
      </section>

      <section className="features">
        <div className="features-container">
          <h2>How It Works</h2>
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">🤖</div>
              <h3>AI Generated</h3>
              <p>Different AI models take turns creating puzzles designed to challenge human players</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">📊</div>
              <h3>Dynamic Difficulty</h3>
              <p>Puzzle difficulty adjusts based on community performance - harder when solved, easier when stumped</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🏆</div>
              <h3>Daily Competition</h3>
              <p>24-hour solve window with leaderboards tracking speed and consistency</p>
            </div>
          </div>
        </div>
      </section>

      <section className="categories">
        <div className="categories-container">
          <h2>Puzzle Categories</h2>
          <div className="categories-grid">
            <div className="category-card">
              <div className="category-icon">🔢</div>
              <h3>Math Puzzles</h3>
              <p>Algebra, physics problems, number theory, and geometry challenges</p>
            </div>
            <div className="category-card">
              <div className="category-icon">📝</div>
              <h3>Word Puzzles</h3>
              <p>Riddles, word searches, anagrams, and clever wordplay challenges</p>
            </div>
            <div className="category-card">
              <div className="category-icon">🎨</div>
              <h3>Art Puzzles</h3>
              <p>Music identification, visual recognition, and creative challenges</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

export default Home;