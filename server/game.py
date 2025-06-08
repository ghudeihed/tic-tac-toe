from typing import Optional
from config import Config, logger

class TicTacToeGame:
    def __init__(self):
        self.board_size = Config.BOARD_SIZE
        self.win_patterns = Config.WIN_PATTERNS
        self.computer_symbol = 'O'
        self.human_symbol = 'X'
    
    def check_winner(self, board: list[Optional[str]], player: str) -> bool:
        """Check if a player has won the game."""
        try:
            return any(all(board[i] == player for i in pattern) for pattern in self.win_patterns)
        except Exception as e:
            logger.error(f"Error checking winner: {str(e)}")
            return False
    
    def is_draw(self, board: list[Optional[str]]) -> bool:
        """Check if the game is a draw."""
        try:
            return all(cell is not None for cell in board) and not self.check_winner(board, self.computer_symbol) and not self.check_winner(board, self.human_symbol)
        except TypeError as e:
            logger.error(f"Error checking draw: {str(e)}")
            return False
    
    def get_computer_move(self, board: list[Optional[str]]) -> Optional[int]:
        """Get the computer's next move using simple strategy."""
        # Prioritize center
        if board[4] is None:
            logger.info("Computer choosing center position")
            return 4
        
        # Prioritize corners
        for i in [0, 2, 6, 8]:
            if board[i] is None:
                logger.info(f"Computer choosing corner position {i}")
                return i
        
        # Then sides
        for i in [1, 3, 5, 7]:
            if board[i] is None:
                logger.info(f"Computer choosing side position {i}")
                return i
        
        logger.warning("No available moves for computer")
        return None
    
    def validate_move(self, board: list[Optional[str]], index: Optional[int]) -> tuple[bool, Optional[str]]:
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