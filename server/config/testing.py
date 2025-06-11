class TestingConfig:
    """Testing configuration."""
    
    # Security (minimal for testing)
    SECRET_KEY = 'test-secret-key'
    DEBUG = False
    TESTING = True
    
    # Flask settings
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = False
    
    # Rate limiting (disabled for testing)
    RATELIMIT_STORAGE_URL = 'memory://'
    RATELIMIT_HEADERS_ENABLED = False
    
    # Logging
    LOG_LEVEL = 'ERROR'  # Suppress logs during testing
    LOG_TO_STDOUT = False
    
    # CORS (permissive for testing)
    ALLOWED_ORIGINS = ['*']
    
    # Security headers (disabled for testing)
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Application settings
    BOARD_SIZE = 9
    WIN_PATTERNS = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]              # diagonals
    ]
    
    # Server settings
    PORT = 5000