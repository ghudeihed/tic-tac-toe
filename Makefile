.PHONY: help dev prod test clean logs build deploy health stop restart backend frontend

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-22s\033[0m %s\n", $$1, $$2}'

# Development
dev: ## Run development environment (both services)
	docker compose up --build

dev-backend: ## Run only backend in development
	docker compose up backend --build

dev-frontend: ## Run only frontend in development
	docker compose up frontend --build

# Production - Full Stack
prod: ## Run production environment (both services)
	docker compose -f docker-compose.prod.yml up --build -d

# Production - Individual Services
prod-backend: ## Deploy only backend in production
	docker compose -f docker-compose.backend.yml up --build -d

prod-frontend: ## Deploy only frontend in production
	docker compose -f docker-compose.frontend.yml up --build -d

# Testing
test: ## Run backend tests with coverage report
	docker compose run --rm backend sh -c "cd /app && PYTHONPATH=. pytest --cov=. --cov-report=html --cov-report=term"
	@echo "Coverage report would be generated in htmlcov/ (if running locally)"

test-frontend: ## Run frontend linting
	docker compose run --rm frontend npm run lint

# Building
build: ## Build all production images
	docker compose -f docker-compose.prod.yml build

build-backend: ## Build only backend production image
	docker compose -f docker-compose.backend.yml build

build-frontend: ## Build only frontend production image
	docker compose -f docker-compose.frontend.yml build

# Deployment
deploy: build ## Deploy full stack to production
	@echo "Deploying full stack to production..."
	docker compose -f docker-compose.prod.yml up -d
	@echo "Deployment complete! Check health with 'make health'"

deploy-backend: build-backend ## Deploy only backend to production
	@echo "Deploying backend to production..."
	docker compose -f docker-compose.backend.yml up -d
	@echo "Backend deployment complete!"

deploy-frontend: build-frontend ## Deploy only frontend to production
	@echo "Deploying frontend to production..."
	docker compose -f docker-compose.frontend.yml up -d
	@echo "Frontend deployment complete!"

# Health Checks
health: ## Check application health
	@echo "Checking application health..."
	@curl -f http://localhost:8080/health && echo " ✓ Backend healthy" || echo " ✗ Backend unhealthy"
	@curl -f http://localhost:80/health && echo " ✓ Frontend healthy" || echo " ✗ Frontend unhealthy"

health-backend: ## Check only backend health
	@echo "Checking backend health..."
	@curl -f http://localhost:8080/health && echo " ✓ Backend healthy" || echo " ✗ Backend unhealthy"

health-frontend: ## Check only frontend health
	@echo "Checking frontend health..."
	@curl -f http://localhost:80/health && echo " ✓ Frontend healthy" || echo " ✗ Frontend unhealthy"

# Logs
logs: ## Tail logs from all containers
	docker compose -f docker-compose.prod.yml logs -f

logs-backend: ## Tail backend logs only
	docker compose -f docker-compose.prod.yml logs -f backend

logs-frontend: ## Tail frontend logs only
	docker compose -f docker-compose.prod.yml logs -f frontend

logs-dev: ## Tail logs from development containers
	docker compose logs -f

# Environment Management
env-setup: ## Set up environment files from examples
	@echo "Setting up environment files..."
	@[ ! -f server/.env.production ] && cp server/.env.example server/.env.production && echo "Created server/.env.production" || echo "server/.env.production already exists"
	@[ ! -f client/.env.production ] && cp client/.env.example client/.env.production && echo "Created client/.env.production" || echo "client/.env.production already exists"
	@echo "Please update the environment files with your actual configuration"

env-dev: ## Set up development environment files
	@echo "Setting up development environment files..."
	@[ ! -f server/.env ] && cp server/.env.development server/.env && echo "Created server/.env" || echo "server/.env already exists"
	@[ ! -f client/.env ] && cp client/.env.development client/.env && echo "Created client/.env" || echo "client/.env already exists"

# Cleanup
clean: ## Remove all containers and images
	docker compose down -v --remove-orphans
	docker compose -f docker-compose.prod.yml down -v --remove-orphans
	docker compose -f docker-compose.backend.yml down -v --remove-orphans
	docker compose -f docker-compose.frontend.yml down -v --remove-orphans
	docker system prune -f

stop: ## Stop all containers
	docker compose down
	docker compose -f docker-compose.prod.yml down
	docker compose -f docker-compose.backend.yml down
	docker compose -f docker-compose.frontend.yml down

# Restart
restart: stop prod ## Restart production environment

restart-backend: ## Restart only backend
	docker compose -f docker-compose.backend.yml down
	docker compose -f docker-compose.backend.yml up -d

restart-frontend: ## Restart only frontend  
	docker compose -f docker-compose.frontend.yml down
	docker compose -f docker-compose.frontend.yml up -d

# Legacy targets for backward compatibility
install-backend: ## Install Python backend dependencies
	docker compose run --rm backend pip install -r requirements.txt

install-frontend: ## Install Node frontend dependencies
	docker compose run --rm frontend npm install