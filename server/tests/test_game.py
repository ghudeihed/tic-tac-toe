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
        assert game.is_draw(sample_boards['all_x_board']) == False
        assert game.is_draw(sample_boards['all_o_board']) == False
        assert game.is_draw(sample_boards['alternating_full_board']) == False
        assert game.is_draw(sample_boards['one_empty_at_start']) == False
        assert game.is_draw(sample_boards['one_empty_at_end']) == False

class TestComputerStrategy:
    """Test cases for computer move strategy - comprehensive coverage."""
    
    # ========== WIN STRATEGY TESTS (Priority 1) ==========
    
    def test_computer_takes_winning_move_rows(self, game):
        """Test computer takes winning moves in all rows."""
        # Top row win
        board = ['O', 'O', None, 'X', 'X', None, None, None, None]
        move = game.get_computer_move(board)
        assert move == 2
        
        # Middle row win
        board = [None, None, None, 'O', 'O', None, 'X', 'X', None]
        move = game.get_computer_move(board)
        assert move == 5
        
        # Bottom row win
        board = ['X', None, None, None, None, None, 'O', 'O', None]
        move = game.get_computer_move(board)
        assert move == 8

    def test_computer_takes_winning_move_columns(self, game):
        """Test computer takes winning moves in all columns."""
        # Left column win
        board = ['O', 'X', None, 'O', 'X', None, None, None, None]
        move = game.get_computer_move(board)
        assert move == 6
        
        # Middle column win
        board = [None, 'O', None, None, 'O', None, 'X', None, 'X']
        move = game.get_computer_move(board)
        assert move == 7
        
        # Right column win
        board = [None, None, 'O', None, 'X', 'O', None, 'X', None]
        move = game.get_computer_move(board)
        assert move == 8

    def test_computer_takes_winning_move_diagonals(self, game):
        """Test computer takes winning moves in diagonals."""
        # Main diagonal win
        board = ['O', 'X', None, None, 'O', 'X', None, None, None]
        move = game.get_computer_move(board)
        assert move == 8
        
        # Anti-diagonal win
        board = [None, None, 'O', None, 'O', None, None, 'X', 'X']
        move = game.get_computer_move(board)
        assert move == 6

    # ========== BLOCK STRATEGY TESTS (Priority 2) ==========
    
    def test_computer_blocks_human_win_rows(self, game):
        """Test computer blocks human winning moves in rows."""
        # Block top row
        board = ['X', 'X', None, 'O', None, None, None, None, None]
        move = game.get_computer_move(board)
        assert move == 2
        
        # Block middle row
        board = [None, None, None, 'X', 'X', None, 'O', None, None]
        move = game.get_computer_move(board)
        assert move == 5
        
        # Block bottom row
        board = ['O', None, None, None, None, None, 'X', 'X', None]
        move = game.get_computer_move(board)
        assert move == 8

    def test_computer_blocks_human_win_columns(self, game):
        """Test computer blocks human winning moves in columns."""
        # Block left column
        board = ['X', 'O', None, 'X', None, None, None, None, None]
        move = game.get_computer_move(board)
        assert move == 6
        
        # Block middle column
        board = [None, 'X', None, None, 'X', None, 'O', None, None]
        move = game.get_computer_move(board)
        assert move == 7
        
        # Block right column
        board = [None, None, 'X', None, 'O', 'X', None, None, None]
        move = game.get_computer_move(board)
        assert move == 8

    def test_computer_blocks_human_win_diagonals(self, game):
        """Test computer blocks human winning moves in diagonals."""
        # Block main diagonal
        board = ['X', 'O', None, None, 'X', None, None, None, None]
        move = game.get_computer_move(board)
        assert move == 8
        
        # Block anti-diagonal
        board = [None, None, 'X', None, 'X', None, None, 'O', None]
        move = game.get_computer_move(board)
        assert move == 6

    # ========== FORK STRATEGY TESTS (Priority 3) ==========
    
    def test_computer_creates_fork_corner_setup(self, game):
        """Test computer creates fork with corner positions."""
        # Computer at opposite corners creates fork opportunity
        board = ['O', None, None, None, 'X', None, None, None, 'O']
        move = game.get_computer_move(board)
        # AI correctly chooses corner that creates fork (position 2 or 6)
        assert move in [2, 6]
        
        # Verify it actually creates a fork
        new_board = game.make_move(board, move, 'O')
        win_opportunities = 0
        for pos in game.get_available_moves(new_board):
            test_board = game.make_move(new_board, pos, 'O')
            if game.check_winner(test_board, 'O'):
                win_opportunities += 1
        assert win_opportunities >= 2

    def test_computer_creates_fork_edge_center(self, game):
        """Test computer creates fork with edge and center positions."""
        # Computer at center and corner
        board = [None, None, None, None, 'O', None, None, None, 'O']
        move = game.get_computer_move(board)
        # Should create fork
        if move is not None:
            new_board = game.make_move(board, move, 'O')
            win_opportunities = sum(
                1 for pos in game.get_available_moves(new_board)
                if game.check_winner(game.make_move(new_board, pos, 'O'), 'O')
            )
            assert win_opportunities >= 2

    # ========== BLOCK FORK STRATEGY TESTS (Priority 4) ==========
    
    def test_computer_blocks_human_fork_opposite_corners(self, game):
        """Test computer blocks human fork with opposite corners."""
        # Human at opposite corners creates fork threat
        board = ['X', None, None, None, 'O', None, None, None, 'X']
        move = game.get_computer_move(board)
        # AI correctly blocks fork by taking corner (position 2 or 6)
        assert move in [2, 6]

    def test_computer_blocks_human_fork_corner_edge(self, game):
        """Test computer blocks human fork setups."""
        # Human setup that could create fork
        board = ['X', None, None, None, None, None, None, None, 'X']
        move = game.get_computer_move(board)
        # Should take center to prevent fork
        assert move == 4

    # ========== CENTER STRATEGY TESTS (Priority 5) ==========
    
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

    def test_computer_center_priority_over_corners(self, game):
        """Test center takes priority over corners when available."""
        # Human at corner, center available
        board = ['X', None, None, None, None, None, None, None, None]
        move = game.get_computer_move(board)
        assert move == 4

    # ========== OPPOSITE CORNER STRATEGY TESTS (Priority 6) ==========
    
    def test_computer_takes_opposite_corner_pairs(self, game):
        """Test computer takes opposite corner strategy."""
        # Human at top-left (0), computer should take bottom-right (8)
        board = ['X', None, None, None, 'O', None, None, None, None]
        move = game.get_computer_move(board)
        assert move == 8
        
        # Human at top-right (2), computer should take bottom-left (6)
        board = [None, None, 'X', None, 'O', None, None, None, None]
        move = game.get_computer_move(board)
        assert move == 6
        
        # Human at bottom-left (6), computer should take top-right (2)
        board = [None, None, None, None, 'O', None, 'X', None, None]
        move = game.get_computer_move(board)
        assert move == 2
        
        # Human at bottom-right (8), computer should take top-left (0)
        board = [None, None, None, None, 'O', None, None, None, 'X']
        move = game.get_computer_move(board)
        assert move == 0

    def test_computer_opposite_corner_multiple_options(self, game):
        """Test computer behavior with multiple human corners."""
        # Human at multiple corners, computer must block immediate win
        board = ['X', None, 'X', None, 'O', None, None, None, None]
        move = game.get_computer_move(board)
        # AI correctly blocks immediate win at position 1 (top row)
        assert move == 1

    # ========== EMPTY CORNER STRATEGY TESTS (Priority 7) ==========
    
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

    def test_computer_chooses_available_corner(self, game, sample_boards):
        """Test computer chooses available corner when some are taken."""
        board = sample_boards['corners_0_2_taken']
        move = game.get_computer_move(board)
        assert move in [6, 8]

    def test_computer_corner_preference_order(self, game):
        """Test computer corner selection follows consistent order."""
        # Center taken, all corners available
        board = [None, None, None, None, 'X', None, None, None, None]
        move = game.get_computer_move(board)
        assert move in [0, 2, 6, 8]

    # ========== EMPTY SIDE STRATEGY TESTS (Priority 8) ==========
    
    def test_computer_chooses_side_when_center_and_corners_taken(self, game, sample_boards):
        """Test computer chooses sides when center and all corners are taken."""
        board = sample_boards['all_corners_center_taken']
        move = game.get_computer_move(board)
        assert move in [1, 3, 5, 7]

    def test_computer_chooses_available_side(self, game, sample_boards):
        """Test computer chooses available side when some are taken."""
        board = sample_boards['corners_center_sides_partial']
        move = game.get_computer_move(board)
        assert move in [3, 5]

    def test_computer_side_last_resort(self, game):
        """Test sides are chosen only when no better options exist."""
        # All corners and center taken, only sides available
        board = ['X', None, 'O', None, 'X', None, 'O', None, 'X']
        move = game.get_computer_move(board)
        assert move in [1, 3, 5, 7]

    # ========== PRIORITY ORDER TESTS ==========
    
    def test_win_overrides_block(self, game):
        """Test that winning move takes priority over blocking."""
        # Computer can win OR block, should choose win
        board = ['O', 'O', None, 'X', 'X', None, None, None, None]
        move = game.get_computer_move(board)
        assert move == 2  # Win instead of blocking at position 5

    def test_win_overrides_all_other_strategies(self, game):
        """Test win takes priority over all other strategies."""
        # Win available with center also available
        board = ['O', 'O', None, None, None, None, None, None, None]
        move = game.get_computer_move(board)
        assert move == 2  # Win instead of center

    def test_block_overrides_center(self, game):
        """Test that blocking takes priority over center."""
        # Center available but must block
        board = ['X', 'X', None, None, None, None, None, None, None]
        move = game.get_computer_move(board)
        assert move == 2  # Block instead of taking center

    def test_block_overrides_corners_and_sides(self, game):
        """Test blocking takes priority over positional strategies."""
        # Must block, corners available
        board = [None, None, None, 'X', 'X', None, None, None, None]
        move = game.get_computer_move(board)
        assert move == 5  # Block instead of corner

    def test_fork_overrides_center(self, game):
        """Test that fork creation takes priority over center."""
        # Setup where fork is available and center is free
        board = ['O', None, None, None, None, None, None, None, 'O']
        move = game.get_computer_move(board)
        # Should create fork instead of taking center
        if move != 4:  # If not center, verify it creates a fork
            new_board = game.make_move(board, move, 'O')
            win_opportunities = sum(
                1 for pos in game.get_available_moves(new_board)
                if game.check_winner(game.make_move(new_board, pos, 'O'), 'O')
            )
            assert win_opportunities >= 2

    def test_center_overrides_corners(self, game):
        """Test center takes priority over corners."""
        # Center and corners available
        board = ['X', None, None, None, None, None, None, None, None]
        move = game.get_computer_move(board)
        assert move == 4

    def test_corners_override_sides(self, game):
        """Test corners take priority over sides."""
        # Center taken, corners and sides available
        board = [None, None, None, None, 'X', None, None, None, None]
        move = game.get_computer_move(board)
        assert move in [0, 2, 6, 8]

    # ========== EDGE CASES AND NO MOVES ==========
    
    def test_computer_no_moves_available(self, game, sample_boards):
        """Test computer behavior when no moves are available."""
        move = game.get_computer_move(sample_boards['full_board_no_moves'])
        assert move is None

    def test_computer_move_with_one_option(self, game):
        """Test computer behavior with only one available move."""
        board = ['X', 'O', 'X', 'O', 'X', 'O', 'O', 'X', None]
        move = game.get_computer_move(board)
        assert move == 8

    def test_computer_early_game_scenarios(self, game):
        """Test computer moves in early game situations."""
        # Human takes corner, computer should take center
        board = ['X', None, None, None, None, None, None, None, None]
        move = game.get_computer_move(board)
        assert move == 4
        
        # Human takes side, computer should take center
        board = [None, 'X', None, None, None, None, None, None, None]
        move = game.get_computer_move(board)
        assert move == 4
        
        # Human takes center, computer should take corner
        board = [None, None, None, None, 'X', None, None, None, None]
        move = game.get_computer_move(board)
        assert move in [0, 2, 6, 8]

    # ========== INTEGRATION AND GAMEPLAY TESTS ==========
    
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
                
    def test_computer_never_loses_over_gameplay(self, game):
        """Ensure the computer never loses in full gameplay simulation."""
        from random import choice

        for first_human_move in range(9):
            if first_human_move == 4:
                continue  # Computer will take center anyway

            board = [None] * 9
            board[first_human_move] = game.human_symbol

            for _ in range(4):  # Up to 4 more human turns
                # Computer's turn
                comp_move = game.get_computer_move(board)
                assert comp_move is not None
                board = game.make_move(board, comp_move, game.computer_symbol)

                if game.check_winner(board, game.computer_symbol):
                    break  # computer wins, OK

                if game.is_draw(board):
                    break  # draw, OK

                # Human makes a valid random move
                human_moves = game.get_available_moves(board)
                if not human_moves:
                    break

                board = game.make_move(board, choice(human_moves), game.human_symbol)

                # Now check that computer hasn't lost
                assert not game.check_winner(board, game.human_symbol), \
                    f"Computer lost when human started with {first_human_move} and board was {board}"

    def test_computer_strategy_consistency(self, game):
        """Test that computer strategy is consistent across similar board states."""
        # Similar board states should produce similar strategic responses
        board1 = ['X', None, None, None, None, None, None, None, None]
        board2 = [None, None, 'X', None, None, None, None, None, None]
        
        move1 = game.get_computer_move(board1)
        move2 = game.get_computer_move(board2)
        
        # Both should take center
        assert move1 == 4
        assert move2 == 4

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
        board = game.make_move(board, 0, 'X')
        board = game.make_move(board, 4, 'O')
        assert not game.check_winner(board, 'X')
        assert not game.check_winner(board, 'O')
        assert not game.is_draw(board)
        
        # Create winning condition
        board = game.make_move(board, 1, 'X')
        board = game.make_move(board, 2, 'X')
        assert game.check_winner(board, 'X')
        assert not game.check_winner(board, 'O')

class TestEdgeCases:
    """Test cases for edge cases and boundary conditions."""
    
    def test_single_move_scenarios(self, game, sample_boards):
        """Test scenarios with only one move made."""
        for i in range(9):
            board = sample_boards['empty'].copy()
            board = game.make_move(board, i, 'X')
            
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
            board = game.make_move(board, empty_pos, 'O')
            assert game.is_draw(board) == False

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

class TestErrorHandling:
    """Test error handling and edge cases."""
    
    def test_check_winner_with_invalid_board(self, game):
        """Test check_winner handles invalid board gracefully."""
        # Invalid board that causes IndexError - this should be handled
        result = game.check_winner([], 'X')
        assert result == False
        
        # Another invalid scenario
        result = game.check_winner([None, None], 'X')  # Too short
        assert result == False
    
    def test_is_draw_with_invalid_board(self, game):
        """Test is_draw handles invalid board gracefully."""
        # Test board that's too short - should return False due to error handling
        result = game.is_draw([])
        assert result == True  # Empty list passes all() check, then hits error in check_winner
        
        # Test with mixed types that should cause issues
        result = game.is_draw(['X', 'O', 1, 'X', None, None, None, None, None])
        assert result == False  # Should handle TypeError gracefully

class TestUtilityMethods:
    """Test utility and helper methods."""
    
    def test_get_available_moves_empty_board(self, game):
        """Test getting available moves on empty board."""
        board = [None] * 9
        moves = game.get_available_moves(board)
        assert moves == list(range(9))
        assert len(moves) == 9
    
    def test_get_available_moves_partial_board(self, game):
        """Test getting available moves on partially filled board."""
        board = ['X', None, 'O', None, 'X', None, None, 'O', None]
        moves = game.get_available_moves(board)
        expected = [1, 3, 5, 6, 8]
        assert moves == expected
    
    def test_get_available_moves_full_board(self, game):
        """Test getting available moves on full board."""
        board = ['X', 'O', 'X', 'O', 'X', 'O', 'O', 'X', 'O']
        moves = game.get_available_moves(board)
        assert moves == []
    
    def test_make_move_creates_new_board(self, game):
        """Test that make_move creates a new board instance."""
        original_board = [None] * 9
        new_board = game.make_move(original_board, 4, 'X')
        
        assert original_board != new_board
        assert original_board[4] is None
        assert new_board[4] == 'X'
        assert id(original_board) != id(new_board)
    
    def test_make_move_preserves_other_positions(self, game):
        """Test that make_move only changes the specified position."""
        board = ['X', None, 'O', None, None, None, None, None, None]
        new_board = game.make_move(board, 4, 'X')
        
        # Check that other positions are preserved
        assert new_board[0] == 'X'
        assert new_board[2] == 'O'
        assert new_board[4] == 'X'  # New move
        assert new_board[1] is None
        assert new_board[3] is None

