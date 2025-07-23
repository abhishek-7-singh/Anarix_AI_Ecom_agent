#!/usr/bin/env python3
"""
Simple database setup without data processing dependencies
"""
import asyncio
import sqlite3
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def setup_database():
    """Setup database tables without data loading"""
    
    # Database path
    db_path = Path("../data/database/ecommerce_data.db")
    
    # Ensure directory exists
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        # Create connection
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        logger.info("Creating database tables...")
        
        # Product Eligibility Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS product_eligibility (
                eligibility_datetime_utc TEXT,
                item_id INTEGER,
                eligibility BOOLEAN,
                message TEXT,
                PRIMARY KEY (eligibility_datetime_utc, item_id)
            )
        """)
        
        # Ad Sales Metrics Table
        cursor.execute("""
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
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS total_sales_metrics (
                date TEXT,
                item_id INTEGER,
                total_sales REAL,
                total_units_ordered INTEGER,
                PRIMARY KEY (date, item_id)
            )
        """)
        
        # Create indexes for better performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_eligibility_item ON product_eligibility(item_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_ad_sales_item ON ad_sales_metrics(item_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_ad_sales_date ON ad_sales_metrics(date)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_total_sales_item ON total_sales_metrics(item_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_total_sales_date ON total_sales_metrics(date)")
        
        # Commit changes
        conn.commit()
        conn.close()
        
        logger.info("✅ Database tables created successfully!")
        logger.info(f"Database location: {db_path.absolute()}")
        
        # Insert some sample data for testing
        await insert_sample_data(str(db_path))
        
    except Exception as e:
        logger.error(f"Database setup failed: {e}")
        return False
    
    return True

async def insert_sample_data(db_path: str):
    """Insert sample data for testing"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        logger.info("Inserting sample data...")
        
        # Sample eligibility data
        cursor.execute("""
            INSERT OR REPLACE INTO product_eligibility 
            (eligibility_datetime_utc, item_id, eligibility, message) 
            VALUES (?, ?, ?, ?)
        """, ('2024-01-01 00:00:00', 1001, 1, 'Product eligible for advertising'))
        
        cursor.execute("""
            INSERT OR REPLACE INTO product_eligibility 
            (eligibility_datetime_utc, item_id, eligibility, message) 
            VALUES (?, ?, ?, ?)
        """, ('2024-01-01 00:00:00', 1002, 0, 'Product not eligible - restricted category'))
        
        # Sample ad sales data
        cursor.execute("""
            INSERT OR REPLACE INTO ad_sales_metrics 
            (date, item_id, ad_sales, impressions, ad_spend, clicks, units_sold) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ('2024-01-01', 1001, 150.75, 1000, 25.50, 45, 3))
        
        cursor.execute("""
            INSERT OR REPLACE INTO ad_sales_metrics 
            (date, item_id, ad_sales, impressions, ad_spend, clicks, units_sold) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ('2024-01-02', 1001, 200.25, 1200, 30.75, 52, 4))
        
        # Sample total sales data
        cursor.execute("""
            INSERT OR REPLACE INTO total_sales_metrics 
            (date, item_id, total_sales, total_units_ordered) 
            VALUES (?, ?, ?, ?)
        """, ('2024-01-01', 1001, 500.25, 10))
        
        cursor.execute("""
            INSERT OR REPLACE INTO total_sales_metrics 
            (date, item_id, total_sales, total_units_ordered) 
            VALUES (?, ?, ?, ?)
        """, ('2024-01-02', 1001, 650.75, 13))
        
        conn.commit()
        conn.close()
        
        logger.info("✅ Sample data inserted successfully!")
        
    except Exception as e:
        logger.error(f"Failed to insert sample data: {e}")

async def main():
    logger.info("Starting database setup...")
    success = await setup_database()
    if success:
        logger.info("🎉 Database setup completed successfully!")
        logger.info("You can now start the backend server with: python main.py")
    else:
        logger.error("❌ Database setup failed!")

if __name__ == "__main__":
    asyncio.run(main())
