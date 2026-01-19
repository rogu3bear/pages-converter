# Makefile for Pages Converter

.PHONY: help install test lint format clean build docs

# Default target
help: ## Show this help message
	@echo "Pages Converter Development Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

# Installation
install: ## Install development dependencies
	uv sync

install-dev: ## Install with development dependencies
	uv sync --dev

# Testing
test: ## Run all tests
	uv run python tests/test_converter.py

test-verbose: ## Run tests with verbose output
	uv run python -m pytest tests/ -v

test-coverage: ## Run tests with coverage report
	uv run python -m pytest tests/ --cov=pages_converter --cov-report=html

# Code Quality
lint: ## Run linting checks
	uv run flake8 pages_converter tests
	uv run mypy pages_converter

format: ## Format code with black and isort
	uv run black pages_converter tests scripts
	uv run isort pages_converter tests scripts

check-format: ## Check code formatting
	uv run black --check pages_converter tests scripts
	uv run isort --check-only pages_converter tests scripts

# Development
dev: ## Start development mode
	uv run python pages_converter.py --help

demo: ## Run demo script
	uv run python scripts/demo_converter.py

# Building
build: ## Build the package
	uv build

# Documentation
docs: ## Generate documentation
	@echo "Documentation generation not yet implemented"

# Cleanup
clean: ## Clean up build artifacts and cache
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf __pycache__/
	rm -rf pages_converter/__pycache__/
	rm -rf tests/__pycache__/

clean-all: clean ## Clean everything including uv cache
	rm -rf .venv/
	uv cache clean

# Release
release: ## Create a new release (requires version argument)
	@echo "Usage: make release VERSION=1.0.0"
	@if [ -z "$(VERSION)" ]; then echo "Error: VERSION is required"; exit 1; fi
	@echo "Creating release v$(VERSION)"
	# Update version in pyproject.toml
	# Create git tag
	# Push to GitHub
	@echo "Release process not fully automated yet"

# Git helpers
status: ## Show git status
	git status

push: ## Push changes to remote
	git push origin main

pull: ## Pull changes from remote
	git pull origin main

# CI/CD simulation
ci: lint test build ## Run full CI pipeline locally
	@echo "✅ All checks passed!"

# Quick development cycle
dev-cycle: format lint test ## Run format, lint, and test
	@echo "🎯 Development cycle complete!"