import os
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='app.log',
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
    
    DEBUG_MODE = os.getenv('FLASK_ENV', 'production').lower() == 'development'
    
    @staticmethod
    def get_port():
        try:
            return int(os.getenv('PORT', 5000))
        except ValueError:
            logger.warning("Invalid PORT value, defaulting to 5000")
            return 5000
    
    PORT = get_port.__func__()