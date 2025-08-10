import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './Header.css';

function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const closeMenu = () => {
    setIsMenuOpen(false);
  };

  return (
    <header className="header">
      <div className="header-container">
        <Link to="/" className="logo" onClick={closeMenu}>
          <h1>🧩 Daily Puzzle</h1>
        </Link>
        
        <button 
          className={`menu-toggle ${isMenuOpen ? 'active' : ''}`}
          onClick={toggleMenu}
          aria-label="Toggle navigation menu"
        >
          <span></span>
          <span></span>
          <span></span>
        </button>

        <nav className={`nav ${isMenuOpen ? 'nav-open' : ''}`}>
          <Link to="/" className="nav-link" onClick={closeMenu}>
            <span className="nav-icon">🏠</span>
            Home
          </Link>
          <Link to="/puzzle" className="nav-link" onClick={closeMenu}>
            <span className="nav-icon">🧩</span>
            Puzzle
          </Link>
          <Link to="/leaderboard" className="nav-link" onClick={closeMenu}>
            <span className="nav-icon">🏆</span>
            Leaderboard
          </Link>
          <Link to="/stump-tally" className="nav-link" onClick={closeMenu}>
            <span className="nav-icon">🏴‍☠️</span>
            Stump Tally
          </Link>
        </nav>
      </div>
      {isMenuOpen && <div className="nav-backdrop" onClick={closeMenu}></div>}
    </header>
  );
}

export default Header;