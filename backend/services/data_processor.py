import pandas as pd
import logging
from pathlib import Path
from typing import List, Dict, Any
import asyncio

from core.database import DatabaseManager
from config import ELIGIBILITY_FILE, AD_SALES_FILE, TOTAL_SALES_FILE

logger = logging.getLogger(__name__)

class DataProcessor:
    def __init__(self):
        self.db_manager = DatabaseManager()
    
    async def load_all_data(self):
        """Load all data from Excel files into database"""
        try:
            logger.info("Loading eligibility data...")
            await self.load_eligibility_data()
            
            logger.info("Loading ad sales data...")
            await self.load_ad_sales_data()
            
            logger.info("Loading total sales data...")
            await self.load_total_sales_data()
            
            logger.info("All data loaded successfully!")
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    async def load_eligibility_data(self):
        """Load product eligibility data"""
        try:
            df = pd.read_excel(ELIGIBILITY_FILE)
            
            # Clean and prepare data
            df['eligibility'] = df['eligibility'].astype(bool)
            df['message'] = df['message'].fillna('')
            
            # FIXED: Convert timestamp to string format
            df['eligibility_datetime_utc'] = pd.to_datetime(df['eligibility_datetime_utc']).dt.strftime('%Y-%m-%d %H:%M:%S')
            
            # Convert to list of tuples for insertion
            data = [
                (
                    str(row['eligibility_datetime_utc']),  # Now it's already a string
                    int(row['item_id']),
                    bool(row['eligibility']),
                    str(row['message'])
                )
                for _, row in df.iterrows()
            ]
            
            # Clear existing data and insert new data
            await self.db_manager.execute_query("DELETE FROM product_eligibility")
            
            query = """
                INSERT OR REPLACE INTO product_eligibility 
                (eligibility_datetime_utc, item_id, eligibility, message) 
                VALUES (?, ?, ?, ?)
            """
            
            await self.db_manager.execute_many(query, data)
            logger.info(f"Loaded {len(data)} eligibility records")
            
        except Exception as e:
            logger.error(f"Error loading eligibility data: {e}")
            raise
    
    async def load_ad_sales_data(self):
        """Load ad sales metrics data"""
        try:
            df = pd.read_excel(AD_SALES_FILE)
            
            # Clean and prepare data
            numeric_columns = ['ad_sales', 'impressions', 'ad_spend', 'clicks', 'units_sold']
            for col in numeric_columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
            # FIXED: Convert date to string format
            df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
            
            # Convert to list of tuples for insertion
            data = [
                (
                    str(row['date']),  # Now it's already a string
                    int(row['item_id']),
                    float(row['ad_sales']),
                    int(row['impressions']),
                    float(row['ad_spend']),
                    int(row['clicks']),
                    int(row['units_sold'])
                )
                for _, row in df.iterrows()
            ]
            
            # Clear existing data and insert new data
            await self.db_manager.execute_query("DELETE FROM ad_sales_metrics")
            
            query = """
                INSERT OR REPLACE INTO ad_sales_metrics 
                (date, item_id, ad_sales, impressions, ad_spend, clicks, units_sold) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            
            await self.db_manager.execute_many(query, data)
            logger.info(f"Loaded {len(data)} ad sales records")
            
        except Exception as e:
            logger.error(f"Error loading ad sales data: {e}")
            raise
    
    async def load_total_sales_data(self):
        """Load total sales metrics data"""
        try:
            df = pd.read_excel(TOTAL_SALES_FILE)
            
            # Clean and prepare data
            df['total_sales'] = pd.to_numeric(df['total_sales'], errors='coerce').fillna(0)
            df['total_units_ordered'] = pd.to_numeric(df['total_units_ordered'], errors='coerce').fillna(0)
            
            # FIXED: Convert date to string format
            df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
            
            # Convert to list of tuples for insertion
            data = [
                (
                    str(row['date']),  # Now it's already a string
                    int(row['item_id']),
                    float(row['total_sales']),
                    int(row['total_units_ordered'])
                )
                for _, row in df.iterrows()
            ]
            
            # Clear existing data and insert new data
            await self.db_manager.execute_query("DELETE FROM total_sales_metrics")
            
            query = """
                INSERT OR REPLACE INTO total_sales_metrics 
                (date, item_id, total_sales, total_units_ordered) 
                VALUES (?, ?, ?, ?)
            """
            
            await self.db_manager.execute_many(query, data)
            logger.info(f"Loaded {len(data)} total sales records")
            
        except Exception as e:
            logger.error(f"Error loading total sales data: {e}")
            raise
    
    async def get_summary_stats(self) -> Dict[str, Any]:
        """Get summary statistics of the loaded data"""
        try:
            stats = {}
            
            # Total sales
            result = await self.db_manager.execute_query(
                "SELECT SUM(total_sales) as total FROM total_sales_metrics"
            )
            stats['total_sales'] = result[0]['total'] if result else 0
            
            # Total ad spend
            result = await self.db_manager.execute_query(
                "SELECT SUM(ad_spend) as total FROM ad_sales_metrics"
            )
            stats['total_ad_spend'] = result[0]['total'] if result else 0
            
            # ROAS
            result = await self.db_manager.execute_query("""
                SELECT 
                    SUM(ad_sales) / NULLIF(SUM(ad_spend), 0) as roas
                FROM ad_sales_metrics 
                WHERE ad_spend > 0
            """)
            stats['roas'] = result[0]['roas'] if result and result[0]['roas'] else 0
            
            # Product counts
            result = await self.db_manager.execute_query(
                "SELECT COUNT(DISTINCT item_id) as count FROM total_sales_metrics"
            )
            stats['total_products'] = result[0]['count'] if result else 0
            
            result = await self.db_manager.execute_query(
                "SELECT COUNT(DISTINCT item_id) as count FROM product_eligibility WHERE eligibility = 1"
            )
            stats['eligible_products'] = result[0]['count'] if result else 0
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting summary stats: {e}")
            return {}
