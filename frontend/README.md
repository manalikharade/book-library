# Book Library Frontend (Next.js)

React/Next.js 14 frontend application for the Book Library Management System.

## Features

- **Dashboard**: Overview of books, members, and active borrowings
- **Books Management**: Add, edit, delete, and view books
- **Members Management**: Add, edit, delete, and view library members
- **Borrowing System**: Record when members borrow books and when they return them
- **Borrowing History**: View all borrowing records and member borrowing history
- **Real-time Status**: See which books are available and which are currently borrowed

## Technology Stack

- **Next.js 14**: React framework with App Router
- **React 18**: UI library
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client for API communication
- **JavaScript ES6+**: Modern JavaScript

## Setup

### Prerequisites

- Node.js 18+ and npm

### Local Development

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Create `.env.local` file:**
   ```bash
   cp .env.example .env.local
   ```
   
   Update API URL if needed:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000/api
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```
   
   The app will be available at `http://localhost:3000`

4. **Build for production:**
   ```bash
   npm run build
   npm start
   ```

## Docker Setup

### Build and run with Docker

```bash
# Build image
docker build -t book-library-frontend ./frontend

# Run container for development
docker run -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL=http://localhost:8000/api \
  -v $(pwd)/frontend:/app \
  book-library-frontend npm run dev

# Run container for production
docker build -t book-library-frontend:prod ./frontend
docker run -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL=http://api:8000/api \
  book-library-frontend:prod
```

### Using Docker Compose (from root directory)

```bash
# Start all services (backend, frontend, database)
docker-compose up

# Access frontend at http://localhost:3000
# Access API docs at http://localhost:8000/docs
```

## Project Structure (Next.js App Router)

```
frontend/
├── app/                      # Next.js app directory
│   ├── layout.jsx           # Root layout with Navbar
│   ├── globals.css          # Tailwind imports
│   ├── page.jsx             # Dashboard page (/)
│   ├── books/
│   │   ├── layout.jsx       # Books section layout
│   │   └── page.jsx         # Books management page
│   ├── members/
│   │   ├── layout.jsx       # Members section layout
│   │   └── page.jsx         # Members management page
│   └── borrowing/
│       ├── layout.jsx       # Borrowing section layout
│       └── page.jsx         # Borrowing operations page
├── lib/
│   └── api/                 # API integration layer
│       ├── axiosConfig.js        # Axios configuration
│       ├── bookApi.js            # Book endpoints
│       ├── memberApi.js          # Member endpoints
│       ├── borrowingApi.js       # Borrowing endpoints
│       └── index.js              # Export all APIs
├── components/              # Reusable React components
│   ├── Navbar.jsx           # Navigation bar
│   ├── BookForm.jsx         # Book add/edit form
│   ├── BookTable.jsx        # Books list table
│   ├── MemberForm.jsx       # Member add/edit form
│   ├── MemberTable.jsx      # Members list table
│   ├── BorrowForm.jsx       # Borrow book form
│   ├── ReturnForm.jsx       # Return book form
│   └── BorrowingTable.jsx   # Borrowing records table
├── jsconfig.json            # Path aliases configuration
├── next.config.js           # Next.js configuration
├── package.json
├── Dockerfile
├── .env.example             # Environment template
└── .env.local               # Local environment (git-ignored)
```

## Next.js App Router Benefits

✅ **Server Components**: Automatic client/server boundaries
✅ **Streaming**: Progressive rendering support
✅ **Route Groups**: Organized folder structure
✅ **Layouts**: Shared UI between routes
✅ **Path Aliases**: `@/` imports instead of relative paths
✅ **Built-in Optimization**: Image, font, and script optimization
✅ **Fast Refresh**: Instant updates during development

## API Integration

The frontend communicates with the FastAPI backend at configured `NEXT_PUBLIC_API_URL`.

### Environment Variables

- `NEXT_PUBLIC_API_URL` - Backend API URL (exposed to browser)
  - Local development: `http://localhost:8000/api`
  - Docker: `http://api:8000/api`

## Running in Different Environments

### Local Development with Backend

```bash
# Terminal 1 - Backend
cd ..
python -m uvicorn app.main:app --reload

# Terminal 2 - Frontend
npm run dev
```

Visit: `http://localhost:3000`

### Docker Compose (Full Stack)

```bash
docker-compose up
```

Automatically sets up:
- PostgreSQL database
- FastAPI backend
- Next.js frontend
- Network communication

### Production Build

```bash
npm run build
npm start
```

Creates optimized production build and starts server.

## Key Files Explained

### app/layout.jsx
Root layout that includes Navbar and wraps all pages. Sets up HTML structure and metadata.

### app/page.jsx
Dashboard page showing stats and active borrowings. Uses Server Components where possible.

### lib/api/\*
API modules using Axios. Each module handles one resource (books, members, borrowing).

### components/\*
Reusable client components marked with `'use client'` for interactivity (forms, tables).

## Common Tasks

### Add a new page

1. Create folder in `app/` (e.g., `app/reports/`)
2. Add `layout.jsx` with metadata
3. Add `page.jsx` with component
4. Auto-added to navigation

### Use API from component

```javascript
'use client'
import { bookApi } from '@/lib/api'

export default function MyComponent() {
  const [books, setBooks] = useState([])
  
  useEffect(() => {
    bookApi.getAllBooks().then(res => setBooks(res.data))
  }, [])
  
  return <div>{/* render books */}</div>
}
```

### Add new API endpoint

1. Create file in `lib/api/` (e.g., `reportApi.js`)
2. Export functions using Axios
3. Import and use in components

## Troubleshooting

### Frontend can't connect to API

1. Check `NEXT_PUBLIC_API_URL` in `.env.local`
2. Ensure backend is running on correct port
3. Check browser console for CORS errors
4. Verify backend CORS middleware allows frontend origin

### Port 3000 already in use

```bash
# Kill process using port 3000
lsof -i :3000
kill -9 <PID>
```

### Modules not found

```bash
rm -rf node_modules .next
npm install
npm run dev
```

### 'use client' directive

Mark components that use hooks/interactivity with `'use client'`:
- Components with useState, useEffect
- Event handlers (onClick, onChange)
- Browser APIs

Server components (no directive) are default.

## Building for Production

### Development Image

```dockerfile
# Uses next dev (with file watching)
CMD ["npm", "run", "dev"]
```

### Production Image

```dockerfile
RUN npm run build
CMD ["npm", "start"]
```

For production use, create separate Dockerfile.prod with build step.

## Browser Support

Next.js 14 supports:
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Performance Tips

1. **Use Image component** instead of `<img>`
2. **Dynamic imports** for large components
3. **Code splitting** automatic by routes
4. **Font optimization** with next/font
5. **API routes** for backend if needed

## Development Tips

- HMR (Hot Module Replacement) enabled by default
- Fast Refresh preserves component state
- Source maps for debugging in dev tools
- Next.js DevTools for performance analysis

## Related Documents

- [Backend README](../README.md)
- [SETUP_GUIDE.md](../SETUP_GUIDE.md) - Full system setup
- [Dockerfile](./Dockerfile) - Container configuration
