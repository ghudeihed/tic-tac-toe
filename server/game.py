from typing import List, Optional
from config.config import Config, logger

class TicTacToeGame:
    def __init__(self):
        self.board_size = Config.BOARD_SIZE
        self.win_patterns = Config.WIN_PATTERNS
        self.computer_symbol = 'O'
        self.human_symbol = 'X'
    
    def check_winner(self, board: List[Optional[str]], player: str) -> bool:
        """Check if a player has won the game."""
        try:
            return any(all(board[i] == player for i in pattern) for pattern in self.win_patterns)
        except Exception as e:
            logger.error(f"Error checking winner: {str(e)}")
            return False
    
    def is_draw(self, board: List[Optional[str]]) -> bool:
        """Check if the game is a draw."""
        try:
            return all(cell is not None for cell in board) and not self.check_winner(board, self.computer_symbol) and not self.check_winner(board, self.human_symbol)
        except TypeError as e:
            logger.error(f"Error checking draw: {str(e)}")
            return False
    
    def get_available_moves(self, board: List[Optional[str]]) -> List[int]:
        """Get all available moves on the board."""
        return [i for i in range(len(board)) if board[i] is None]
    
    def make_move(self, board: List[Optional[str]], position: int, player: str) -> List[Optional[str]]:
        """Make a move on the board and return a new board state."""
        new_board = board.copy()
        new_board[position] = player
        return new_board
    def minimax(self, board: List[Optional[str]], is_maximizing: bool) -> int:
        if self.check_winner(board, self.computer_symbol):
            return 1
        if self.check_winner(board, self.human_symbol):
            return -1
        if self.is_draw(board):
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for move in self.get_available_moves(board):
                new_board = self.make_move(board, move, self.computer_symbol)
                score = self.minimax(new_board, False)
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for move in self.get_available_moves(board):
                new_board = self.make_move(board, move, self.human_symbol)
                score = self.minimax(new_board, True)
                best_score = min(score, best_score)
            return best_score
    
    def get_computer_move(self, board: List[Optional[str]]) -> Optional[int]:
        best_score = -float('inf')
        best_move = None
        for move in self.get_available_moves(board):
            new_board = self.make_move(board, move, self.computer_symbol)
            score = self.minimax(new_board, False)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move
    
    def validate_move(self, board: List[Optional[str]], index: Optional[int]) -> tuple[bool, Optional[str]]:
        """Validate if a move is legal."""
        if not board:
            return False, "Board data required"
        
        if len(board) != self.board_size:
            return False, f"Invalid board size: {len(board)}"
        
        if index is None or index < 0 or index >= self.board_size:
            return False, f"Invalid move index: {index}"
        
        if board[index] is not None:
            return False, f"Position {index} already occupied"
        
        return True, None