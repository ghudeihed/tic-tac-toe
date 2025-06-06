import pytest
from main import app

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

def test_ping(client):
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.get_json() == {"message": "pong"}

def test_move_valid_human_win(client):
    # Simulate human (X) winning move
    board = ['X', 'X', None,
            'O', 'O', None,
            None, None, None]
    response = client.post("/move", json={"board": board, "index": 2})
    data = response.get_json()

    assert response.status_code == 200
    assert data["status"] == "X_wins"
    assert data["board"][2] == 'X'

def test_move_valid_computer_win(client):
    board = ['X', 'X', 'O',
            'X', 'O', None,
            None, None, None]
    response = client.post("/move", json={"board": board, "index": 5})
    data = response.get_json()

    assert response.status_code == 200
    assert data["status"] == "O_wins"

def test_move_draw(client):
    board = ['X', 'O', 'X',
            'X', 'O', 'O',
            'O', 'X', None]
    response = client.post("/move", json={"board": board, "index": 8})
    data = response.get_json()

    assert response.status_code == 200
    assert data["status"] == "draw"

def test_move_in_progress(client):
    board = ['X', None, None,
            None, None, None,
            None, None, None]
    response = client.post("/move", json={"board": board, "index": 1})
    data = response.get_json()

    assert response.status_code == 200
    assert data["status"] == "in_progress"
    assert data["board"][1] == 'X'
    assert 'O' in data["board"]
