#!/bin/bash
# Setup script for Linux/macOS

echo "Setting up Book Library API..."

# Install dependencies
echo "Installing dependencies with uv..."
uv sync

# Create sample data
echo "Creating sample database data..."
uv run python create_sample_data.py

echo "Setup complete! You can now run:"
echo "  uv run uvicorn app.main:app --host 0.0.0.0"
