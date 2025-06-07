import pytest
import logging
import tempfile
import os

# Configure logging for tests
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=os.path.join(tempfile.gettempdir(), 'test_app.log'),
    filemode='w'
)

@pytest.fixture
def client():
    """Create a test client for the Flask application.
    
    This fixture:
    - Imports the Flask app
    - Configures it for testing
    - Provides a test client that can make HTTP requests
    - Automatically cleans up after each test
    """
    from main import app
    
    # Configure app for testing
    app.config['TESTING'] = True
    app.config['DEBUG'] = False
    
    # Create and provide test client
    with app.test_client() as client:
        yield client

@pytest.fixture
def game():
    """Create a game instance for testing."""
    from game import TicTacToeGame
    return TicTacToeGame()

@pytest.fixture
def empty_board():
    """Provide an empty 3x3 game board."""
    return [None] * 9

@pytest.fixture
def sample_boards():
    """Provide various board states for testing."""
    return {
        'empty': [None] * 9,
        'human_about_to_win_row': ['X', 'X', None, 'O', 'O', None, None, None, None],
        'human_about_to_win_column': ['X', 'O', 'O', 'X', None, None, None, None, None],
        'human_about_to_win_diagonal': ['X', 'O', 'O', 'O', 'X', None, None, None, None],
        'computer_about_to_win': ['X', 'X', 'O', 'X', 'O', None, None, None, None],
        'draw_position': ['X', 'O', 'X', 'X', 'O', 'O', 'O', 'X', None],
        'game_in_progress': ['X', None, None, None, 'O', None, None, None, None ],
        'center_taken': ['X', None, None, None, 'X', None, None, None, None],
        'almost_win_but_not_quite': ['X', 'X', 'O', 'O', 'O', 'X', None, None, None],
        # Win detection boards
        'top_row_win': ['X', 'X', 'X', 'O', 'O', None, None, None, None],
        'middle_row_win': [None, None, None, 'X', 'X', 'X', 'O', 'O', None],
        'bottom_row_win': [None, None, None, 'O', 'O', None, 'X', 'X', 'X'],
        'left_column_win': ['X', 'O', 'O', 'X', None, None, 'X', None, None],
        'middle_column_win': ['O', 'X', 'O', None, 'X', None, None, 'X', None],
        'right_column_win': ['O', 'O', 'X', None, None, 'X', None, None, 'X'],
        'main_diagonal_win': ['X', 'O', 'O', 'O', 'X', None, None, None, 'X'],
        'anti_diagonal_win': ['O', 'O', 'X', None, 'X', None, 'X', None, None],
        # Computer win boards
        'computer_row_win': ['O', 'O', 'O', 'X', 'X', None, None, None, None],
        'computer_column_win': ['O', 'X', 'X', 'O', None, None, 'O', None, None],
        'computer_diagonal_win': ['O', 'X', None, 'X', 'O', None, None, None, 'O'],
        # Draw boards
        'full_draw_board': ['X', 'O', 'X', 'O', 'X', 'O', 'O', 'X', 'O'],
        'all_x_board': ['X'] * 9,
        'all_o_board': ['O'] * 9,
        'alternating_full_board': ['X', 'O'] * 4 + ['X'],
        'almost_full_board': ['X', 'O', 'X', 'O', 'X', 'O', 'O', 'X', None],
        'one_empty_at_start': [None] + ['X'] * 8,
        'one_empty_at_end': ['X'] * 8 + [None],
        # Computer strategy boards
        'center_free_with_x': ['X', None, None, None, None, None, None, None, None],
        'center_free_with_x_o': ['X', 'O', None, None, None, None, None, None, None],
        'center_taken_by_o': [None, None, None, None, 'O', None, None, None, None],
        'center_taken_some_corners': ['X', None, None, None, 'O', None, None, None, None],
        'all_corners_center_taken': ['X', None, 'O', None, 'X', None, 'O', None, 'X'],
        'corners_0_2_taken': ['X', None, 'O', None, 'X', None, None, None, None],
        'corners_center_sides_partial': ['X', 'O', 'O', None, 'X', None, 'O', None, 'X'],
        'full_board_no_moves': ['X', 'O', 'X', 'O', 'X', 'O', 'O', 'X', 'O'],
        # Move validation boards
        'x_at_0_o_at_4': ['X', None, None, None, 'O', None, None, None, None],
        # Edge case boards
        'many_moves_board': ['X', 'O', 'X', 'O', None, 'X', 'O', None, None]
    }