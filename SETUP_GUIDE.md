# Book Library Complete Setup Guide

This guide provides step-by-step instructions to set up and run the complete Book Library Management System with React frontend, FastAPI backend, and PostgreSQL database.

## Project Structure

```
book-library/
├── backend/           # FastAPI backend
│   ├── app/          # Application code
│   └── main.py       # Entry point
├── frontend/         # React frontend
│   ├── src/          # React components
│   └── Dockerfile    # Frontend container
├── docker-compose.yml # Orchestration
└── Dockerfile        # Backend container
```

## Quick Start (Docker)

### Option 1: Using Docker Compose (Recommended)

1. **Prerequisites:**
   - Docker and Docker Compose installed
   - Port 3000 (frontend), 8000 (API), 5432 (database) available

2. **Start all services:**
   ```bash
   cd book-library
   docker-compose up
   ```

3. **Access the application:**
   - Frontend: http://localhost:3000
   - API Documentation: http://localhost:8000/docs
   - Database: localhost:5432

4. **Stop services:**
   ```bash
   docker-compose down
   ```

The first run will be slower due to building images. Subsequent runs will be faster.

## Local Development Setup

### Backend Setup

1. **Create Python environment:**
   ```bash
   cd book-library
   python -m venv myenv
   source myenv/bin/activate  # On Windows: myenv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Setup database:**
   - Ensure PostgreSQL is running on localhost:5432
   - Update `DATABASE_URL` in `app/config.py` if needed

4. **Create sample data (optional):**
   ```bash
   cd ..
   python create_sample_data.py
   ```

5. **Start backend server:**
   ```bash
   # From book-library directory
   python -m uvicorn app.main:app --reload --port 8000
   ```
   
   API will be available at http://localhost:8000

### Frontend Setup

1. **Install Node dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Create .env file:**
   ```bash
   cp .env.example .env
   ```
   
   Content:
   ```env
   VITE_API_URL=http://localhost:8000/api
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```
   
   App will be available at http://localhost:3000

## Core Features

### Dashboard
- View total books, available books, total members, and active borrowings
- Table showing all currently borrowed books with member names and days out
- Quick overview of system status

### Books Management
- **Add Book**: Enter title and author
- **View Books**: See all books with availability status
- **Edit Book**: Update book details
- **Delete Book**: Remove books from system
- Color-coded status (green = available, yellow = borrowed)

### Members Management
- **Add Member**: Register new library members with contact and address info
- **View Members**: Browse all registered members
- **Edit Member**: Update member information
- **Delete Member**: Remove members from system

### Borrowing Operations
- **Record Borrow**: Select available book and member to record borrowing
- **Record Return**: Select active borrowing record to mark as returned
- Shows days borrowed automatically
- Validates that books are available and member exists

### Viewing Records
- **Active Borrowings**: See all current unreturned books
- **All Borrowing Records**: View complete borrowing history
- Shows book info, member info, dates, and status
- Ordered by date

## API Endpoints

### Books
- `GET /api/books` - List all books
- `GET /api/books/{id}` - Get specific book
- `POST /api/books` - Create book
- `PUT /api/books/{id}` - Update book
- `DELETE /api/books/{id}` - Delete book
- `GET /api/books/available/all` - List available books

### Members
- `GET /api/members` - List all members
- `GET /api/members/{id}` - Get specific member
- `POST /api/members` - Create member
- `PUT /api/members/{id}` - Update member
- `DELETE /api/members/{id}` - Delete member

### Borrowing
- `POST /api/borrowing/borrow` - Record borrowing
- `POST /api/borrowing/return` - Record return
- `GET /api/borrowing` - List all borrowings
- `GET /api/borrowing/{id}` - Get specific borrowing
- `GET /api/borrowing/active/all` - Get active borrowings
- `GET /api/borrowing/member/{id}/borrowed` - Get member's current books
- `GET /api/borrowing/member/{id}/history` - Get member's borrowing history
- `GET /api/borrowing/book/{id}/history` - Get book's borrowing history

## Database Models

### Book
- id (integer, primary key)
- title (string)
- author (string)
- available (boolean)
- created_at (datetime)

### Member
- id (integer, primary key)
- name (string)
- contact_no (string)
- address (string)
- created_at (datetime)

### Borrowing
- id (integer, primary key)
- book_id (foreign key)
- member_id (foreign key)
- borrowed_date (datetime)
- returned_date (datetime, nullable)
- is_active (boolean)

## Frontend Technologies

- **React 18**: UI framework
- **Vite**: Build tool and dev server
- **Tailwind CSS**: Styling
- **Axios**: HTTP requests
- **JavaScript ES6+**: Modern JavaScript

## Backend Technologies

- **FastAPI**: Web framework
- **SQLAlchemy**: ORM
- **Pydantic**: Data validation
- **PostgreSQL**: Database
- **Uvicorn**: ASGI server

## Configuration Files

### docker-compose.yml
Orchestrates three services:
- **db**: PostgreSQL database
- **api**: FastAPI backend
- **frontend**: React application

All services connected via `book-library-network`

### Dockerfile (Backend)
- Python 3.11 base image
- Installs dependencies
- Runs FastAPI with uvicorn

### frontend/Dockerfile
- Node 18 base image
- Installs npm dependencies
- Builds React app with Vite
- Serves production build

## Environment Variables

Create `.env` in root directory:

```env
# Database
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=book_library
DB_PORT=5432

# API
API_PORT=8000

# Frontend
FRONTEND_PORT=3000
```

Frontend also has `.env.example` in `frontend/` directory

## Troubleshooting

### Docker Issues

**Container fails to start:**
```bash
docker-compose logs api
docker-compose logs frontend
```

**Port already in use:**
```bash
# Change ports in docker-compose.yml or .env
# Or kill processes using the ports
lsof -i :3000  # Find process on port 3000
kill -9 <PID>
```

### Backend Issues

**Database connection errors:**
- Ensure PostgreSQL is running
- Check DATABASE_URL in config.py
- Verify credentials match .env file

**Import errors:**
```bash
pip install -r requirements.txt
```

### Frontend Issues

**API connection errors:**
- Check VITE_API_URL in .env
- Ensure backend is running
- Check browser console for CORS errors

**Port 3000 in use:**
```bash
npm run dev -- --port 3001
```

**Module not found:**
```bash
rm -rf node_modules package-lock.json
npm install
```

## Production Deployment

### Using Docker

1. **Build production images:**
   ```bash
   docker build -t book-library-backend .
   docker build -t book-library-frontend ./frontend
   ```

2. **Update docker-compose.yml:**
   - Remove `volumes` for development
   - Change `command` from reload to production server
   - Set environment variables appropriately

3. **Deploy with proper configuration:**
   - Use environment-specific .env files
   - Set up proper PostgreSQL backup
   - Configure reverse proxy (nginx)
   - Use HTTPS certificates

### Manual Deployment

**Backend:**
```bash
pip install -r requirements.txt
gunicorn app.main:app --bind 0.0.0.0:8000
```

**Frontend:**
```bash
npm install
npm run build
# Serve dist/ folder with web server
```

## Development Tips

1. **Reload modes:**
   - Frontend: Auto-reloads on file changes (HMR)
   - Backend: Auto-reloads with --reload flag

2. **Database reset:**
   ```bash
   # Stop containers
   docker-compose down -v
   
   # Remove postgres_data folder for clean slate
   rm -rf postgres_data
   
   # Restart
   docker-compose up
   ```

3. **Sample data:**
   - Run `create_sample_data.py` after database is ready
   - Useful for testing

4. **API Testing:**
   - Visit http://localhost:8000/docs for interactive Swagger UI
   - Use curl or Postman for manual testing

## Common Workflows

### Add a new book and borrow it

1. Navigate to Books page
2. Click "Add Book" and fill in details
3. Go to Borrowing/Returns page
4. Click "Record Borrow"
5. Select the book and a member
6. Click "Record Borrowing"

### Return a borrowed book

1. Navigate to Borrowing/Returns page
2. Click "Record Return"
3. Select the borrowing record from dropdown
4. Click "Record Return"

### View member's borrowed books

1. Go to Dashboard - see all active borrowings
2. Or go to Borrowing/Returns page - filter by member in active borrowings

## Support

- Check logs: `docker-compose logs [service-name]`
- Review API docs: http://localhost:8000/docs
- Check frontend console for JavaScript errors
- Verify CORS settings in backend if API calls fail
