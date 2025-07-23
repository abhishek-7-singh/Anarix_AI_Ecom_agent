#!/usr/bin/env python3
"""
Database setup script - Backend version
"""
import asyncio
import sys
import logging
from pathlib import Path

# Since we're in the backend directory, imports will work directly
from core.database import DatabaseManager
from services.data_processor import DataProcessor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    """Setup database and load initial data"""
    try:
        logger.info("Setting up database...")
        
        # Initialize database
        db_manager = DatabaseManager()
        await db_manager.initialize()
        
        logger.info("Database initialized successfully!")
        logger.info("✅ Database setup complete!")
        
    except Exception as e:
        logger.error(f"Database setup failed: {e}")
        logger.error("Make sure you have the required dependencies installed:")
        logger.error("pip install fastapi uvicorn pandas openpyxl aiosqlite pydantic")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
