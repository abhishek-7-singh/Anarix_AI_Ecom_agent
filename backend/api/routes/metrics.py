from fastapi import APIRouter, HTTPException
import logging
from typing import Dict, Any

from core.models import MetricsSummary
from core.database import DatabaseManager

router = APIRouter()
logger = logging.getLogger(__name__)

db_manager = DatabaseManager()

@router.get("/metrics/summary", response_model=MetricsSummary)
async def get_summary_metrics():
    """Get overall business metrics summary"""
    try:
        metrics = {}
        
        # Total sales
        result = await db_manager.execute_query(
            "SELECT SUM(total_sales) as total FROM total_sales_metrics"
        )
        metrics['total_sales'] = float(result[0]['total'] or 0)
        
        # Total ad spend
        result = await db_manager.execute_query(
            "SELECT SUM(ad_spend) as total FROM ad_sales_metrics"
        )
        metrics['total_ad_spend'] = float(result[0]['total'] or 0)
        
        # Overall ROAS
        result = await db_manager.execute_query("""
            SELECT 
                SUM(ad_sales) / NULLIF(SUM(ad_spend), 0) as roas
            FROM ad_sales_metrics 
            WHERE ad_spend > 0
        """)
        metrics['total_roas'] = float(result[0]['roas'] or 0)
        
        # Product counts
        result = await db_manager.execute_query(
            "SELECT COUNT(DISTINCT item_id) as count FROM total_sales_metrics"
        )
        metrics['total_products'] = int(result[0]['count'] or 0)
        
        result = await db_manager.execute_query("""
            SELECT COUNT(DISTINCT item_id) as count 
            FROM product_eligibility 
            WHERE eligibility = 1
        """)
        metrics['eligible_products'] = int(result[0]['count'] or 0)
        
        # Top performing product
        result = await db_manager.execute_query("""
            SELECT item_id, SUM(total_sales) as sales
            FROM total_sales_metrics
            GROUP BY item_id
            ORDER BY sales DESC
            LIMIT 1
        """)
        metrics['top_performing_product'] = str(result[0]['item_id']) if result else None
        
        return MetricsSummary(**metrics)
        
    except Exception as e:
        logger.error(f"Error getting summary metrics: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get metrics: {str(e)}")

@router.get("/metrics/performance")
async def get_performance_metrics():
    """Get detailed performance metrics"""
    try:
        metrics = {}
        
        # ROAS by product (top 10)
        result = await db_manager.execute_query("""
            SELECT 
                item_id,
                SUM(ad_sales) as total_ad_sales,
                SUM(ad_spend) as total_ad_spend,
                SUM(ad_sales) / NULLIF(SUM(ad_spend), 0) as roas
            FROM ad_sales_metrics 
            WHERE ad_spend > 0
            GROUP BY item_id
            ORDER BY roas DESC
            LIMIT 10
        """)
        metrics['top_roas_products'] = result
        
        # CPC by product (top 10)
        result = await db_manager.execute_query("""
            SELECT 
                item_id,
                SUM(ad_spend) as total_spend,
                SUM(clicks) as total_clicks,
                SUM(ad_spend) / NULLIF(SUM(clicks), 0) as cpc
            FROM ad_sales_metrics 
            WHERE clicks > 0
            GROUP BY item_id
            ORDER BY cpc DESC
            LIMIT 10
        """)
        metrics['highest_cpc_products'] = result
        
        # Conversion rates
        result = await db_manager.execute_query("""
            SELECT 
                item_id,
                SUM(clicks) as total_clicks,
                SUM(units_sold) as total_units,
                (SUM(units_sold) * 100.0) / NULLIF(SUM(clicks), 0) as conversion_rate
            FROM ad_sales_metrics 
            WHERE clicks > 0
            GROUP BY item_id
            ORDER BY conversion_rate DESC
            LIMIT 10
        """)
        metrics['best_conversion_rates'] = result
        
        # Click-through rates
        result = await db_manager.execute_query("""
            SELECT 
                item_id,
                SUM(impressions) as total_impressions,
                SUM(clicks) as total_clicks,
                (SUM(clicks) * 100.0) / NULLIF(SUM(impressions), 0) as ctr
            FROM ad_sales_metrics 
            WHERE impressions > 0
            GROUP BY item_id
            ORDER BY ctr DESC
            LIMIT 10
        """)
        metrics['best_ctr_products'] = result
        
        return metrics
        
    except Exception as e:
        logger.error(f"Error getting performance metrics: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get performance metrics: {str(e)}")

@router.get("/metrics/trends")
async def get_trend_metrics():
    """Get trend data over time"""
    try:
        # Sales trends
        sales_trends = await db_manager.execute_query("""
            SELECT 
                date,
                SUM(total_sales) as daily_sales,
                SUM(total_units_ordered) as daily_units
            FROM total_sales_metrics
            GROUP BY date
            ORDER BY date
        """)
        
        # Ad performance trends
        ad_trends = await db_manager.execute_query("""
            SELECT 
                date,
                SUM(ad_sales) as daily_ad_sales,
                SUM(ad_spend) as daily_ad_spend,
                SUM(impressions) as daily_impressions,
                SUM(clicks) as daily_clicks
            FROM ad_sales_metrics
            GROUP BY date
            ORDER BY date
        """)
        
        return {
            "sales_trends": sales_trends,
            "ad_trends": ad_trends
        }
        
    except Exception as e:
        logger.error(f"Error getting trend metrics: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get trend metrics: {str(e)}")

@router.get("/metrics/products/{item_id}")
async def get_product_metrics(item_id: int):
    """Get detailed metrics for a specific product"""
    try:
        # Product eligibility
        eligibility = await db_manager.execute_query(
            "SELECT * FROM product_eligibility WHERE item_id = ? ORDER BY eligibility_datetime_utc DESC LIMIT 1",
            (item_id,)
        )
        
        # Sales metrics
        sales_metrics = await db_manager.execute_query(
            "SELECT * FROM total_sales_metrics WHERE item_id = ? ORDER BY date",
            (item_id,)
        )
        
        # Ad metrics
        ad_metrics = await db_manager.execute_query(
            "SELECT * FROM ad_sales_metrics WHERE item_id = ? ORDER BY date",
            (item_id,)
        )
        
        # Summary stats for this product
        summary = await db_manager.execute_query("""
            SELECT 
                ts.item_id,
                SUM(ts.total_sales) as total_sales,
                SUM(ts.total_units_ordered) as total_units,
                SUM(ads.ad_sales) as total_ad_sales,
                SUM(ads.ad_spend) as total_ad_spend,
                SUM(ads.impressions) as total_impressions,
                SUM(ads.clicks) as total_clicks,
                SUM(ads.units_sold) as total_ad_units,
                SUM(ads.ad_sales) / NULLIF(SUM(ads.ad_spend), 0) as roas,
                SUM(ads.ad_spend) / NULLIF(SUM(ads.clicks), 0) as cpc,
                (SUM(ads.clicks) * 100.0) / NULLIF(SUM(ads.impressions), 0) as ctr,
                (SUM(ads.units_sold) * 100.0) / NULLIF(SUM(ads.clicks), 0) as conversion_rate
            FROM total_sales_metrics ts
            LEFT JOIN ad_sales_metrics ads ON ts.item_id = ads.item_id AND ts.date = ads.date
            WHERE ts.item_id = ?
            GROUP BY ts.item_id
        """, (item_id,))
        
        return {
            "item_id": item_id,
            "eligibility": eligibility[0] if eligibility else None,
            "sales_data": sales_metrics,
            "ad_data": ad_metrics,
            "summary": summary[0] if summary else None
        }
        
    except Exception as e:
        logger.error(f"Error getting product metrics: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get product metrics: {str(e)}")
