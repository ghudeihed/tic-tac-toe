import os

class DevelopmentConfig:
    """Development configuration."""
    
    # Security (relaxed for development)
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-not-for-production')
    DEBUG = True
    TESTING = False
    
    # Flask settings
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True
    
    # Rate limiting (disabled for development)
    RATELIMIT_STORAGE_URL = 'memory://'
    RATELIMIT_HEADERS_ENABLED = True
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'DEBUG')
    LOG_TO_STDOUT = True
    
    # CORS (permissive for development)
    ALLOWED_ORIGINS = [origin.strip() for origin in 
                      os.getenv('ALLOWED_ORIGINS', 'http://localhost:5173,http://localhost:3000').split(',')]
    
    # Security headers (disabled for development)
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
    PORT = int(os.environ.get('PORT', 5000))