from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import redis.asyncio as redis
import os

from app.api_routes.v1.users import router as users_router
from app.api_routes.v1.refresh_tokens import router as refresh_tokens_router
from app.db.session import engine
from app.db.base import Base
from app.schemas import *  # Import schemas to trigger model rebuilding
from app.core.limiter import limiter
from slowapi.middleware import SlowAPIMiddleware
from app.core.redis_client import init_redis, close_redis
from app.core.exception_handlers import add_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    print("Starting up...")

    # Initialize Redis
    redis_instance = await init_redis()
    app.state.redis = redis_instance
    print("Redis connected")

    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created")
    
    yield
    
    # Shutdown
    print("Shutting down...")
    await close_redis()
    await engine.dispose()
    print("Redis and DB connections closed.")

# Create FastAPI app
app = FastAPI(
    title="Q&A API",
    description="A simple Question and Answer API with async support",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",  
    redoc_url="/redoc",  
    openapi_url="/openapi.json"
)

#TODO: IN PROD CHANGE TO SPECIFIC DOMAINS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add SlowAPI middleware
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# Add custom exception handler
add_exception_handlers(app)


# Include routers
app.include_router(users_router, prefix="/api/v1")
app.include_router(refresh_tokens_router, prefix="/api/v1")


# Serve static frontend
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
async def root():
    """Serve frontend login page"""
    return FileResponse("frontend/index.html")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
