"""
Star Power API - FastAPI Backend
Main application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Star Power API",
    description="Backend API for Star Power - A Celebrity Card Game",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration - Allow frontend to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api", tags=["game"])

@app.get("/", tags=["root"])
def root():
    """Root endpoint - API information"""
    return {
        "message": "Star Power API",
        "version": "0.1.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health"
    }

@app.get("/health", tags=["health"])
def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": "star-power-api",
        "version": "0.1.0"
    }

@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    logger.info("🚀 Star Power API starting up...")
    logger.info("📚 API Documentation available at /docs")

@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    logger.info("👋 Star Power API shutting down...")

if __name__ == "__main__":
    import uvicorn

    # Get port from environment (Railway sets this) or default to 8000
    port = int(os.environ.get("PORT", 8000))

    logger.info(f"Starting server on port {port}")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
