from fastapi import APIRouter, HTTPException
import asyncio
import time
import logging
from typing import Dict, Any

from core.database import DatabaseManager

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/health")
async def health_check():
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "service": "E-commerce AI Agent"
    }

@router.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check including database connectivity"""
    health_info = {
        "status": "healthy",
        "timestamp": time.time(),
        "service": "E-commerce AI Agent",
        "checks": {}
    }
    
    try:
        # Database connectivity check
        db_manager = DatabaseManager()
        start_time = time.time()
        
        result = await db_manager.execute_query("SELECT 1 as test")
        db_response_time = time.time() - start_time
        
        health_info["checks"]["database"] = {
            "status": "healthy",
            "response_time": db_response_time,
            "message": "Database connection successful"
        }
        
        # Check table existence and data
        tables = await db_manager.get_all_tables()
        required_tables = ["product_eligibility", "ad_sales_metrics", "total_sales_metrics"]
        
        missing_tables = [table for table in required_tables if table not in tables]
        
        if missing_tables:
            health_info["checks"]["tables"] = {
                "status": "warning",
                "message": f"Missing tables: {missing_tables}"
            }
        else:
            health_info["checks"]["tables"] = {
                "status": "healthy",
                "message": "All required tables present"
            }
        
        # Check data counts
        data_counts = {}
        for table in required_tables:
            if table in tables:
                result = await db_manager.execute_query(f"SELECT COUNT(*) as count FROM {table}")
                data_counts[table] = result[0]['count'] if result else 0
        
        health_info["checks"]["data"] = {
            "status": "healthy",
            "counts": data_counts
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        health_info["status"] = "unhealthy"
        health_info["checks"]["database"] = {
            "status": "unhealthy",
            "error": str(e)
        }
    
    return health_info

@router.get("/health/metrics")
async def health_metrics():
    """Get health metrics for monitoring"""
    try:
        db_manager = DatabaseManager()
        
        # Basic counts
        metrics = {}
        
        # Record counts
        result = await db_manager.execute_query("SELECT COUNT(*) as count FROM product_eligibility")
        metrics['eligibility_records'] = result[0]['count'] if result else 0
        
        result = await db_manager.execute_query("SELECT COUNT(*) as count FROM ad_sales_metrics")
        metrics['ad_sales_records'] = result[0]['count'] if result else 0
        
        result = await db_manager.execute_query("SELECT COUNT(*) as count FROM total_sales_metrics")
        metrics['total_sales_records'] = result[0]['count'] if result else 0
        
        # Unique products
        result = await db_manager.execute_query("SELECT COUNT(DISTINCT item_id) as count FROM total_sales_metrics")
        metrics['unique_products'] = result[0]['count'] if result else 0
        
        # Date ranges
        result = await db_manager.execute_query("SELECT MIN(date) as min_date, MAX(date) as max_date FROM total_sales_metrics")
        if result and result[0]['min_date']:
            metrics['date_range'] = {
                'start': result[0]['min_date'],
                'end': result[0]['max_date']
            }
        
        return {
            "status": "healthy",
            "metrics": metrics,
            "timestamp": time.time()
        }
        
    except Exception as e:
        logger.error(f"Error getting health metrics: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get health metrics: {str(e)}")
