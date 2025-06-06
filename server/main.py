from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

WIN_PATTERNS = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
    [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
    [0, 4, 8], [2, 4, 6]              # diagonals
]

def check_winner(board, player):
    return any(all(board[i] == player for i in pattern) for pattern in WIN_PATTERNS)

def is_draw(board):
    return all(cell is not None for cell in board)

def get_computer_move(board):
    # Prioritize center
    if board[4] is None:
        return 4
    # Prioritize corners
    for i in [0, 2, 6, 8]:
        if board[i] is None:
            return i
    # Then sides
    for i in [1, 3, 5, 7]:
        if board[i] is None:
            return i
    return None 

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "pong"})

@app.route('/move', methods=['POST'])
def move():
    data = request.get_json()
    board = data.get("board")
    index = data.get("index")

    if not board or board[index] is not None:
        return jsonify({"error": "Invalid move"}), 400

    board[index] = 'X'  # Human move

    if check_winner(board, 'X'):
        return jsonify({"board": board, "status": "X_wins"})

    if is_draw(board):
        return jsonify({"board": board, "status": "draw"})

    comp_move = get_computer_move(board)
    if comp_move is not None:
        board[comp_move] = 'O'

    if check_winner(board, 'O'):
        return jsonify({"board": board, "status": "O_wins"})

    if is_draw(board):
        return jsonify({"board": board, "status": "draw"})

    return jsonify({"board": board, "status": "in_progress"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
