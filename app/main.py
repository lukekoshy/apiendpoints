from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.mongodb import mongodb_client
from app.routes import organizations, auth

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Multi-tenant organization management service",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database connection on startup"""
    try:
        mongodb_client.connect()
        print("✓ Application started successfully with MongoDB connected")
    except Exception as e:
        print(f"⚠ Application started but MongoDB connection failed: {e}")
        print("  The API is running but database operations will fail until MongoDB is available")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown"""
    mongodb_client.disconnect()
    print("✓ Application shut down successfully")


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "app": settings.APP_NAME}


# Include routers
app.include_router(organizations.router)
app.include_router(auth.router)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "app": settings.APP_NAME,
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "organizations": {
                "create": "POST /org/create",
                "get": "GET /org/get",
                "update": "PUT /org/update",
                "delete": "DELETE /org/delete",
            },
            "admin": {
                "login": "POST /admin/login",
            },
        },
    }
