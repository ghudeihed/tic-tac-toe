import os
from flask import Flask, request, jsonify
from flask_cors import CORS

def create_app(config_name=None):
    """Application factory pattern."""
    app = Flask(__name__)
    
    # Set testing environment early if needed
    if config_name == 'testing':
        os.environ['TESTING'] = 'true'
        os.environ['FLASK_ENV'] = 'testing'
    
    # Import after environment setup
    from config.config import Config, logger
    from game import TicTacToeGame
    from schemas import validate_move_input
    from datetime import datetime
    
    # Load configuration
    config = Config.get_config()
    app.config.from_object(config)
    
    # CORS
    CORS(app, origins=config.ALLOWED_ORIGINS)
    
    # Initialize production dependencies only if available and not in testing
    limiter = None
    if not getattr(config, 'TESTING', False):
        try:
            import sentry_sdk
            from sentry_sdk.integrations.flask import FlaskIntegration
            from flask_talisman import Talisman
            from flask_limiter import Limiter
            from flask_limiter.util import get_remote_addr
            
            # Initialize Sentry for error tracking
            if os.getenv('SENTRY_DSN'):
                sentry_sdk.init(
                    dsn=os.getenv('SENTRY_DSN'),
                    integrations=[FlaskIntegration()],
                    traces_sample_rate=0.1,
                    environment=os.getenv('FLASK_ENV', 'development')
                )

            # Security headers (only in production)
            if os.getenv('FLASK_ENV') == 'production':
                Talisman(app,
                    force_https=False,  # Let reverse proxy handle HTTPS
                    strict_transport_security=True,
                    content_security_policy={
                        'default-src': "'self'",
                        'script-src': "'self'",
                        'style-src': "'self' 'unsafe-inline'",
                    }
                )

            # Rate limiting - Fixed syntax
            limiter = Limiter(
                key_func=get_remote_addr,
                app=app,
                default_limits=["200 per day", "50 per hour"],
                storage_uri=getattr(config, 'RATELIMIT_STORAGE_URL', 'memory://')
            )
            
        except ImportError as e:
            # If production dependencies aren't installed, continue without them
            logger.warning(f"Production dependencies not installed: {e}")
    
    game = TicTacToeGame()

    @app.route("/health", methods=["GET"])
    def health():
        """Comprehensive health check."""
        health_status = {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": os.getenv("APP_VERSION", "1.0.0"),
            "environment": os.getenv("FLASK_ENV", "development"),
            "checks": {
                "api": "ok",
                "game_logic": "ok"
            }
        }
        
        try:
            # Test game logic
            test_game = TicTacToeGame()
            test_board = [None] * 9
            test_game.validate_move(test_board, 0)
                
        except Exception as e:
            health_status["status"] = "unhealthy"
            health_status["checks"]["game_logic"] = f"error: {str(e)}"
            return jsonify(health_status), 503
        
        return jsonify(health_status)

    def move():
        """Handle player move and computer response with validation."""
        try:
            # Handle request parsing errors
            try:
                json_data = request.get_json()
            except Exception as e:
                logger.warning(f"Invalid JSON data: {str(e)}")
                return jsonify({"error": "Invalid JSON data"}), 400
            
            if json_data is None:
                logger.warning("No JSON data received")
                return jsonify({"error": "No JSON data provided"}), 400
            
            # Validate input with marshmallow
            data, errors = validate_move_input(json_data)
            if errors:
                logger.warning(f"Input validation failed: {errors}")
                return jsonify({"error": "Invalid input", "details": errors}), 400
            
            board = data["board"]
            index = data["index"]
            
            # Additional game validation
            is_valid, error_msg = game.validate_move(board, index)
            if not is_valid:
                logger.warning(error_msg)
                return jsonify({"error": error_msg}), 400
            
            # Human move
            board[index] = 'X'
            logger.info(f"Human player moved to position {index}")
            
            if game.check_winner(board, 'X'):
                logger.info("Human player wins")
                return jsonify({"board": board, "status": "X_wins"})
            
            if game.is_draw(board):
                logger.info("Game ended in draw after human move")
                return jsonify({"board": board, "status": "draw"})
            
            # Computer move
            comp_move = game.get_computer_move(board)
            if comp_move is not None:
                board[comp_move] = 'O'
                logger.info(f"Computer moved to position {comp_move}")
                
                if game.check_winner(board, 'O'):
                    logger.info("Computer wins")
                    return jsonify({"board": board, "status": "O_wins"})
                
                if game.is_draw(board):
                    logger.info("Game ended in draw after computer move")
                    return jsonify({"board": board, "status": "draw"})
            
            logger.info("Game continues")
            return jsonify({"board": board, "status": "in_progress"})
        
        except Exception as e:
            logger.error(f"Error processing move: {str(e)}")
            if 'sentry_sdk' in globals():
                sentry_sdk.capture_exception(e)
            return jsonify({"error": "Internal server error"}), 500

    # Apply rate limiting conditionally
    if limiter:
        move = limiter.limit("30 per minute")(move)
    
    # Register the route
    app.add_url_rule('/move', 'move', move, methods=['POST'])

    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        logger.warning(f"404 error: {request.url}")
        return jsonify({"error": "Endpoint not found"}), 404

    @app.errorhandler(429)
    def rate_limit_handler(e):
        """Handle rate limit errors."""
        logger.warning(f"Rate limit exceeded for {request.remote_addr}")
        return jsonify({
            "error": "Rate limit exceeded", 
            "retry_after": str(getattr(e, 'retry_after', 60))
        }), 429

    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        logger.error(f"500 error: {str(error)}")
        try:
            import sentry_sdk
            sentry_sdk.capture_exception(error)
        except ImportError:
            pass
        return jsonify({"error": "Internal server error"}), 500

    return app

# Create app instance
app = create_app()

if __name__ == "__main__":
    from config.config import Config, logger
    
    logger.info(f"Starting Flask app on port {Config.PORT}")
    logger.info(f"Debug mode: {Config.DEBUG_MODE}")
    logger.info(f"Allowed origins: {Config.ALLOWED_ORIGINS}")
    
    app.run(
        host="0.0.0.0", 
        port=Config.PORT, 
        debug=Config.DEBUG_MODE
    )