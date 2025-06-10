from typing import List, Optional
from config import Config, logger

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
    
    def get_computer_move(self, board: List[Optional[str]]) -> Optional[int]:
        opponent = self.human_symbol
        player = self.computer_symbol
        available = self.get_available_moves(board)
        
        logger.debug(f"Computer evaluating {len(available)} available moves: {available}")
        
        # 1. Win
        for move in available:
            if self.check_winner(self.make_move(board, move, player), player):
                logger.info(f"Computer winning game with move at position {move}")
                return move
        
        # 2. Block
        for move in available:
            if self.check_winner(self.make_move(board, move, opponent), opponent):
                logger.info(f"Computer blocking opponent win at position {move}")
                return move
        
        # 3. Fork
        for move in available:
            new_board = self.make_move(board, move, player)
            win_count = sum(
                self.check_winner(self.make_move(new_board, m, player), player)
                for m in self.get_available_moves(new_board)
            )
            if win_count >= 2:
                logger.info(f"Computer creating fork at position {move} (creates {win_count} winning opportunities)")
                return move
        
        # 4. Block Fork
        for move in available:
            new_board = self.make_move(board, move, opponent)
            win_count = sum(
                self.check_winner(self.make_move(new_board, m, opponent), opponent)
                for m in self.get_available_moves(new_board)
            )
            if win_count >= 2:
                logger.info(f"Computer blocking opponent fork at position {move}")
                return move
        
        # 5. Center
        if board[4] is None:
            logger.info("Computer choosing center position 4")
            return 4
        
        # 6. Opposite Corner
        corners = [(0, 8), (2, 6)]
        for a, b in corners:
            if board[a] == opponent and board[b] is None:
                logger.info(f"Computer choosing opposite corner {b} to opponent at {a}")
                return b
            if board[b] == opponent and board[a] is None:
                logger.info(f"Computer choosing opposite corner {a} to opponent at {b}")
                return a
        
        # 7. Empty Corner
        for i in [0, 2, 6, 8]:
            if board[i] is None:
                logger.info(f"Computer choosing corner position {i}")
                return i
        
        # 8. Empty Side
        for i in [1, 3, 5, 7]:
            if board[i] is None:
                logger.info(f"Computer choosing side position {i}")
                return i
        
        logger.warning("No available moves for computer")
        return None
    
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