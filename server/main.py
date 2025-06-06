from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/ping")
def ping():
    return jsonify({"message": "pong"})

@app.route('/move', methods=['POST'])
def move():
    data = request.get_json()
    board = data.get("board")
    index = data.get("index")

    if not board or board[index] is not None:
        return jsonify({"error": "Invalid move"}), 400

    board[index] = 'X'

    # Basic random computer move
    for i in range(9):
        if board[i] is None:
            board[i] = 'O'
            break

    return jsonify({"board": board})

if __name__ == "__main__":
    app.run(debug=True)
