import { useState } from 'react';
import './App.css';

const EMPTY_BOARD = Array(9).fill(null);

function App() {
  const [board, setBoard] = useState(EMPTY_BOARD);
  const [status, setStatus] = useState("Your turn");

  const handleClick = async (index) => {
    if (board[index] !== null) return;

    try {
      const response = await fetch("http://localhost:5000/move", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ board, index }),
      });

      const data = await response.json();
      if (data.board) {
        setBoard(data.board);
        setStatus("Your turn"); // Will improve later to show win/draw
      } else if (data.error) {
        setStatus("Invalid move.");
      }
    } catch (err) {
      console.error("Error:", err);
      setStatus("Server error.");
    }
  };

  const renderCell = (i) => (
    <div className="cell" onClick={() => handleClick(i)}>
      {board[i]}
    </div>
  );

  return (
    <div className="app">
      <h1>Tic-Tac-Toe</h1>
      <p>{status}</p>
      <div className="board">
        {board.map((_, i) => renderCell(i))}
      </div>
    </div>
  );
}

export default App;
