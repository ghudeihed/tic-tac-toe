import { useState } from 'react';
import './App.css';

const initialBoard = Array(9).fill(null);

function App() {
  const [board, setBoard] = useState(initialBoard);
  const [status, setStatus] = useState('Your move');
  const [isGameOver, setIsGameOver] = useState(false);

  const handleClick = async (index) => {
    if (board[index] || isGameOver) return;

    const response = await fetch(`${import.meta.env.VITE_API_URL}/move`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ board, index }),
    });

    const data = await response.json();
    setBoard(data.board);
    setStatus(prettyStatus(data.status));
    if (data.status !== 'in_progress') setIsGameOver(true);
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
  };

  return (
    <div className="container">
      <h1>Tic-Tac-Toe</h1>
      <p className="status">{status}</p>
      <div className="board">
        {board.map((cell, i) => (
          <button
            key={i}
            className={`cell ${cell === 'X' ? 'x' : cell === 'O' ? 'o' : ''}`}
            onClick={() => handleClick(i)}
            disabled={!!cell || isGameOver}
          >
            {cell}
          </button>
        ))}
      </div>
      {isGameOver && (
        <button className="new-game-btn" onClick={resetGame}>
          New Game
        </button>
      )}
    </div>
  );
}

export default App;
