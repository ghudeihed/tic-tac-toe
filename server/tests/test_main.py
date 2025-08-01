import pytest

class TestMoveEndpointHTTP:
    """Test cases for HTTP/API behavior of move endpoint."""
    
    def test_move_successful_request_format(self, client):
        """Test successful move request returns proper format."""
        board = [None] * 9
        response = client.post("/move", json={"board": board, "index": 0})
        data = response.get_json()
        
        assert response.status_code == 200
        assert "board" in data
        assert "status" in data
        assert isinstance(data["board"], list)
        assert len(data["board"]) == 9
        assert data["status"] in ["X_wins", "O_wins", "draw", "in_progress"]
        assert response.content_type == 'application/json'

    def test_move_human_move_applied(self, client):
        """Test that human move is correctly applied to the board."""
        board = [None] * 9
        response = client.post("/move", json={"board": board, "index": 4})
        data = response.get_json()
        
        assert response.status_code == 200
        assert data["board"][4] == 'X'  # Human move applied
        assert data["board"].count('X') == 1

    def test_move_computer_responds(self, client):
        """Test that computer makes a move in response."""
        board = [None] * 9
        response = client.post("/move", json={"board": board, "index": 0})
        data = response.get_json()
        
        assert response.status_code == 200
        assert data["board"].count('O') == 1  # Computer made a move
        assert data["board"][0] == 'X'  # Human move preserved


class TestInputValidation:
    """Test cases for API input validation."""
    
    def test_move_no_data(self, client):
        """Test move endpoint with no JSON data."""
        response = client.post("/move")
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
        assert "Invalid JSON data" in data["error"]

    def test_move_no_board(self, client):
        """Test move endpoint without board data."""
        response = client.post("/move", json={"index": 0})
        assert response.status_code == 400
        data = response.get_json()
        assert data["error"] == "Invalid input"
        assert "board" in data["details"]
        assert "Missing data for required field" in str(data["details"]["board"])

    def test_move_invalid_board_size(self, client):
        """Test move endpoint with invalid board size."""
        board = ['X', 'O']  # Too small
        response = client.post("/move", json={"board": board, "index": 0})
        assert response.status_code == 400
        data = response.get_json()
        # This passes marshmallow but fails game validation
        assert "Invalid board size: 2" in data["error"]

    def test_move_invalid_index_none(self, client):
        """Test move endpoint with None index."""
        board = [None] * 9
        response = client.post("/move", json={"board": board, "index": None})
        assert response.status_code == 400
        data = response.get_json()
        assert data["error"] == "Invalid input"
        assert "index" in data["details"]
        assert "Field may not be null" in str(data["details"]["index"])

    def test_move_invalid_index_negative(self, client):
        """Test move endpoint with negative index."""
        board = [None] * 9
        response = client.post("/move", json={"board": board, "index": -1})
        assert response.status_code == 400
        data = response.get_json()
        # This passes marshmallow but fails game validation
        assert "Invalid move index: -1" in data["error"]

    def test_move_invalid_index_too_large(self, client):
        """Test move endpoint with index too large."""
        board = [None] * 9
        response = client.post("/move", json={"board": board, "index": 9})
        assert response.status_code == 400
        data = response.get_json()
        # This passes marshmallow but fails game validation
        assert "Invalid move index: 9" in data["error"]

    def test_move_position_occupied(self, client):
        """Test move endpoint with already occupied position."""
        board = ['X', None, None,
                None, None, None,
                None, None, None]
        response = client.post("/move", json={"board": board, "index": 0})
        assert response.status_code == 400
        data = response.get_json()
        # This should pass marshmallow validation but fail game validation
        assert "Position 0 already occupied" in data["error"]

    def test_move_invalid_json(self, client):
        """Test move endpoint with invalid JSON."""
        response = client.post("/move", 
                             data="invalid json", 
                             content_type='application/json')
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
        assert "Invalid JSON data" in data["error"]

    def test_move_missing_index(self, client):
        """Test move endpoint with missing index field."""
        board = [None] * 9
        response = client.post("/move", json={"board": board})
        assert response.status_code == 400
        data = response.get_json()
        assert data["error"] == "Invalid input"
        assert "index" in data["details"]
        assert "Missing data for required field" in str(data["details"]["index"])

    def test_move_empty_json(self, client):
        """Test move endpoint with empty JSON object."""
        response = client.post("/move", json={})
        assert response.status_code == 400
        data = response.get_json()
        assert data["error"] == "Invalid input"
        assert "board" in data["details"]
        assert "index" in data["details"]


class TestErrorHandling:
    """Test cases for HTTP error handling."""
    
    def test_404_error(self, client):
        """Test 404 error handling."""
        response = client.get("/nonexistent")
        assert response.status_code == 404
        assert "Endpoint not found" in response.get_json()["error"]

    def test_method_not_allowed_health(self, client):
        """Test method not allowed for health endpoint."""
        response = client.put("/health")
        assert response.status_code == 405

    def test_method_not_allowed_move(self, client):
        """Test method not allowed for move endpoint."""
        response = client.get("/move")
        assert response.status_code == 405


class TestResponseFormat:
    """Test cases for API response format consistency."""
    
    def test_successful_response_content_type(self, client):
        """Test that successful responses have correct content type."""
        board = [None] * 9
        response = client.post("/move", json={"board": board, "index": 0})
        assert response.content_type == 'application/json'

    def test_error_response_format(self, client):
        """Test that error responses have consistent format."""
        response = client.post("/move", json={"index": 0})  # Missing board
        data = response.get_json()
        
        assert response.status_code == 400
        assert "error" in data
        assert isinstance(data["error"], str)
        assert response.content_type == 'application/json'

    def test_health_response_format(self, client):
        """Test health response format."""
        response = client.get("/health")
        health_status = response.get_json()
        
        assert response.status_code == 200
        assert health_status["status"] in ["healthy", "unhealthy"]
        assert health_status["version"] == "1.0.0"
        assert health_status["environment"] in ["production", "development", "testing"]
        assert "checks" in health_status
        assert health_status["checks"]["api"] == "ok"
        assert health_status["checks"]["game_logic"] == "ok"
        assert response.content_type == 'application/json'


class TestGameIntegration:
    """Integration tests for game functionality through HTTP API."""
    
    def test_complete_game_flow_human_wins(self, client):
        """Test complete game flow where human wins via API."""
        board = ['X', 'X', None,
                'O', 'O', None,
                None, None, None]
        response = client.post("/move", json={"board": board, "index": 2})
        data = response.get_json()
        
        assert response.status_code == 200
        assert data["status"] == "X_wins"
        assert data["board"][2] == 'X'

    def test_complete_game_flow_draw(self, client):
        """Test complete game flow ending in draw via API."""
        board = ['X', 'O', 'X',
                'X', 'O', 'O',
                'O', 'X', None]
        response = client.post("/move", json={"board": board, "index": 8})
        data = response.get_json()
        
        assert response.status_code == 200
        assert data["status"] == "draw"
        assert all(cell is not None for cell in data["board"])

    def test_game_continues_properly(self, client):
        """Test that game continues with proper state transitions."""
        board = ['X', None, None,
                None, None, None,
                None, None, None]
        response = client.post("/move", json={"board": board, "index": 1})
        data = response.get_json()
        
        assert response.status_code == 200
        assert data["status"] == "in_progress"
        assert data["board"][1] == 'X'
        assert data["board"].count('O') == 1  # Computer responded