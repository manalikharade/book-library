from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import init_db
from app.routers import books, borrowing, members

settings = get_settings()

app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    swagger_ui_parameters={
        "defaultModelsExpandDepth": 1,
        "defaultModelExpandDepth": 1,
        "deepLinking": True,
        "presets": [
            "https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui.js",
            "https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui-bundle.js",
        ],
    },
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
@app.on_event("startup")
def startup():
    init_db()

# Include routers
app.include_router(books.router, prefix="/api/books", tags=["books"])
app.include_router(borrowing.router, prefix="/api/borrowing", tags=["borrowing"])
app.include_router(members.router, prefix="/api/members", tags=["members"])

@app.get("/", tags=["health"])
async def root():
    """Health check endpoint"""
    return {"message": "Book Library API is running"}

@app.get("/health", tags=["health"])
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}
