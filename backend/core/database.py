import sqlite3
import aiosqlite
import asyncio
from pathlib import Path
import logging
from typing import List, Dict, Any

from config import DATABASE_PATH

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_path: str = None):
        self.db_path = db_path or str(DATABASE_PATH)
        
    async def initialize(self):
        """Initialize database and create tables"""
        # Ensure directory exists
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        async with aiosqlite.connect(self.db_path) as db:
            await self._create_tables(db)
            await db.commit()
            logger.info("Database initialized successfully")
    
    async def _create_tables(self, db):
        """Create all necessary tables"""
        
        # Product Eligibility Table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS product_eligibility (
                eligibility_datetime_utc TEXT,
                item_id INTEGER,
                eligibility BOOLEAN,
                message TEXT,
                PRIMARY KEY (eligibility_datetime_utc, item_id)
            )
        """)
        
        # Ad Sales Metrics Table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS ad_sales_metrics (
                date TEXT,
                item_id INTEGER,
                ad_sales REAL,
                impressions INTEGER,
                ad_spend REAL,
                clicks INTEGER,
                units_sold INTEGER,
                PRIMARY KEY (date, item_id)
            )
        """)
        
        # Total Sales Metrics Table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS total_sales_metrics (
                date TEXT,
                item_id INTEGER,
                total_sales REAL,
                total_units_ordered INTEGER,
                PRIMARY KEY (date, item_id)
            )
        """)
        
        # Create indexes for better performance
        await db.execute("CREATE INDEX IF NOT EXISTS idx_eligibility_item ON product_eligibility(item_id)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_ad_sales_item ON ad_sales_metrics(item_id)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_ad_sales_date ON ad_sales_metrics(date)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_total_sales_item ON total_sales_metrics(item_id)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_total_sales_date ON total_sales_metrics(date)")
    
    async def execute_query(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        """Execute a query and return results"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                if params:
                    cursor = await db.execute(query, params)
                else:
                    cursor = await db.execute(query)
                
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Database query error: {e}")
            raise
    
    async def execute_many(self, query: str, data: List[tuple]):
        """Execute many queries with data"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.executemany(query, data)
                await db.commit()
                
        except Exception as e:
            logger.error(f"Database executemany error: {e}")
            raise
    
    async def get_table_schema(self, table_name: str) -> List[Dict[str, Any]]:
        """Get schema information for a table"""
        query = f"PRAGMA table_info({table_name})"
        return await self.execute_query(query)
    
    async def get_all_tables(self) -> List[str]:
        """Get all table names"""
        query = "SELECT name FROM sqlite_master WHERE type='table'"
        results = await self.execute_query(query)
        return [row['name'] for row in results]
