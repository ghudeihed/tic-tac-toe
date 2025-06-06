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

def test_move_valid(client):
    board = [None] * 9
    index = 0
    response = client.post("/move", json={"board": board, "index": index})
    assert response.status_code == 200

    data = response.get_json()
    assert "board" in data
    assert data["board"][index] == "X"
    assert data["board"].count("O") == 1
    assert data["board"].count("X") == 1

def test_move_invalid(client):
    board = ["X"] + [None] * 8
    index = 0
    response = client.post("/move", json={"board": board, "index": index})
    assert response.status_code == 400
    assert response.get_json() == {"error": "Invalid move"}
