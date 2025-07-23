from typing import Dict, List, Any, Optional
import json
import logging

logger = logging.getLogger(__name__)

class ResponseFormatter:
    def __init__(self):
        self.number_formatters = {
            'currency': self._format_currency,
            'percentage': self._format_percentage,
            'decimal': self._format_decimal,
            'integer': self._format_integer
        }

    def format_query_response(self, question: str, results: List[Dict[str, Any]]) -> str:
        """Format query results into human-readable response"""
        if not results:
            return "No data found for your query."

        question_lower = question.lower()
        
        # Determine response type based on question
        if 'total sales' in question_lower:
            return self._format_sales_response(results)
        elif 'roas' in question_lower:
            return self._format_roas_response(results)
        elif 'cpc' in question_lower:
            return self._format_cpc_response(results)
        elif 'top' in question_lower and 'product' in question_lower:
            return self._format_top_products_response(results)
        elif 'conversion' in question_lower:
            return self._format_conversion_response(results)
        elif 'eligible' in question_lower:
            return self._format_eligibility_response(results)
        else:
            return self._format_generic_response(results)

    def _format_sales_response(self, results: List[Dict]) -> str:
        """Format total sales response"""
        data = results[0]
        total_sales = data.get('total_sales', 0)
        total_units = data.get('total_units', 0)
        unique_products = data.get('unique_products', 0)
        
        return f"""Your total sales performance:
        
• **Total Revenue**: {self._format_currency(total_sales)}
• **Units Sold**: {self._format_integer(total_units)} units
• **Active Products**: {unique_products} products
• **Average Revenue per Product**: {self._format_currency(total_sales / max(unique_products, 1))}

This represents your overall sales performance across all products and time periods."""

    def _format_roas_response(self, results: List[Dict]) -> str:
        """Format ROAS response"""
        data = results[0]
        roas = data.get('overall_roas', 0)
        ad_sales = data.get('total_ad_sales', 0)
        ad_spend = data.get('total_ad_spend', 0)
        
        return f"""Your advertising Return on Ad Spend (ROAS):
        
• **Overall ROAS**: {self._format_decimal(roas, 2)}x
• **Ad Sales Revenue**: {self._format_currency(ad_sales)}
• **Total Ad Spend**: {self._format_currency(ad_spend)}
• **Net Profit**: {self._format_currency(ad_sales - ad_spend)}

A ROAS of {self._format_decimal(roas, 2)}x means you earn ${self._format_decimal(roas, 2)} for every $1 spent on advertising."""

    def _format_cpc_response(self, results: List[Dict]) -> str:
        """Format CPC response"""
        if len(results) == 1 and 'avg_cpc' in results[0]:
            # Average CPC response
            data = results[0]
            return f"""Your Cost Per Click (CPC) metrics:
            
• **Average CPC**: {self._format_currency(data.get('avg_cpc', 0))}
• **Lowest CPC**: {self._format_currency(data.get('min_cpc', 0))}
• **Highest CPC**: {self._format_currency(data.get('max_cpc', 0))}"""
        else:
            # Top CPC products
            response = "**Products with Highest Cost Per Click (CPC):**\n\n"
            for i, item in enumerate(results[:10], 1):
                cpc = item.get('cpc', 0)
                clicks = item.get('total_clicks', 0)
                spend = item.get('total_spend', 0)
                
                response += f"{i}. **Product {item.get('item_id')}**\n"
                response += f"   • CPC: {self._format_currency(cpc)}\n"
                response += f"   • Total Clicks: {self._format_integer(clicks)}\n"
                response += f"   • Total Spend: {self._format_currency(spend)}\n\n"
            
            return response

    def _format_top_products_response(self, results: List[Dict]) -> str:
        """Format top products response"""
        response = "**Top Performing Products by Revenue:**\n\n"
        
        for i, product in enumerate(results[:10], 1):
            item_id = product.get('item_id')
            total_sales = product.get('total_sales', 0)
            total_units = product.get('total_units', 0)
            ad_sales = product.get('ad_sales', 0) or 0
            ad_spend = product.get('ad_spend', 0) or 0
            
            response += f"**#{i} Product {item_id}**\n"
            response += f"• Total Sales: {self._format_currency(total_sales)}\n"
            response += f"• Units Sold: {self._format_integer(total_units)}\n"
            
            if ad_sales > 0:
                response += f"• Ad Revenue: {self._format_currency(ad_sales)}\n"
                response += f"• Ad Spend: {self._format_currency(ad_spend)}\n"
                if ad_spend > 0:
                    roas = ad_sales / ad_spend
                    response += f"• ROAS: {self._format_decimal(roas, 2)}x\n"
            
            response += "\n"
        
        return response

    def _format_conversion_response(self, results: List[Dict]) -> str:
        """Format conversion rate response"""
        response = "**Products with Best Conversion Rates:**\n\n"
        
        for i, product in enumerate(results[:10], 1):
            item_id = product.get('item_id')
            conversion_rate = product.get('conversion_rate', 0)
            clicks = product.get('total_clicks', 0)
            units_sold = product.get('total_units_sold', 0)
            
            response += f"**#{i} Product {item_id}**\n"
            response += f"• Conversion Rate: {self._format_percentage(conversion_rate)}%\n"
            response += f"• Total Clicks: {self._format_integer(clicks)}\n"
            response += f"• Units Sold: {self._format_integer(units_sold)}\n\n"
        
        return response

    def _format_eligibility_response(self, results: List[Dict]) -> str:
        """Format eligibility response"""
        response = "**Product Advertising Eligibility Status:**\n\n"
        
        total_products = sum(item.get('count', 0) for item in results)
        
        for item in results:
            eligible = item.get('eligibility')
            count = item.get('count', 0)
            percentage = item.get('percentage', 0)
            
            status = "✅ Eligible" if eligible else "❌ Not Eligible"
            response += f"• {status}: {count} products ({self._format_percentage(percentage)}%)\n"
        
        response += f"\n**Total Products Analyzed**: {total_products}"
        
        return response

    def _format_generic_response(self, results: List[Dict]) -> str:
        """Format generic response"""
        if len(results) == 1:
            data = results[0]
            response = "**Query Results:**\n\n"
            for key, value in data.items():
                formatted_key = key.replace('_', ' ').title()
                if isinstance(value, (int, float)):
                    if 'sales' in key.lower() or 'spend' in key.lower() or 'revenue' in key.lower():
                        formatted_value = self._format_currency(value)
                    elif 'rate' in key.lower() or 'percentage' in key.lower():
                        formatted_value = f"{self._format_percentage(value)}%"
                    else:
                        formatted_value = self._format_integer(value) if isinstance(value, int) else self._format_decimal(value, 2)
                else:
                    formatted_value = str(value)
                
                response += f"• {formatted_key}: {formatted_value}\n"
        else:
            response = f"Found {len(results)} results:\n\n"
            for i, item in enumerate(results[:10], 1):
                response += f"**Result {i}:**\n"
                for key, value in item.items():
                    response += f"  • {key}: {value}\n"
                response += "\n"
        
        return response

    def _format_currency(self, value: float) -> str:
        """Format value as currency"""
        if value is None:
            return "$0.00"
        return f"${value:,.2f}"

    def _format_percentage(self, value: float) -> str:
        """Format value as percentage"""
        if value is None:
            return "0.00"
        return f"{value:.2f}"

    def _format_decimal(self, value: float, places: int = 2) -> str:
        """Format value as decimal"""
        if value is None:
            return "0.00"
        return f"{value:.{places}f}"

    def _format_integer(self, value: int) -> str:
        """Format value as integer with commas"""
        if value is None:
            return "0"
        return f"{int(value):,}"
