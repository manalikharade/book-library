@echo off
REM Setup script for Windows

echo Setting up Book Library API...

REM Install dependencies
echo Installing dependencies with uv...
uv sync

REM Create sample data
echo Creating sample database data...
uv run python create_sample_data.py

echo Setup complete! You can now run:
echo   uv run uvicorn app.main:app --host 0.0.0.0
