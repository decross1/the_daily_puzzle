import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Home from './pages/Home';
import Puzzle from './pages/Puzzle';
import Leaderboard from './pages/Leaderboard';
import StumpTally from './pages/StumpTally';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Header />
        <main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/puzzle" element={<Puzzle />} />
            <Route path="/leaderboard" element={<Leaderboard />} />
            <Route path="/stump-tally" element={<StumpTally />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;