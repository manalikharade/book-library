# Book Library API

A FastAPI application for managing a book library with books, members, and borrowing records.

## Features

- **Books Management**: Add, update, list, and delete books
- **Members Management**: Manage library members
- **Borrowing System**: Track book borrowing and return history with automatic due date calculation
- **Fine Management**: Automatic fine calculation for late book returns (configurable rates)
- **Configuration Management**: API endpoints to view and manage library settings
- **Interactive API Documentation**: Built-in Swagger UI and ReDoc

## Prerequisites

- Python 3.13+
- PostgreSQL 15+
- uv (Python package manager)

## Quick Start

### Local Development Setup

### .env setup
copy variables from .env.example to .env file and update the values

#### Windows
```bash
setup.bat
```

#### Linux/macOS
```bash
chmod +x setup.sh
./setup.sh
```

### Manual Setup

1. **Install dependencies**:
```bash
uv sync
```

2. **Start PostgreSQL** (if not running):
   - Ensure PostgreSQL is running on `localhost:5432`
   - Create database if needed (default name: `book_library`)

3. **Populate sample data**:
```bash
uv run python create_sample_data.py
```

4. **Run the application**:
```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the application is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## API Endpoints

### Health Check
- `GET /` - Health check endpoint
- `GET /health` - Health check endpoint

### Books
- `GET /api/books/` - List all books
- `POST /api/books/` - Create a new book
- `GET /api/books/{id}` - Get book details
- `PUT /api/books/{id}` - Update a book
- `DELETE /api/books/{id}` - Delete a book

### Members
- `GET /api/members/` - List all members
- `POST /api/members/` - Create a new member
- `GET /api/members/{id}` - Get member details
- `PUT /api/members/{id}` - Update a member
- `DELETE /api/members/{id}` - Delete a member

### Borrowing
- `GET /api/borrowing/` - List all borrowing records
- `POST /api/borrowing/` - Create a borrowing record
- `GET /api/borrowing/{id}` - Get borrowing record details
- `PUT /api/borrowing/{id}` - Update a borrowing record
- `PUT /api/borrowing/{id}/return` - Return a book and calculate fine if late

### Configuration
- `GET /api/config/borrowing` - Get borrowing configuration (duration and fine settings)
- `GET /api/config/settings` - Get all application settings

## Configuration

Configuration can be set via environment variables or the `.env` file:

```env
# Database Configuration
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=book_library
DB_PORT=5432
DB_HOST=localhost

# API Configuration
API_PORT=8000

# Borrowing Configuration
BORROWING_DURATION_DAYS=14  # Number of days a member can borrow a book
FINE_PER_DAY=10.0           # Fine amount per day for late returns
MAX_FINE=500.0              # Maximum fine cap per borrowing

# Logging
LOG_LEVEL=INFO
```

## Database Schema

### Books Table
- `id` (int, primary key)
- `title` (string, indexed)
- `author` (string, indexed)
- `available` (boolean, default: true)
- `created_at` (datetime)

### Members Table
- `id` (int, primary key)
- `name` (string, indexed)
- `contact_no` (string)
- `address` (string)
- `created_at` (datetime)

### Borrowings Table
- `id` (int, primary key)
- `book_id` (int, foreign key)
- `member_id` (int, foreign key)
- `borrowed_date` (datetime)
- `due_date` (datetime) - Automatically calculated as borrowed_date + borrowing_duration_days
- `returned_date` (datetime, nullable)
- `is_active` (boolean, default: true)
- `fine` (float, default: 0.0) - Calculated when returned late based on fine_per_day

## Docker Setup

Build and run the application using Docker:

```bash
docker-compose up -d
```

This will:
1. Start PostgreSQL database
2. Build and run the FastAPI application
3. Build and run the React/Next.js frontend application
4. Expose the API on port 8000
5. Expose the frontend on port 3000
6. Create a local `postgres_data/` directory for database persistence

### Data Persistence

PostgreSQL data is stored in a local bind mount at:
```
./postgres_data/
```

This directory is created automatically in your project root and contains all the database files. This allows you to:
- Easily backup your database by copying the `postgres_data/` directory
- Access database files directly from your filesystem
- Persist data between container restarts

### Stopping and Cleaning Up

Stop the containers:
```bash
docker-compose down
```

Stop containers and remove the database volume:
```bash
docker-compose down -v
```

**Note**: The `-v` flag will delete the `postgres_data/` directory and all data in it.

### Accessing the Application

Once running:
- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Database**: localhost:5432 (connect with credentials from `.env`)
- **ReactApp**: http://localhost:3000

## Development

### Install dev dependencies
```bash
uv sync
```

### Run tests
```bash
uv run pytest
```

### Format code
```bash
uv run black app/
```

### Lint code
```bash
uv run flake8 app/
```

### Type checking
```bash
uv run mypy app/
```

## Project Structure

```
book-library/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database setup and session management
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── crud.py              # CRUD operations
│   └── routers/
│       ├── books.py         # Books endpoints
│       ├── members.py       # Members endpoints
│       └── borrowing.py     # Borrowing endpoints
├── create_sample_data.py    # Sample data population script
├── pyproject.toml           # Project configuration and dependencies
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose configuration
├── setup.sh                 # Linux/macOS setup script
├── setup.bat                # Windows setup script
└── README.md                # This file
```