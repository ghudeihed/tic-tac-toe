# game.py
from config import Config, logger

class TicTacToeGame:
    def __init__(self):
        self.board_size = Config.BOARD_SIZE
        self.win_patterns = Config.WIN_PATTERNS
    
    def check_winner(self, board, player):
        """Check if a player has won the game."""
        return any(all(board[i] == player for i in pattern) for pattern in self.win_patterns)
    
    def is_draw(self, board):
        """Check if the game is a draw."""
        return all(cell is not None for cell in board)
    
    def get_computer_move(self, board):
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
    
    def validate_move(self, board, index):
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