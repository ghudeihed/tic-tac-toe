# Runs backend and frontend together
up:
	docker compose up --build -d 

# Stops and removes containers
down:
	docker compose down

# Stops, removes, and rebuilds containers
restart: down up

# Runs backend tests
test:
	docker compose run --rm backend sh -c "PYTHONPATH=. pytest --cov=."

# Installs Python backend dependencies
install-backend:
	docker compose run --rm backend pip install -r requirements.txt

# Installs Node frontend dependencies
install-frontend:
	docker compose run --rm frontend npm install

# Cleans up all dangling images and containers
clean:
	docker system prune -f
