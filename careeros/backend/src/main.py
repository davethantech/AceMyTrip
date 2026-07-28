"""FastAPI application main entry point."""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import structlog

from src.shared.utils.config import get_settings
from src.infrastructure.database.session import init_db, close_db
from src.presentation.api import auth, users, resumes, jobs, applications, ai_services

settings = get_settings()
logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting CareerOS API", version=settings.APP_VERSION)
    await init_db()
    yield
    # Shutdown
    await close_db()
    logger.info("Shutting down CareerOS API")


app = FastAPI(
    title=settings.APP_NAME,
    description="AI-Powered Career Operating System - Automate your job search",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests."""
    logger.info(
        "Request received",
        method=request.method,
        path=request.url.path,
        client_ip=request.client.host if request.client else "unknown",
    )
    response = await call_next(request)
    logger.info(
        "Response sent",
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
    )
    return response


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": settings.APP_VERSION}


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": "AI-Powered Career Operating System",
        "docs": "/docs",
        "health": "/health",
    }


# Include routers
app.include_router(auth.router, prefix=f"{settings.API_PREFIX}/auth", tags=["Authentication"])
app.include_router(users.router, prefix=f"{settings.API_PREFIX}/users", tags=["Users"])
app.include_router(resumes.router, prefix=f"{settings.API_PREFIX}/resumes", tags=["Resumes"])
app.include_router(jobs.router, prefix=f"{settings.API_PREFIX}/jobs", tags=["Jobs"])
app.include_router(applications.router, prefix=f"{settings.API_PREFIX}/applications", tags=["Applications"])
app.include_router(ai_services.router, prefix=f"{settings.API_PREFIX}/ai", tags=["AI Services"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
