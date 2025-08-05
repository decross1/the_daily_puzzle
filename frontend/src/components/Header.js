import React from 'react';
import { Link } from 'react-router-dom';
import './Header.css';

function Header() {
  return (
    <header className="header">
      <div className="header-container">
        <Link to="/" className="logo">
          <h1>🧩 The Daily Puzzle</h1>
        </Link>
        <nav className="nav">
          <Link to="/" className="nav-link">Home</Link>
          <Link to="/puzzle" className="nav-link">Today's Puzzle</Link>
          <Link to="/leaderboard" className="nav-link">Leaderboard</Link>
          <Link to="/stump-tally" className="nav-link">Stump Tally</Link>
        </nav>
      </div>
    </header>
  );
}

export default Header;