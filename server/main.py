from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config, logger
from game import TicTacToeGame

app = Flask(__name__)

CORS(app, origins=Config.ALLOWED_ORIGINS)

game = TicTacToeGame()

@app.route("/ping", methods=["GET"])
def ping():
    """Health check endpoint."""
    logger.info("Ping endpoint accessed")
    return jsonify({"message": "pong"})

@app.route('/move', methods=['POST'])
def move():
    """Handle player move and computer response."""
    try:
        data = request.get_json()
        
        if not data:
            logger.warning("No JSON data received")
            return jsonify({"error": "No data provided"}), 400
        
        board = data.get("board")
        index = data.get("index")
        
        # Validate move
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
        return jsonify({"error": "Internal server error"}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    logger.warning(f"404 error: {request.url}")
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"500 error: {str(error)}")
    return jsonify({"error": "Internal server error"}), 500

def create_app():
    """Application factory pattern."""
    return app

if __name__ == "__main__":
    logger.info(f"Starting Flask app on port {Config.PORT}")
    logger.info(f"Debug mode: {Config.DEBUG_MODE}")
    logger.info(f"Allowed origins: {Config.ALLOWED_ORIGINS}")
    
    app.run(
        host="0.0.0.0", 
        port=Config.PORT, 
        debug=Config.DEBUG_MODE
    )