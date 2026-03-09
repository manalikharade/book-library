# Book Library API - Docker & PostgreSQL Setup Guide

This guide explains how to set up and run the Book Library API with PostgreSQL using Docker.

## Prerequisites

- Docker installed ([Download Docker Desktop](https://www.docker.com/products/docker-desktop))
- Docker Compose (included with Docker Desktop)
- Git

## Quick Start with Docker Compose

### 1. Clone the Repository

```bash
git clone https://github.com/manalikharade/book-library.git
cd book-library
```

### 2. Create Environment File

Copy the example environment file:

```bash
cp .env.example .env
```

You can optionally edit `.env` to change database credentials, but defaults are fine for development.

### 3. Start Services

```bash
docker-compose up -d
```

This will:
- Start PostgreSQL database on `localhost:5432`
- Start the FastAPI application on `localhost:8000`
- Create all necessary tables automatically

### 4. Verify Services

```bash
# Check if services are running
docker-compose ps

# View API logs
docker-compose logs api

# View database logs
docker-compose logs db
```

### 5. Access the Application

- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## Local Development (Without Docker)

### 1. Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up PostgreSQL

Install PostgreSQL locally and create a database, or use Docker just for the database:

```bash
docker run -d \
  --name book-library-db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=book_library \
  -p 5432:5432 \
  postgres:15-alpine
```

### 4. Configure Environment

Create a `.env` file:

```bash
cp .env.example .env
```

### 5. Run the Application

```bash
python main.py
```

The application will start at `http://localhost:8000`

## Docker Compose Configuration

### Services

**db**: PostgreSQL 15 Alpine
- Port: 5432
- Default User: postgres
- Default Password: password
- Default Database: book_library
- Volume: postgres_data (persistent storage)

**api**: FastAPI Application
- Port: 8000
- Auto-reloads on code changes (development mode)
- Depends on db service

### Environment Variables

Configure in `.env` file:

```
DB_USER=postgres              # PostgreSQL user
DB_PASSWORD=password          # PostgreSQL password
DB_NAME=book_library          # Database name
DB_PORT=5432                  # PostgreSQL port
API_PORT=8000                 # API port
ENVIRONMENT=development       # Environment (development/production)
DEBUG=True                     # Debug mode
```

## Useful Docker Commands

### View Running Containers

```bash
docker-compose ps
```

### View Logs

```bash
# All services
docker-compose logs

# Specific service
docker-compose logs api
docker-compose logs db

# Follow logs
docker-compose logs -f api
```

### Stop Services

```bash
docker-compose stop
```

### Remove Services (including volumes)

```bash
docker-compose down -v
```

### Rebuild Services

```bash
docker-compose up -d --build
```

### Execute Commands in Container

```bash
# Access API container
docker-compose exec api bash

# Access database container
docker-compose exec db psql -U postgres -d book_library
```

## Database Management

### Connect to PostgreSQL

Using psql (if installed locally):

```bash
psql -h localhost -U postgres -d book_library
```

Using Docker:

```bash
docker-compose exec db psql -U postgres -d book_library
```

### Common PostgreSQL Commands

```sql
-- List all tables
\dt

-- Describe a table
\d books

-- List all databases
\l

-- Exit psql
\q
```

## Production Deployment

For production:

1. Update `.env` with secure credentials
2. Set `ENVIRONMENT=production` and `DEBUG=False`
3. Use a production-grade WSGI server:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

4. Use a reverse proxy (nginx) in front of the API
5. Enable SSL/TLS certificates
6. Configure database backups
7. Use managed PostgreSQL service (RDS, CloudSQL, etc.)

## Troubleshooting

### Connection Refused

```bash
# Check if services are running
docker-compose ps

# Restart services
docker-compose restart
```

### Database Not Accessible

```bash
# Check database logs
docker-compose logs db

# Verify database is healthy
docker-compose ps db
```

### Port Already in Use

Change ports in `.env`:

```
API_PORT=8001
DB_PORT=5433
```

Then restart:

```bash
docker-compose restart
```

### Clear Everything and Start Fresh

```bash
docker-compose down -v
docker-compose up -d
```

## Pyproject.toml

The `pyproject.toml` file contains:

- Project metadata
- Dependencies (main and optional dev dependencies)
- Tool configurations (black, isort, mypy)
- Python version requirements

To use it instead of requirements.txt:

```bash
pip install -e .
```

## Project Structure

```
book-library/
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── pyproject.toml            # Modern Python project configuration
├── Dockerfile                # Container image definition
├── docker-compose.yml        # Multi-container orchestration
├── docker-compose.override.yml # Development overrides
├── .env.example              # Example environment variables
├── .dockerignore              # Files to exclude from Docker image
├── setup.sh                  # Setup script for Unix/Linux/macOS
├── setup.bat                 # Setup script for Windows
├── README.md                 # This file
└── app/
    ├── __init__.py
    ├── config.py            # Configuration settings
    ├── database.py          # Database connection
    ├── models.py            # SQLAlchemy models
    ├── schemas.py           # Pydantic schemas
    ├── crud.py              # Database operations
    └── routers/
        ├── books.py         # Books endpoints
        ├── members.py       # Members endpoints
        └── borrowing.py     # Borrowing endpoints
```

## API Endpoints

### Books
- `POST /books/` - Create a new book
- `GET /books/` - List all books
- `GET /books/{book_id}` - Get a specific book
- `GET /books/available/all` - Get all available books
- `PUT /books/{book_id}` - Update a book
- `DELETE /books/{book_id}` - Delete a book

### Members
- `POST /members/` - Create a new member
- `GET /members/` - List all members
- `GET /members/{member_id}` - Get a specific member
- `PUT /members/{member_id}` - Update a member
- `DELETE /members/{member_id}` - Delete a member

### Borrowing
- `POST /borrowing/borrow` - Record a book borrowing
- `POST /borrowing/return` - Record a book return
- `GET /borrowing/{borrowing_id}` - Get a borrowing record
- `GET /borrowing/` - List all borrowing records
- `GET /borrowing/active/all` - Get all active borrowings
- `GET /borrowing/member/{member_id}/borrowed` - Get books currently borrowed by a member
- `GET /borrowing/member/{member_id}/history` - Get borrowing history for a member
- `GET /borrowing/book/{book_id}/history` - Get borrowing history for a book

## Next Steps

1. Start the application: `docker-compose up -d`
2. Open http://localhost:8000/docs
3. Create some test data using the API
4. Explore the API endpoints
5. Check the database using: `docker-compose exec db psql -U postgres -d book_library`

## Support

For issues or questions, please create an issue on GitHub.
