.PHONY: help install install-dev lint format typecheck test test-cov clean build publish

.DEFAULT_GOAL := help
include Makefile.dev Makefile.ci

help: ## Show this help message
	@echo "Available commands:"
	@grep -h -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install package in development mode
	uv sync --no-dev

lint: ## Run linting with ruff
	uv run ruff check .

format: ## Format code with ruff
	uv run ruff format .

format-check: ## Check formatting without applying changes
	uv run ruff format --check .

typecheck: ## Run type checking with mypy
	uv run mypy src/hackathon_roulette tests

test: ## Run tests with pytest
	uv run pytest tests/ -v

test-cov: ## Run tests with coverage report
	uv run pytest tests/ -v --cov=src/hackathon_roulette --cov-report=term-missing --cov-report=html

test-fast: ## Run tests without slow markers
	uv run pytest tests/ -v -m "not slow"

clean: ## Clean build artifacts and caches
	rm -rf build/
	rm -rf dist/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

build: clean ## Build package
	uv build

publish: ## Publish to the private artifactory
	uv publish --publish-url https://artifactory.dummy.com/pypi
