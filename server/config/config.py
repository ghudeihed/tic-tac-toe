import os
import logging

# Create logs directory if it doesn't exist
log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=os.path.join(log_dir, 'app.log'),
    filemode='a'
)

logger = logging.getLogger(__name__)

class Config:
    """Application configuration settings."""
    
    BOARD_SIZE = 9
    WIN_PATTERNS = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]              # diagonals
    ]
    
    ALLOWED_ORIGINS = [origin.strip() for origin in 
                    os.getenv('ALLOWED_ORIGINS', 'http://localhost:5173').split(',')]
    
    DEBUG_MODE = os.getenv('FLASK_ENV', 'development').lower() == 'development'
    PORT = int(os.getenv('PORT', 5000))
    
    @staticmethod
    def get_config():
        """Get configuration based on environment."""
        env = os.getenv('FLASK_ENV', 'development')
        
        # Check if we're running tests
        if os.getenv('TESTING') == 'true' or 'pytest' in os.environ.get('_', ''):
            from .testing import TestingConfig
            return TestingConfig()
        elif env == 'production':
            from .production import ProductionConfig
            return ProductionConfig()
        elif env == 'development':
            from .development import DevelopmentConfig
            return DevelopmentConfig()
        else:
            # Default to development
            from .development import DevelopmentConfig
            return DevelopmentConfig()