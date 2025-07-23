from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import uvicorn
import asyncio
from typing import Optional
import json
from pydantic import BaseModel
import logging

from api.routes import query, metrics, health
from core.database import DatabaseManager
from services.mistral_service import MistralService
from services.data_processor import DataProcessor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="E-commerce AI Agent",
    description="AI-powered e-commerce data analysis system",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(query.router, prefix="/api", tags=["queries"])
app.include_router(metrics.router, prefix="/api", tags=["metrics"])
app.include_router(health.router, prefix="/api", tags=["health"])

@app.on_event("startup")
async def startup_event():
    """Initialize application components"""
    try:
        logger.info("Initializing database...")
        db_manager = DatabaseManager()
        await db_manager.initialize()
        
        logger.info("Loading data...")
        data_processor = DataProcessor()
        await data_processor.load_all_data()
        
        logger.info("Application started successfully!")
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        raise

@app.get("/")
async def root():
    return {"message": "E-commerce AI Agent API", "status": "running"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
