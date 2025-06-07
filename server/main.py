from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config, logger

app = Flask(__name__)

CORS(app, origins=Config.ALLOWED_ORIGINS)

def check_winner(board, player):
    return any(all(board[i] == player for i in pattern) for pattern in Config.WIN_PATTERNS)

def is_draw(board):
    return all(cell is not None for cell in board)

def get_computer_move(board):
    # Prioritize center
    if board[4] is None:
        logger.info("Computer choosing center position")
        return 4

    # Prioritize corners
    for i in [0, 2, 6, 8]:
        if board[i] is None:
            logger.info(f"Computer choosing corner position {i}")
            return i
    
    # Then sides
    for i in [1, 3, 5, 7]:
        if board[i] is None:
            logger.info(f"Computer choosing side position {i}")
            return i
    
    logger.warning("No available moves for computer")
    return None

@app.route("/ping", methods=["GET"])
def ping():
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
        
        # Validate input
        if not board:
            logger.warning("No board data provided")
            return jsonify({"error": "Board data required"}), 400
        
        if len(board) != Config.BOARD_SIZE:
            logger.warning(f"Invalid board size: {len(board)}")
            return jsonify({"error": "Invalid board size"}), 400
        
        if index is None or index < 0 or index >= Config.BOARD_SIZE:
            logger.warning(f"Invalid move index: {index}")
            return jsonify({"error": "Invalid move index"}), 400
        
        if board[index] is not None:
            logger.warning(f"Position {index} already occupied")
            return jsonify({"error": "Position already occupied"}), 400
        
        # Human move
        board[index] = 'X'
        logger.info(f"Human player moved to position {index}")
        
        if check_winner(board, 'X'):
            logger.info("Human player wins")
            return jsonify({"board": board, "status": "X_wins"})
        
        if is_draw(board):
            logger.info("Game ended in draw after human move")
            return jsonify({"board": board, "status": "draw"})
        
        # Computer move
        comp_move = get_computer_move(board)
        if comp_move is not None:
            board[comp_move] = 'O'
            logger.info(f"Computer moved to position {comp_move}")
            
            if check_winner(board, 'O'):
                logger.info("Computer wins")
                return jsonify({"board": board, "status": "O_wins"})
            
            if is_draw(board):
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

if __name__ == "__main__":
    logger.info(f"Starting Flask app on port {Config.PORT}")
    logger.info(f"Debug mode: {Config.DEBUG_MODE}")
    logger.info(f"Allowed origins: {Config.ALLOWED_ORIGINS}")
    
    app.run(
        host="0.0.0.0", 
        port=Config.PORT, 
        debug=Config.DEBUG_MODE
    )