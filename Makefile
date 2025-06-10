.PHONY: help up down restart test install-backend install-frontend clean logs build

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-22s\033[0m %s\n", $$1, $$2}'

up: ## Run backend and frontend in Docker
	docker compose up --build -d

down: ## Stop and remove containers
	docker compose down

restart: down up ## Restart containers (stop, rebuild, and start)

test: ## Run backend tests with coverage report
	PYTHONPATH=./server/ pytest --cov=. --cov-report=html
	@command -v xdg-open && xdg-open ./htmlcov/index.html || open ./htmlcov/index.html || echo "Open ./htmlcov/index.html manually"

install-backend: ## Install Python backend dependencies
	docker compose run --rm backend pip install -r requirements.txt

install-frontend: ## Install Node frontend dependencies
	docker compose run --rm frontend npm install

clean: ## Remove all dangling images and containers
	docker system prune -f

logs: ## Tail logs from all containers
	docker compose logs -f

build: ## Rebuild all containers without running
	docker compose build

tree: ## Show directory structure
	tree -I 'node_modules|__pycache__|.git|.venv|.idea|.vscode|dist|build|htmlcov|logs' --dirsfirst
