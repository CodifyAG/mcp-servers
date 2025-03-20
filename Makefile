.PHONY: setup clean dev run test lint format help venv

# Default Python interpreter
PYTHON := python3
# pip executable
PIP := pip3

# Project directories
SRC_DIR := src
VENV_DIR := .venv
VENV_PYTHON := $(VENV_DIR)/bin/python
VENV_PIP := $(VENV_DIR)/bin/pip

help:
	@echo "Makefile for mcp-server-harvest-time-tracking"
	@echo ""
	@echo "Usage:"
	@echo "  make venv          Create a virtual environment"
	@echo "  make setup         Install project dependencies in the virtual environment"
	@echo "  make dev           Install development dependencies"
	@echo "  make run           Run the MCP server"
	@echo "  make test          Run tests"
	@echo "  make lint          Run linters (flake8, mypy)"
	@echo "  make format        Format code with black and isort"
	@echo "  make clean         Remove virtual environment and cache files"
	@echo ""

venv:
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv $(VENV_DIR)
	@echo "Virtual environment created at $(VENV_DIR)"
	@echo "Activate with: source $(VENV_DIR)/bin/activate"

setup: venv
	@echo "Installing dependencies in virtual environment..."
	$(VENV_PIP) install python-dotenv requests
	@echo "Attempting to install mcp package..."
	-$(VENV_PIP) install mcp || echo "Warning: mcp package installation failed. You may need to install it manually or use a custom path."

dev: setup
	@echo "Installing development dependencies..."
	$(VENV_PIP) install pytest black isort flake8 mypy

run: setup
	@echo "Running MCP server in virtual environment..."
	$(VENV_PYTHON) -m src.server

test: setup
	@echo "Running tests in virtual environment..."
	$(VENV_PYTHON) -m pytest tests

lint: setup
	@echo "Running linters in virtual environment..."
	$(VENV_PYTHON) -m flake8 $(SRC_DIR)
	$(VENV_PYTHON) -m mypy $(SRC_DIR)

format: setup
	@echo "Formatting code in virtual environment..."
	$(VENV_PYTHON) -m black $(SRC_DIR)
	$(VENV_PYTHON) -m isort $(SRC_DIR)

clean:
	@echo "Cleaning up..."
	rm -rf $(VENV_DIR)
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf __pycache__
	rm -rf $(SRC_DIR)/__pycache__
	rm -rf *.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
