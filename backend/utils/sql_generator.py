import re
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class SQLQueryGenerator:
    def __init__(self):
        self.table_schemas = {
            'product_eligibility': {
                'columns': ['eligibility_datetime_utc', 'item_id', 'eligibility', 'message'],
                'primary_key': ['eligibility_datetime_utc', 'item_id']
            },
            'ad_sales_metrics': {
                'columns': ['date', 'item_id', 'ad_sales', 'impressions', 'ad_spend', 'clicks', 'units_sold'],
                'primary_key': ['date', 'item_id']
            },
            'total_sales_metrics': {
                'columns': ['date', 'item_id', 'total_sales', 'total_units_ordered'],
                'primary_key': ['date', 'item_id']
            }
        }
        
        self.query_patterns = {
            'total_sales': self._generate_total_sales_query,
            'roas': self._generate_roas_query,
            'cpc': self._generate_cpc_query,
            'top_products': self._generate_top_products_query,
            'conversion_rate': self._generate_conversion_rate_query,
            'eligible_products': self._generate_eligible_products_query
        }

    def generate_query(self, question: str) -> str:
        """Generate SQL query based on natural language question"""
        question_lower = question.lower()
        
        for pattern, generator in self.query_patterns.items():
            if pattern in question_lower or any(keyword in question_lower for keyword in self._get_keywords(pattern)):
                return generator(question)
        
        return self._generate_generic_query(question)

    def _get_keywords(self, pattern: str) -> List[str]:
        """Get keywords associated with each query pattern"""
        keywords = {
            'total_sales': ['total sales', 'revenue', 'sales amount'],
            'roas': ['return on ad spend', 'advertising roi', 'ad return'],
            'cpc': ['cost per click', 'click cost', 'cost per click'],
            'top_products': ['top products', 'best selling', 'highest', 'best performers'],
            'conversion_rate': ['conversion', 'conversion rate', 'click to sale'],
            'eligible_products': ['eligible', 'eligibility', 'advertising eligible']
        }
        return keywords.get(pattern, [])

    def _generate_total_sales_query(self, question: str) -> str:
        """Generate query for total sales"""
        return """
        SELECT 
            SUM(total_sales) as total_sales,
            SUM(total_units_ordered) as total_units,
            COUNT(DISTINCT item_id) as unique_products
        FROM total_sales_metrics
        """

    def _generate_roas_query(self, question: str) -> str:
        """Generate query for ROAS calculation"""
        return """
        SELECT 
            SUM(ad_sales) / NULLIF(SUM(ad_spend), 0) as overall_roas,
            SUM(ad_sales) as total_ad_sales,
            SUM(ad_spend) as total_ad_spend,
            COUNT(DISTINCT item_id) as advertised_products
        FROM ad_sales_metrics 
        WHERE ad_spend > 0
        """

    def _generate_cpc_query(self, question: str) -> str:
        """Generate query for CPC analysis"""
        if 'highest' in question.lower():
            return """
            SELECT 
                item_id,
                SUM(ad_spend) / NULLIF(SUM(clicks), 0) as cpc,
                SUM(ad_spend) as total_spend,
                SUM(clicks) as total_clicks
            FROM ad_sales_metrics 
            WHERE clicks > 0
            GROUP BY item_id
            ORDER BY cpc DESC
            LIMIT 10
            """
        else:
            return """
            SELECT 
                AVG(ad_spend / NULLIF(clicks, 0)) as avg_cpc,
                MIN(ad_spend / NULLIF(clicks, 0)) as min_cpc,
                MAX(ad_spend / NULLIF(clicks, 0)) as max_cpc
            FROM ad_sales_metrics 
            WHERE clicks > 0
            """

    def _generate_top_products_query(self, question: str) -> str:
        """Generate query for top products"""
        return """
        SELECT 
            t.item_id,
            SUM(t.total_sales) as total_sales,
            SUM(t.total_units_ordered) as total_units,
            SUM(a.ad_sales) as ad_sales,
            SUM(a.ad_spend) as ad_spend
        FROM total_sales_metrics t
        LEFT JOIN ad_sales_metrics a ON t.item_id = a.item_id AND t.date = a.date
        GROUP BY t.item_id
        ORDER BY total_sales DESC
        LIMIT 10
        """

    def _generate_conversion_rate_query(self, question: str) -> str:
        """Generate query for conversion rate"""
        return """
        SELECT 
            item_id,
            (SUM(units_sold) * 100.0) / NULLIF(SUM(clicks), 0) as conversion_rate,
            SUM(clicks) as total_clicks,
            SUM(units_sold) as total_units_sold
        FROM ad_sales_metrics 
        WHERE clicks > 0
        GROUP BY item_id
        HAVING SUM(clicks) > 10
        ORDER BY conversion_rate DESC
        LIMIT 20
        """

    def _generate_eligible_products_query(self, question: str) -> str:
        """Generate query for product eligibility"""
        return """
        SELECT 
            eligibility,
            COUNT(*) as count,
            COUNT(*) * 100.0 / (SELECT COUNT(*) FROM product_eligibility) as percentage
        FROM product_eligibility
        GROUP BY eligibility
        """

    def _generate_generic_query(self, question: str) -> str:
        """Generate a generic query when no pattern matches"""
        return """
        SELECT 
            COUNT(DISTINCT t.item_id) as total_products,
            SUM(t.total_sales) as total_sales,
            SUM(a.ad_spend) as total_ad_spend
        FROM total_sales_metrics t
        LEFT JOIN ad_sales_metrics a ON t.item_id = a.item_id
        """

    def validate_query(self, query: str) -> bool:
        """Validate SQL query for safety"""
        dangerous_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'CREATE', 'TRUNCATE']
        query_upper = query.upper()
        
        for keyword in dangerous_keywords:
            if keyword in query_upper:
                logger.warning(f"Dangerous keyword '{keyword}' found in query")
                return False
        
        return True
