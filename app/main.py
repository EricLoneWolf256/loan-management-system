# the main module for the Loan Management System
# this is where the FastAPI app is created and configured
from fastapi import FastAPI
from app.config import settings
from app.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import auth, users, loans, payments

# Create the database tables    
Base.metadata.create_all(bind=engine)

# Initialize the FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="A Loan Management System API built with FastAPI and SQLAlchemy",
    docs_url=f"{settings.API_V1_PREFIX}/docs",
    redoc_url=f"{settings.API_V1_PREFIX}/redoc",
)

# Configure CORS middleware - allows cross-origin requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint for health check
@app.get("/")
def read_root():
    return {
        "message": "Loan Management System API",
        "status": "running",
        "version": settings.VERSION,
        "docs": f"{settings.API_V1_PREFIX}/docs"
    }
    
@app.get("/health")  
def health_check():
    return {
        "status": "healthy",
        "database": "connected"
    }

# Include routers
app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
app.include_router(users.router, prefix=settings.API_V1_PREFIX)
app.include_router(loans.router, prefix=settings.API_V1_PREFIX)
app.include_router(payments.router, prefix=settings.API_V1_PREFIX)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1", 
        port=8000,
        reload=settings.DEBUG)
# This allows us to run the app with `python app/main.py` and it will automatically reload in debug mode