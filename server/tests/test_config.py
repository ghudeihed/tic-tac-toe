import pytest
import os
import importlib
from unittest.mock import patch
from config import Config

class TestConfig:
    """Test cases for configuration settings."""
    
    def test_board_size(self):
        """Test that board size is correctly set to 9."""
        assert Config.BOARD_SIZE == 9
    
    def test_win_patterns_count(self):
        """Test that there are exactly 8 win patterns (3 rows + 3 columns + 2 diagonals)."""
        assert len(Config.WIN_PATTERNS) == 8
    
    def test_win_patterns_structure(self):
        """Test that all win patterns are valid board positions."""
        for pattern in Config.WIN_PATTERNS:
            # Each pattern should have 3 positions
            assert len(pattern) == 3
            # All positions should be valid board indices (0-8)
            assert all(0 <= pos <= 8 for pos in pattern)
            # All positions in a pattern should be unique
            assert len(set(pattern)) == 3
    
    def test_win_patterns_completeness(self):
        """Test that win patterns include all expected combinations."""
        expected_patterns = {
            # Rows
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            # Columns  
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            # Diagonals
            (0, 4, 8), (2, 4, 6)
        }
        
        actual_patterns = {tuple(pattern) for pattern in Config.WIN_PATTERNS}
        assert actual_patterns == expected_patterns
    
    @patch.dict(os.environ, {}, clear=True)
    def test_port_default_when_not_set(self):
        """Test default port when PORT environment variable is not set."""
        # Reload config module to test default behavior
        import config
        importlib.reload(config)
        assert config.Config.PORT == 5000
    
    @patch.dict(os.environ, {'PORT': '8080'})
    def test_port_from_environment(self):
        """Test port is read from PORT environment variable."""
        import config
        importlib.reload(config)
        assert config.Config.PORT == 8080
    
    def test_allowed_origins_default(self):
        """Test default allowed origins configuration."""
        assert isinstance(Config.ALLOWED_ORIGINS, list)
        assert 'http://localhost:5173' in Config.ALLOWED_ORIGINS
    
    @patch.dict(os.environ, {'ALLOWED_ORIGINS': 'http://localhost:3000,http://localhost:8080'})
    def test_allowed_origins_from_environment(self):
        """Test allowed origins are read from environment variable."""
        import config
        importlib.reload(config)
        expected_origins = ['http://localhost:3000', 'http://localhost:8080']
        assert config.Config.ALLOWED_ORIGINS == expected_origins
    
    @patch.dict(os.environ, {'FLASK_ENV': 'development'})
    def test_debug_mode_development(self):
        """Test debug mode is enabled in development environment."""
        import config
        importlib.reload(config)
        assert config.Config.DEBUG_MODE is True
    
    @patch.dict(os.environ, {'FLASK_ENV': 'production'})
    def test_debug_mode_production(self):
        """Test debug mode is disabled in production environment."""
        import config
        importlib.reload(config)
        assert config.Config.DEBUG_MODE is False
    
    @patch.dict(os.environ, {}, clear=True)
    def test_debug_mode_default(self):
        """Test debug mode defaults to False when FLASK_ENV is not set."""
        import config
        importlib.reload(config)
        assert config.Config.DEBUG_MODE is False