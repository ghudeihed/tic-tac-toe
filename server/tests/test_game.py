import pytest
from game import TicTacToeGame
from config import Config


class TestWinDetection:
    """Test cases for win pattern detection."""
    
    def test_check_winner_row_wins(self, game, sample_boards):
        """Test winner detection for all row combinations."""
        winning_boards = [
            sample_boards['top_row_win'],
            sample_boards['middle_row_win'],
            sample_boards['bottom_row_win'],
        ]
        
        for board in winning_boards:
            assert game.check_winner(board, 'X') == True
            assert game.check_winner(board, 'O') == False

    def test_check_winner_column_wins(self, game, sample_boards):
        """Test winner detection for all column combinations."""
        winning_boards = [
            sample_boards['left_column_win'],
            sample_boards['middle_column_win'],
            sample_boards['right_column_win'],
        ]
        
        for board in winning_boards:
            assert game.check_winner(board, 'X') == True
            assert game.check_winner(board, 'O') == False

    def test_check_winner_diagonal_wins(self, game, sample_boards):
        """Test winner detection for diagonal combinations."""
        winning_boards = [
            sample_boards['main_diagonal_win'],
            sample_boards['anti_diagonal_win'],
        ]
        
        for board in winning_boards:
            assert game.check_winner(board, 'X') == True
            assert game.check_winner(board, 'O') == False

    def test_check_winner_no_win(self, game, sample_boards):
        """Test that no winner is detected when there shouldn't be one."""
        no_win_boards = [
            sample_boards['empty'],
            sample_boards['game_in_progress'],
            sample_boards['almost_win_but_not_quite'],
        ]
        
        for board in no_win_boards:
            assert game.check_winner(board, 'X') == False
            assert game.check_winner(board, 'O') == False

    def test_check_winner_computer_wins(self, game, sample_boards):
        """Test winner detection for computer (O) wins."""
        computer_win_boards = [
            sample_boards['computer_row_win'],
            sample_boards['computer_column_win'],
            sample_boards['computer_diagonal_win'],
        ]
        
        for board in computer_win_boards:
            assert game.check_winner(board, 'O') == True
            assert game.check_winner(board, 'X') == False

class TestDrawDetection:
    """Test cases for draw detection."""
    
    def test_is_draw_full_board(self, game, sample_boards):
        """Test draw detection on completely full board."""
        assert game.is_draw(sample_boards['full_draw_board']) == True

    def test_is_draw_not_full(self, game, sample_boards):
        """Test that draw is not detected on incomplete board."""
        incomplete_boards = [
            sample_boards['empty'],
            sample_boards['game_in_progress'],
            sample_boards['almost_full_board'],
        ]
        
        for board in incomplete_boards:
            assert game.is_draw(board) == False

    def test_is_draw_mixed_scenarios(self, game, sample_boards):
        """Test draw detection with various board states."""
        assert game.is_draw(sample_boards['all_x_board']) == True
        assert game.is_draw(sample_boards['all_o_board']) == True
        assert game.is_draw(sample_boards['alternating_full_board']) == True
        assert game.is_draw(sample_boards['one_empty_at_start']) == False
        assert game.is_draw(sample_boards['one_empty_at_end']) == False

class TestComputerStrategy:
    """Test cases for computer move strategy."""
    
    def test_computer_chooses_center_when_available(self, game, sample_boards):
        """Test computer prioritizes center position."""
        center_available_boards = [
            sample_boards['empty'],
            sample_boards['center_free_with_x'],
            sample_boards['center_free_with_x_o'],
        ]
        
        for board in center_available_boards:
            move = game.get_computer_move(board)
            assert move == 4

    def test_computer_chooses_corner_when_center_taken(self, game, sample_boards):
        """Test computer prioritizes corners when center is occupied."""
        center_taken_boards = [
            sample_boards['center_taken'],
            sample_boards['center_taken_by_o'],
            sample_boards['center_taken_some_corners'],
        ]
        
        for board in center_taken_boards:
            move = game.get_computer_move(board)
            assert move in [0, 2, 6, 8]

    def test_computer_chooses_side_when_center_and_corners_taken(self, game, sample_boards):
        """Test computer chooses sides when center and all corners are taken."""
        board = sample_boards['all_corners_center_taken']
        move = game.get_computer_move(board)
        assert move in [1, 3, 5, 7]

    def test_computer_strategy_priority_order(self, game, sample_boards):
        """Test that computer follows correct priority: center -> corners -> sides."""
        
        board = sample_boards['center_taken_by_o']
        move = game.get_computer_move(board)
        assert move in [0, 2, 6, 8]
        
        board = sample_boards['all_corners_center_taken']
        move = game.get_computer_move(board)
        assert move in [1, 3, 5, 7]

    def test_computer_no_moves_available(self, game, sample_boards):
        """Test computer behavior when no moves are available."""
        move = game.get_computer_move(sample_boards['full_board_no_moves'])
        assert move is None

    def test_computer_chooses_available_corner(self, game, sample_boards):
        """Test computer chooses available corner when some are taken."""
        board = sample_boards['corners_0_2_taken']
        move = game.get_computer_move(board)
        assert move in [6, 8]

    def test_computer_chooses_available_side(self, game, sample_boards):
        """Test computer chooses available side when some are taken."""
        board = sample_boards['corners_center_sides_partial']
        move = game.get_computer_move(board)
        assert move in [3, 5]

class TestGameLogicIntegration:
    """Integration tests for game logic components."""
    
    def test_win_patterns_match_config(self, game, sample_boards):
        """Test that win detection uses correct patterns from config."""
        for pattern in Config.WIN_PATTERNS:
            board = sample_boards['empty'].copy()
            for pos in pattern:
                board[pos] = 'X'
            
            assert game.check_winner(board, 'X') == True
            assert game.check_winner(board, 'O') == False

    def test_board_size_consistency(self, game, sample_boards):
        """Test that all functions work with config board size."""
        board = sample_boards['empty']
        
        assert game.check_winner(board, 'X') == False
        assert game.is_draw(board) == False
        
        move = game.get_computer_move(board)
        assert move is not None
        assert 0 <= move < Config.BOARD_SIZE

    def test_game_state_transitions(self, game, sample_boards):
        """Test logical game state transitions."""
        board = sample_boards['empty'].copy()
        assert not game.check_winner(board, 'X')
        assert not game.check_winner(board, 'O')
        assert not game.is_draw(board)
        
        # Add some moves
        board[0] = 'X'
        board[4] = 'O'
        assert not game.check_winner(board, 'X')
        assert not game.check_winner(board, 'O')
        assert not game.is_draw(board)
        
        # Create winning condition
        board[1] = 'X'
        board[2] = 'X'
        assert game.check_winner(board, 'X')
        assert not game.check_winner(board, 'O')


    def test_computer_move_validity(self, game, sample_boards):
        """Test that computer always chooses valid moves."""
        test_boards = [
            sample_boards['empty'],
            sample_boards['game_in_progress'],
            sample_boards['center_taken'],
            sample_boards['many_moves_board'],
        ]
        
        for board in test_boards:
            move = game.get_computer_move(board)
            if move is not None:
                assert 0 <= move <= 8
                assert board[move] is None

class TestEdgeCases:
    """Test cases for edge cases and boundary conditions."""
    
    def test_single_move_scenarios(self, game, sample_boards):
        """Test scenarios with only one move made."""
        for i in range(9):
            board = sample_boards['empty'].copy()
            board[i] = 'X'
            
            assert not game.check_winner(board, 'X')
            assert not game.check_winner(board, 'O')
            assert not game.is_draw(board)
            
            move = game.get_computer_move(board)
            assert move is not None
            assert board[move] is None

    def test_almost_full_board_scenarios(self, game, sample_boards):
        """Test scenarios with board almost full."""
        # Leave only one empty spot
        for empty_pos in range(9):
            board = sample_boards['alternating_full_board'].copy()
            board[empty_pos] = None
            
            move = game.get_computer_move(board)
            if move is not None:
                assert move == empty_pos
            
            # Test draw detection
            board[empty_pos] = 'O'
            assert game.is_draw(board) == True

class TestMoveValidation:
    """Test cases for move validation logic."""
    
    def test_validate_move_valid_moves(self, game, empty_board):
        """Test validation of valid moves."""
        board = empty_board
        
        for i in range(9):
            is_valid, error = game.validate_move(board, i)
            assert is_valid == True
            assert error is None

    def test_validate_move_invalid_board(self, game):
        """Test validation with invalid board."""
        # None board
        is_valid, error = game.validate_move(None, 0)
        assert is_valid == False
        assert "Board data required" in error
        
        # Empty list
        is_valid, error = game.validate_move([], 0)
        assert is_valid == False
        assert "Board data required" in error

    def test_validate_move_wrong_board_size(self, game):
        """Test validation with wrong board size."""
        # Too small
        is_valid, error = game.validate_move([None] * 5, 0)
        assert is_valid == False
        assert "Invalid board size" in error
        
        # Too large
        is_valid, error = game.validate_move([None] * 12, 0)
        assert is_valid == False
        assert "Invalid board size" in error

    def test_validate_move_invalid_index(self, game, sample_boards):
        """Test validation with invalid move indices."""
        board = sample_boards['empty'].copy()
        
        # None index
        is_valid, error = game.validate_move(board, None)
        assert is_valid == False
        assert "Invalid move index" in error
        
        # Negative index
        is_valid, error = game.validate_move(board, -1)
        assert is_valid == False
        assert "Invalid move index" in error
        
        # Too large index
        is_valid, error = game.validate_move(board, 9)
        assert is_valid == False
        assert "Invalid move index" in error

    def test_validate_move_occupied_position(self, game, sample_boards):
        """Test validation with occupied positions."""
        board = sample_boards['x_at_0_o_at_4']
        
        # Position 0 occupied by X
        is_valid, error = game.validate_move(board, 0)
        assert is_valid == False
        assert "Position 0 already occupied" in error
        
        # Position 4 occupied by O
        is_valid, error = game.validate_move(board, 4)
        assert is_valid == False
        assert "Position 4 already occupied" in error
        
        # Position 1 is free
        is_valid, error = game.validate_move(board, 1)
        assert is_valid == True
        assert error is None