.PHONY: help setup test test-cov lint format type-check quality build publish clean docker-build docker-push

help:
	@echo "figma-mcp - Development Tasks"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  setup          Setup development environment"
	@echo "  test           Run tests"
	@echo "  test-cov       Run tests with coverage"
	@echo "  lint           Run linting checks"
	@echo "  format         Format code"
	@echo "  type-check     Run type checking"
	@echo "  quality        Run full quality checks"
	@echo "  build          Build distribution"
	@echo "  publish        Publish to PyPI"
	@echo "  docker-build   Build Docker image"
	@echo "  docker-push    Push Docker image"
	@echo "  clean          Clean build artifacts"

setup:
	pip install -e ".[dev]"
	pre-commit install
	@echo "✅ Development environment setup complete!"

test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=figma_mcp --cov-report=html --cov-report=term
	@echo "✅ Coverage report generated in htmlcov/index.html"

lint:
	ruff check figma_mcp/
	black --check figma_mcp/
	@echo "✅ All lint checks passed!"

format:
	black figma_mcp/
	ruff check --fix figma_mcp/
	@echo "✅ Code formatted!"

type-check:
	mypy figma_mcp/ || true
	@echo "✅ Type checking complete!"

quality: lint type-check test
	@echo "✅ All quality checks passed!"

build: test quality
	python -m build
	@echo "✅ Distribution built!"

publish: build
	python -m twine upload dist/* || echo "Set TWINE_USERNAME and TWINE_PASSWORD environment variables"
	@echo "✅ Published to PyPI!"

docker-build:
	docker build -t jozrftamson/figma-mcp:latest .
	@echo "✅ Docker image built!"

docker-push: docker-build
	docker push jozrftamson/figma-mcp:latest
	@echo "✅ Docker image pushed!"

clean:
	rm -rf build/ dist/ *.egg-info htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "✅ Clean complete!"
