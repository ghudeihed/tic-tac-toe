import pytest
import os
import importlib
import sys
from unittest.mock import patch

class TestConfig:
    """Test cases for configuration settings."""
    
    def test_board_size(self):
        """Test that board size is correctly set to 9."""
        from config.config import Config
        assert Config.BOARD_SIZE == 9
    
    def test_win_patterns_count(self):
        """Test that there are exactly 8 win patterns (3 rows + 3 columns + 2 diagonals)."""
        from config.config import Config
        assert len(Config.WIN_PATTERNS) == 8
    
    def test_win_patterns_structure(self):
        """Test that all win patterns are valid board positions."""
        from config.config import Config
        for pattern in Config.WIN_PATTERNS:
            # Each pattern should have 3 positions
            assert len(pattern) == 3
            # All positions should be valid board indices (0-8)
            assert all(0 <= pos <= 8 for pos in pattern)
            # All positions in a pattern should be unique
            assert len(set(pattern)) == 3
    
    def test_win_patterns_completeness(self):
        """Test that win patterns include all expected combinations."""
        from config.config import Config
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
        if 'config.config' in sys.modules:
            del sys.modules['config.config']
        from config.config import Config
        assert Config.PORT == 5000
    
    @patch.dict(os.environ, {'PORT': '8080'})
    def test_port_from_environment(self):
        """Test port is read from PORT environment variable."""
        # Reload config module to test environment behavior
        if 'config.config' in sys.modules:
            del sys.modules['config.config']
        from config.config import Config
        assert Config.PORT == 8080
    
    def test_allowed_origins_default(self):
        """Test default allowed origins configuration."""
        from config.config import Config
        assert isinstance(Config.ALLOWED_ORIGINS, list)
        assert 'http://localhost:5173' in Config.ALLOWED_ORIGINS
    
    @patch.dict(os.environ, {'ALLOWED_ORIGINS': 'http://localhost:3000,http://localhost:8080'})
    def test_allowed_origins_from_environment(self):
        """Test allowed origins are read from environment variable."""
        # Reload config module to test environment behavior
        if 'config.config' in sys.modules:
            del sys.modules['config.config']
        from config.config import Config
        expected_origins = ['http://localhost:3000', 'http://localhost:8080']
        assert Config.ALLOWED_ORIGINS == expected_origins
    
    @patch.dict(os.environ, {'FLASK_ENV': 'development'})
    def test_DEBUG_development(self):
        """Test debug mode is enabled in development environment."""
        # Reload config module to test environment behavior
        if 'config.config' in sys.modules:
            del sys.modules['config.config']
        from config.config import Config
        assert Config.DEBUG_MODE is True
    
    @patch.dict(os.environ, {'FLASK_ENV': 'production'})
    def test_DEBUG_production(self):
        """Test debug mode is disabled in production environment."""
        # Reload config module to test environment behavior
        if 'config.config' in sys.modules:
            del sys.modules['config.config']
        from config.config import Config
        assert Config.DEBUG_MODE is False
    
    @patch.dict(os.environ, {}, clear=True)
    def test_DEBUG_default(self):
        """Test debug mode defaults to development when FLASK_ENV is not set."""
        # Reload config module to test default behavior
        if 'config.config' in sys.modules:
            del sys.modules['config.config']
        from config.config import Config
        # With our new logic, default is development mode (DEBUG=True)
        assert Config.DEBUG_MODE is True

class TestConfigurationSelection:
    """Test the new configuration selection logic."""
    
    @patch.dict(os.environ, {'FLASK_ENV': 'testing', 'TESTING': 'true'})
    def test_get_testing_config(self):
        """Test that testing config is returned in testing environment."""
        # Clear cache
        if 'config.config' in sys.modules:
            del sys.modules['config.config']
        from config.config import Config
        config = Config.get_config()
        assert config.TESTING is True
        assert config.DEBUG is False
    
    @patch.dict(os.environ, {'FLASK_ENV': 'production', 'SECRET_KEY': 'test-secret'})
    def test_get_production_config(self):
        """Test that production config is returned in production environment."""
        pass
        # Clear cache
        if 'config.config' in sys.modules:
            del sys.modules['config.config']
        from config.config import Config
        config = Config.get_config()
        assert config.DEBUG is False
        assert config.TESTING is False
    
    @patch.dict(os.environ, {'FLASK_ENV': 'development'})
    def test_get_development_config(self):
        """Test that development config is returned in development environment."""
        pass
        # Clear cache
        if 'config.config' in sys.modules:
            del sys.modules['config.config']
        from config.config import Config
        config = Config.get_config()
        assert config.DEBUG is True
        assert config.TESTING is False
    
    @patch.dict(os.environ, {}, clear=True)
    def test_get_default_config(self):
        """Test that development config is returned by default."""
        # Clear cache
        if 'config.config' in sys.modules:
            del sys.modules['config.config']
        from config.config import Config
        config = Config.get_config()
        assert config.DEBUG is True
        assert config.TESTING is False