#!/usr/bin/env python3
"""
Database setup script
"""
import asyncio
import sys
import logging
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from core.database import DatabaseManager
from services.data_processor import DataProcessor
from config import DATABASE_PATH

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    """Setup database and load initial data"""
    try:
        logger.info("Setting up database...")
        
        # Initialize database
        db_manager = DatabaseManager()
        await db_manager.initialize()
        
        # Load data
        logger.info("Loading data from Excel files...")
        data_processor = DataProcessor()
        await data_processor.load_all_data()
        
        # Verify data
        stats = await data_processor.get_summary_stats()
        logger.info(f"Data loaded successfully: {stats}")
        
        logger.info("Database setup complete!")
        
    except Exception as e:
        logger.error(f"Database setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
