import { useState } from 'react';
import './App.css';

const initialBoard = Array(9).fill(null);

function App() {
  const [board, setBoard] = useState(initialBoard);
  const [status, setStatus] = useState('Your move');
  const [isGameOver, setIsGameOver] = useState(false);
  const [isLoading, setIsLoading] = useState(false); // Added missing state
  const [error, setError] = useState(null); // Added error state

  const handleClick = async (index) => {
    if (board[index] || isGameOver || isLoading) return; // Added isLoading check

    setIsLoading(true);
    setError(null); // Clear previous errors
    
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/move`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ board, index }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      // Check if response has expected structure
      if (!data.board || !data.status) {
        throw new Error('Invalid response format');
      }
      
      setBoard(data.board);
      setStatus(prettyStatus(data.status));
      if (data.status !== 'in_progress') setIsGameOver(true);
      
    } catch (error) {
      setError('Failed to make move. Please try again.');
      console.error('Move error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const prettyStatus = (s) => {
    switch (s) {
      case 'X_wins': return 'You win!';
      case 'O_wins': return 'Computer wins!';
      case 'draw': return "It's a draw!";
      default: return 'Your move';
    }
  };

  const resetGame = () => {
    setBoard(initialBoard);
    setStatus('Your move');
    setIsGameOver(false);
    setError(null);
  };

  return (
    <div className="container">
      <h1>Tic-Tac-Toe</h1>
      
      {/* Error message display */}
      {error && (
        <div className="error-message" role="alert">
          {error}
        </div>
      )}
      
      {/* Loading indicator */}
      {isLoading ? (
        <p className="status loading">Making move...</p>
      ) : (
        <p className="status">{status}</p>
      )}
      
      <div className="board">
        {board.map((cell, i) => (
          <button
            key={i}
            className={`cell ${cell === 'X' ? 'x' : cell === 'O' ? 'o' : ''} ${isLoading ? 'loading' : ''}`}
            onClick={() => handleClick(i)}
            disabled={!!cell || isGameOver || isLoading} // Added isLoading to disabled condition
          >
            {cell}
          </button>
        ))}
      </div>
      {isGameOver && (
        <button className="new-game-btn" onClick={resetGame} disabled={isLoading}>
          New Game
        </button>
      )}
    </div>
  );
}

export default App;
