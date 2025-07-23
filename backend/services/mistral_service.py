# import asyncio
# import subprocess
# import json
# import logging
# import re
# from typing import List, Dict, Any
# from config import OLLAMA_MODEL

# logger = logging.getLogger(__name__)

# class MistralService:
#     def __init__(self):
#         self.model = OLLAMA_MODEL or "mistral:7b-instruct"
#         self.schema_context = self._get_schema_context()
    
#     def _get_schema_context(self) -> str:
#         """Get database schema context for the LLM"""
#         return """
#         Database Schema:
        
#         1. product_eligibility table:
#            - eligibility_datetime_utc (TEXT): Timestamp of eligibility check
#            - item_id (INTEGER): Product identifier
#            - eligibility (BOOLEAN): Whether product is eligible for ads
#            - message (TEXT): Eligibility message or reason
        
#         2. ad_sales_metrics table:
#            - date (TEXT): Date of metrics
#            - item_id (INTEGER): Product identifier
#            - ad_sales (REAL): Revenue from ads
#            - impressions (INTEGER): Number of ad impressions
#            - ad_spend (REAL): Amount spent on ads
#            - clicks (INTEGER): Number of ad clicks
#            - units_sold (INTEGER): Units sold through ads
        
#         3. total_sales_metrics table:
#            - date (TEXT): Date of metrics
#            - item_id (INTEGER): Product identifier
#            - total_sales (REAL): Total revenue
#            - total_units_ordered (INTEGER): Total units ordered
        
#         Common calculations:
#         - ROAS (Return on Ad Spend) = ad_sales / ad_spend
#         - CPC (Cost Per Click) = ad_spend / clicks
#         - CTR (Click Through Rate) = clicks / impressions
#         - Conversion Rate = units_sold / clicks
#         """
    
#     async def generate_sql(self, question: str) -> str:
#         """Convert natural language question to SQL query"""
        
#         prompt = f"""
#         {self.schema_context}
        
#         Convert this natural language question to a SQL query:
#         Question: {question}
        
#         Rules:
#         1. Return ONLY the SQL query, no explanation
#         2. Use proper JOIN syntax when needed
#         3. Include appropriate WHERE clauses for filtering
#         4. Use aggregate functions (SUM, AVG, COUNT) when appropriate
#         5. Limit results to reasonable numbers (e.g., TOP 10)
#         6. Handle potential NULL values with NULLIF
        
#         SQL Query:
#         """
        
#         try:
#             result = await self._call_mistral_async(prompt)
#             sql_query = self._extract_sql(result)
#             logger.info(f"Generated SQL: {sql_query}")
#             return sql_query
            
#         except Exception as e:
#             logger.error(f"Error generating SQL: {e}")
#             # Fallback to basic queries based on keywords
#             return self._fallback_sql(question)
    
#     async def generate_response(self, question: str, sql_query: str, results: List[Dict]) -> str:
#         """Generate human-readable response from query results"""
        
#         # Format results for better readability
#         formatted_results = self._format_results(results)
        
#         prompt = f"""
#         Question: {question}
#         SQL Query: {sql_query}
#         Results: {formatted_results}
        
#         Provide a clear, conversational answer to the question based on the results.
#         Include specific numbers and insights.
#         If there are no results, explain what this means.
#         Keep the response concise but informative.
        
#         Response:
#         """
        
#         try:
#             response = await self._call_mistral_async(prompt)
#             return response.strip()
            
#         except Exception as e:
#             logger.error(f"Error generating response: {e}")
#             return self._fallback_response(question, results)
    
#     async def _call_mistral_async(self, prompt: str) -> str:
#         """Call Mistral model via Ollama with proper async handling"""
#         try:
#             # Use asyncio subprocess for proper async handling
#             process = await asyncio.create_subprocess_exec(
#                 'ollama', 'run', self.model,
#                 stdin=asyncio.subprocess.PIPE,
#                 stdout=asyncio.subprocess.PIPE,
#                 stderr=asyncio.subprocess.PIPE
#             )
            
#             # Send prompt and get response
#             stdout, stderr = await process.communicate(prompt.encode('utf-8'))
            
#             if process.returncode == 0:
#                 response = stdout.decode('utf-8').strip()
#                 logger.info("Mistral responded successfully")
#                 return response
#             else:
#                 error_msg = stderr.decode('utf-8').strip()
#                 logger.error(f"Ollama process failed: {error_msg}")
#                 raise Exception(f"Ollama error: {error_msg}")
                
#         except Exception as e:
#             logger.error(f"Error calling Mistral: {e}")
#             raise
    
#     def _extract_sql(self, text: str) -> str:
#         """Extract SQL query from LLM response"""
#         # Remove common markdown formatting - FIXED
        
#         text = re.sub(r'```\n?', '', text)
        
#         # Look for SQL patterns
#         sql_patterns = [
#             r'SELECT.*?(?:;|$)',
#             r'WITH.*?SELECT.*?(?:;|$)',
#         ]
        
#         for pattern in sql_patterns:
#             match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
#             if match:
#                 sql = match.group(0).strip()
#                 if sql.endswith(';'):
#                     sql = sql[:-1]
#                 return sql
        
#         # If no pattern found, clean and return
#         lines = text.split('\n')
#         for line in lines:
#             line = line.strip()
#             if line.upper().startswith(('SELECT', 'WITH')):
#                 if line.endswith(';'):
#                     line = line[:-1]
#                 return line
        
#         # Last resort - return cleaned text
#         cleaned = text.strip()
#         if cleaned.endswith(';'):
#             cleaned = cleaned[:-1]
#         return cleaned
    
#     def _format_results(self, results: List[Dict]) -> str:
#         """Format query results for LLM consumption"""
#         if not results:
#             return "No results found"
        
#         if len(results) > 5:
#             formatted = json.dumps(results[:5], indent=2, default=str)
#             formatted += f"\n... and {len(results) - 5} more rows"
#         else:
#             formatted = json.dumps(results, indent=2, default=str)
        
#         return formatted
    
#     def _fallback_sql(self, question: str) -> str:
#         """Generate fallback SQL queries based on keywords"""
#         question_lower = question.lower()
        
#         if 'total sales' in question_lower:
#             return "SELECT SUM(total_sales) as total_sales FROM total_sales_metrics"
#         elif 'roas' in question_lower or 'return on ad spend' in question_lower:
#             return """
#                 SELECT 
#                     SUM(ad_sales) / NULLIF(SUM(ad_spend), 0) as roas,
#                     SUM(ad_sales) as total_ad_sales,
#                     SUM(ad_spend) as total_ad_spend
#                 FROM ad_sales_metrics 
#                 WHERE ad_spend > 0
#             """
#         elif 'cpc' in question_lower or 'cost per click' in question_lower:
#             return """
#                 SELECT 
#                     item_id,
#                     SUM(ad_spend) / NULLIF(SUM(clicks), 0) as cpc,
#                     SUM(ad_spend) as total_spend,
#                     SUM(clicks) as total_clicks
#                 FROM ad_sales_metrics 
#                 WHERE clicks > 0 
#                 GROUP BY item_id
#                 ORDER BY cpc DESC 
#                 LIMIT 10
#             """
#         elif 'top' in question_lower and 'product' in question_lower:
#             return """
#                 SELECT 
#                     item_id,
#                     SUM(total_sales) as total_sales,
#                     SUM(total_units_ordered) as total_units
#                 FROM total_sales_metrics 
#                 GROUP BY item_id 
#                 ORDER BY total_sales DESC 
#                 LIMIT 10
#             """
#         else:
#             return "SELECT COUNT(*) as total_records FROM total_sales_metrics"
    
#     def _fallback_response(self, question: str, results: List[Dict]) -> str:
#         """Generate fallback response when LLM fails"""
#         if not results:
#             return f"No data found for your question: '{question}'"
        
#         question_lower = question.lower()
        
#         if 'total sales' in question_lower and results:
#             total = results[0].get('total_sales', 0)
#             return f"Your total sales amount to ${total:,.2f}"
        
#         elif 'roas' in question_lower and results:
#             data = results[0]
#             roas = data.get('roas', 0)
#             return f"Your Return on Ad Spend (ROAS) is {roas:.2f}x"
        
#         elif 'cpc' in question_lower and results:
#             if results:
#                 item = results[0]
#                 cpc = item.get('cpc', 0)
#                 item_id = item.get('item_id', 'Unknown')
#                 return f"Product {item_id} has the highest CPC at ${cpc:.2f} per click"
        
#         return f"Found {len(results)} results for your query: '{question}'"






# import asyncio
# import subprocess
# import json
# import logging
# import re
# import requests
# from typing import List, Dict, Any
# from config import OLLAMA_MODEL

# logger = logging.getLogger(__name__)

# class MistralService:
#     def __init__(self):
#         self.model = OLLAMA_MODEL or "mistral:7b-instruct"
#         self.ollama_url = "http://localhost:11434/api/generate"
#         self.schema_context = self._get_schema_context()
    
#     def _get_schema_context(self) -> str:
#         """Get simplified database schema context"""
#         return """
#         Table 'product_eligibility' has columns: eligibility_datetime_utc, item_id, eligibility, message
#         Table 'ad_sales_metrics' has columns: date, item_id, ad_sales, impressions, ad_spend, clicks, units_sold
#         Table 'total_sales_metrics' has columns: date, item_id, total_sales, total_units_ordered
#         """
    
#     def _clean_sql_from_response(self, raw_response: str) -> str:
#         """
#         Cleans the raw LLM output by finding all SQL queries and returning only the last one.
#         """
#         # Find all snippets that look like SQL queries ending with a semicolon
#         queries = re.findall(r'SELECT.*?;', raw_response, re.IGNORECASE | re.DOTALL)
        
#         if not queries:
#             # Fallback for queries that don't end with a semicolon
#             queries = re.findall(r'SELECT.*', raw_response, re.IGNORECASE | re.DOTALL)
#             if not queries:
#                 return ""

#         last_query = queries[-1].strip()
#         return last_query
    
#     async def generate_sql(self, question: str) -> str:
#         """
#         Generate SQL query using improved prompt engineering from Streamlit version
#         """
#         prompt = f"""You are an expert SQLite data analyst.
# Given the following database schema:
# {self.schema_context}

# Here is an example of how to answer a question:
# Question: "What were the top 5 products by total sales?"
# SQL Query:
# SELECT
#   item_id,
#   SUM(total_sales) AS total_sales_amount
# FROM total_sales_metrics
# GROUP BY
#   item_id
# ORDER BY
#   total_sales_amount DESC
# LIMIT 5;

# ---

# Now, please answer this new question.
# Question: "{question}"
# Your response MUST contain ONLY the SQL query.
# SQL Query:
# """
        
#         try:
#             payload = {
#                 "model": self.model,
#                 "prompt": prompt,
#                 "stream": False,
#                 "options": {
#                     "temperature": 0.0  # Key improvement: deterministic output
#                 }
#             }
            
#             response = requests.post(self.ollama_url, json=payload, timeout=30)
#             response.raise_for_status()
            
#             response_data = response.json()
#             raw_response = response_data.get("response", "")
            
#             sql_query = self._clean_sql_from_response(raw_response)
            
#             if not sql_query or len(sql_query.split()) < 3:
#                 logger.error(f"Failed to generate complete SQL. Raw response: {raw_response}")
#                 return self._fallback_sql(question)
            
#             logger.info(f"Generated SQL: {sql_query}")
#             return sql_query
            
#         except Exception as e:
#             logger.error(f"Error generating SQL: {e}")
#             return self._fallback_sql(question)
    
#     async def generate_response(self, question: str, sql_query: str, results: List[Dict]) -> str:
#         """Generate human-readable response"""
#         formatted_results = self._format_results(results)
        
#         prompt = f"""Based on the SQL query results, provide a clear business answer.

# Question: {question}
# SQL Query: {sql_query}
# Results: {formatted_results}

# Provide a concise, business-friendly answer with specific numbers and insights.
# """
        
#         try:
#             payload = {
#                 "model": self.model,
#                 "prompt": prompt,
#                 "stream": False,
#                 "options": {
#                     "temperature": 0.3
#                 }
#             }
            
#             response = requests.post(self.ollama_url, json=payload, timeout=30)
#             response.raise_for_status()
            
#             response_data = response.json()
#             return response_data.get("response", "").strip()
            
#         except Exception as e:
#             logger.error(f"Error generating response: {e}")
#             return self._fallback_response(question, results)
    
#     def _format_results(self, results: List[Dict]) -> str:
#         """Format query results for LLM consumption"""
#         if not results:
#             return "No results found"
        
#         if len(results) > 5:
#             formatted = json.dumps(results[:5], indent=2, default=str)
#             formatted += f"\n... and {len(results) - 5} more rows"
#         else:
#             formatted = json.dumps(results, indent=2, default=str)
        
#         return formatted
    
#     def _fallback_sql(self, question: str) -> str:
#         """Generate fallback SQL queries based on keywords"""
#         question_lower = question.lower()
        
#         if 'total sales' in question_lower:
#             return "SELECT SUM(total_sales) as total_sales FROM total_sales_metrics"
#         elif 'roas' in question_lower or 'return on ad spend' in question_lower:
#             return """
#                 SELECT 
#                     SUM(ad_sales) / NULLIF(SUM(ad_spend), 0) as roas,
#                     SUM(ad_sales) as total_ad_sales,
#                     SUM(ad_spend) as total_ad_spend
#                 FROM ad_sales_metrics 
#                 WHERE ad_spend > 0
#             """
#         elif 'cpc' in question_lower or 'cost per click' in question_lower:
#             return """
#                 SELECT 
#                     item_id,
#                     SUM(ad_spend) / NULLIF(SUM(clicks), 0) as cpc,
#                     SUM(ad_spend) as total_spend,
#                     SUM(clicks) as total_clicks
#                 FROM ad_sales_metrics 
#                 WHERE clicks > 0 
#                 GROUP BY item_id
#                 ORDER BY cpc DESC 
#                 LIMIT 10
#             """
#         elif 'top' in question_lower and 'product' in question_lower:
#             return """
#                 SELECT 
#                     item_id,
#                     SUM(total_sales) as total_sales,
#                     SUM(total_units_ordered) as total_units
#                 FROM total_sales_metrics 
#                 GROUP BY item_id 
#                 ORDER BY total_sales DESC 
#                 LIMIT 10
#             """
#         else:
#             return "SELECT COUNT(*) as total_records FROM total_sales_metrics"
    
#     def _fallback_response(self, question: str, results: List[Dict]) -> str:
#         """Generate fallback response when LLM fails"""
#         if not results:
#             return f"No data found for your question: '{question}'"
        
#         question_lower = question.lower()
        
#         if 'total sales' in question_lower and results:
#             total = results[0].get('total_sales', 0)
#             return f"Your total sales amount to ${total:,.2f}"
        
#         elif 'roas' in question_lower and results:
#             data = results[0]
#             roas = data.get('roas', 0)
#             return f"Your Return on Ad Spend (ROAS) is {roas:.2f}x"
        
#         elif 'cpc' in question_lower and results:
#             if results:
#                 item = results[0]
#                 cpc = item.get('cpc', 0)
#                 item_id = item.get('item_id', 'Unknown')
#                 return f"Product {item_id} has the highest CPC at ${cpc:.2f} per click"
        
#         return f"Found {len(results)} results for your query: '{question}'"






# import asyncio
# import subprocess
# import json
# import logging
# import re
# import requests
# from typing import List, Dict, Any, Optional, Tuple
# from config import OLLAMA_MODEL

# logger = logging.getLogger(__name__)

# class MistralService:
#     def __init__(self):
#         self.model = OLLAMA_MODEL or "mistral:7b-instruct"
#         self.ollama_url = "http://localhost:11434/api/generate"
#         self.schema_context = self._get_schema_context()
    
#     def _get_schema_context(self) -> str:
#         """Get enhanced database schema context with proper aliasing examples"""
#         return """
#         Database Schema:
        
#         Table 'product_eligibility' has columns: eligibility_datetime_utc, item_id, eligibility, message
#         Table 'ad_sales_metrics' has columns: date, item_id, ad_sales, impressions, ad_spend, clicks, units_sold
#         Table 'total_sales_metrics' has columns: date, item_id, total_sales, total_units_ordered
        
#         IMPORTANT SQL RULES:
#         1. Always use table aliases when joining multiple tables
#         2. Always qualify column names with table aliases to avoid ambiguity
#         3. Use proper JOIN syntax with ON clauses instead of USING when possible
#         4. Handle NULL values with NULLIF for division operations
        
#         Example of CORRECT multi-table query:
#         SELECT 
#             a.item_id,
#             SUM(a.ad_sales) / NULLIF(SUM(a.ad_spend), 0) as roas,
#             SUM(t.total_sales) as total_sales
#         FROM ad_sales_metrics a
#         JOIN total_sales_metrics t ON a.item_id = t.item_id
#         GROUP BY a.item_id
#         ORDER BY roas DESC;
#         """
    
#     def _clean_sql_from_response(self, raw_response: str) -> str:
#         """
#         Cleans the raw LLM output by finding all SQL queries and returning only the last one.
#         """
#         # Find all snippets that look like SQL queries ending with a semicolon
#         queries = re.findall(r'SELECT.*?;', raw_response, re.IGNORECASE | re.DOTALL)
        
#         if not queries:
#             # Fallback for queries that don't end with a semicolon
#             queries = re.findall(r'SELECT.*', raw_response, re.IGNORECASE | re.DOTALL)
#             if not queries:
#                 return ""

#         last_query = queries[-1].strip()
        
#         # Remove trailing semicolon for consistency
#         if last_query.endswith(';'):
#             last_query = last_query[:-1]
            
#         return last_query
    
#     def _validate_and_fix_sql(self, sql_query: str) -> Tuple[str, Optional[str]]:
#         """Validate and fix common SQL issues like ambiguous column references"""
        
#         # Check for ambiguous column references when JOINs are present
#         if 'item_id' in sql_query and 'JOIN' in sql_query.upper():
#             # Look for unqualified item_id references
#             unqualified_pattern = r'(?<![a-zA-Z_.])\bitem_id\b'
#             if re.search(unqualified_pattern, sql_query):
#                 logger.warning("Detected potentially ambiguous item_id reference, attempting to fix...")
                
#                 # Try to fix automatically by adding proper aliases
#                 fixed_query = self._fix_ambiguous_columns(sql_query)
#                 if fixed_query != sql_query:
#                     logger.info(f"Fixed ambiguous query: {fixed_query}")
#                     return fixed_query, None
        
#         return sql_query, None
    
#     def _fix_ambiguous_columns(self, sql_query: str) -> str:
#         """Fix ambiguous column references by adding proper table aliases"""
        
#         # Add aliases to table names if not present
#         if 'ad_sales_metrics' in sql_query and 'ad_sales_metrics a' not in sql_query:
#             sql_query = sql_query.replace('ad_sales_metrics', 'ad_sales_metrics a')
        
#         if 'total_sales_metrics' in sql_query and 'total_sales_metrics t' not in sql_query:
#             sql_query = sql_query.replace('total_sales_metrics', 'total_sales_metrics t')
        
#         if 'product_eligibility' in sql_query and 'product_eligibility p' not in sql_query:
#             sql_query = sql_query.replace('product_eligibility', 'product_eligibility p')
        
#         # Fix unqualified column references
#         # Replace unqualified item_id with qualified version (prefer ad_sales table)
#         sql_query = re.sub(r'(?<![a-zA-Z_.])\bitem_id\b', 'a.item_id', sql_query)
        
#         # Fix other common column ambiguities
#         sql_query = re.sub(r'(?<![a-zA-Z_.])\bdate\b', 'a.date', sql_query)
        
#         # Fix GROUP BY and ORDER BY clauses
#         sql_query = re.sub(r'GROUP BY\s+item_id', 'GROUP BY a.item_id', sql_query, flags=re.IGNORECASE)
#         sql_query = re.sub(r'ORDER BY\s+item_id', 'ORDER BY a.item_id', sql_query, flags=re.IGNORECASE)
        
#         return sql_query
    
#     async def generate_sql(self, question: str) -> str:
#         """
#         Generate SQL query using improved prompt engineering with proper aliasing
#         """
#         prompt = f"""You are an expert SQLite data analyst.
# Given the following database schema:
# {self.schema_context}

# Here is an example of how to answer a question with proper table aliasing:
# Question: "What were the top 5 products by total sales with their ROAS?"
# SQL Query:
# SELECT
#   t.item_id,
#   SUM(t.total_sales) AS total_sales_amount,
#   COALESCE(SUM(a.ad_sales) / NULLIF(SUM(a.ad_spend), 0), 0) AS roas
# FROM total_sales_metrics t
# LEFT JOIN ad_sales_metrics a ON t.item_id = a.item_id
# GROUP BY t.item_id
# ORDER BY total_sales_amount DESC
# LIMIT 5;

# CRITICAL RULES:
# 1. ALWAYS use table aliases (short names like 'a', 't', 'p')
# 2. ALWAYS qualify ALL column names with table aliases
# 3. Use explicit JOIN ... ON syntax, not USING()
# 4. Handle NULL values with NULLIF for division operations
# 5. Use COALESCE for handling potential NULL results

# ---

# Now, please answer this new question following these rules exactly.
# Question: "{question}"
# Your response MUST contain ONLY the SQL query with proper table aliasing.
# SQL Query:
# """
        
#         try:
#             payload = {
#                 "model": self.model,
#                 "prompt": prompt,
#                 "stream": False,
#                 "options": {
#                     "temperature": 0.0  # Deterministic output
#                 }
#             }
            
#             response = requests.post(self.ollama_url, json=payload, timeout=30)
#             response.raise_for_status()
            
#             response_data = response.json()
#             raw_response = response_data.get("response", "")
            
#             sql_query = self._clean_sql_from_response(raw_response)
            
#             if not sql_query or len(sql_query.split()) < 3:
#                 logger.error(f"Failed to generate complete SQL. Raw response: {raw_response}")
#                 return self._fallback_sql(question)
            
#             # Validate and fix the generated SQL
#             validated_query, error = self._validate_and_fix_sql(sql_query)
#             if error:
#                 logger.error(f"SQL validation failed: {error}")
#                 return self._fallback_sql(question)
            
#             logger.info(f"Generated SQL: {validated_query}")
#             return validated_query
            
#         except Exception as e:
#             logger.error(f"Error generating SQL: {e}")
#             return self._fallback_sql(question)
    
#     async def generate_response(self, question: str, sql_query: str, results: List[Dict]) -> str:
#         """Generate human-readable response"""
#         formatted_results = self._format_results(results)
        
#         prompt = f"""Based on the SQL query results, provide a clear business answer.

# Question: {question}
# SQL Query: {sql_query}
# Results: {formatted_results}

# Provide a concise, business-friendly answer with specific numbers and insights.
# Focus on the business meaning of the data, not technical details.
# """
        
#         try:
#             payload = {
#                 "model": self.model,
#                 "prompt": prompt,
#                 "stream": False,
#                 "options": {
#                     "temperature": 0.3
#                 }
#             }
            
#             response = requests.post(self.ollama_url, json=payload, timeout=30)
#             response.raise_for_status()
            
#             response_data = response.json()
#             return response_data.get("response", "").strip()
            
#         except Exception as e:
#             logger.error(f"Error generating response: {e}")
#             return self._fallback_response(question, results)
    
#     def _format_results(self, results: List[Dict]) -> str:
#         """Format query results for LLM consumption"""
#         if not results:
#             return "No results found"
        
#         if len(results) > 5:
#             formatted = json.dumps(results[:5], indent=2, default=str)
#             formatted += f"\n... and {len(results) - 5} more rows"
#         else:
#             formatted = json.dumps(results, indent=2, default=str)
        
#         return formatted
    
#     def _fallback_sql(self, question: str) -> str:
#         """Generate fallback SQL queries with proper table aliasing"""
#         question_lower = question.lower()
        
#         if 'total sales' in question_lower:
#             return "SELECT SUM(t.total_sales) as total_sales FROM total_sales_metrics t"
            
#         elif 'roas' in question_lower or 'return on ad spend' in question_lower:
#             return """
#                 SELECT 
#                     SUM(a.ad_sales) / NULLIF(SUM(a.ad_spend), 0) as roas,
#                     SUM(a.ad_sales) as total_ad_sales,
#                     SUM(a.ad_spend) as total_ad_spend
#                 FROM ad_sales_metrics a
#                 WHERE a.ad_spend > 0
#             """
            
#         elif 'cpc' in question_lower or 'cost per click' in question_lower:
#             return """
#                 SELECT 
#                     a.item_id,
#                     SUM(a.ad_spend) / NULLIF(SUM(a.clicks), 0) as cpc,
#                     SUM(a.ad_spend) as total_spend,
#                     SUM(a.clicks) as total_clicks
#                 FROM ad_sales_metrics a
#                 WHERE a.clicks > 0 
#                 GROUP BY a.item_id
#                 ORDER BY cpc DESC 
#                 LIMIT 10
#             """
            
#         elif 'top' in question_lower and 'product' in question_lower:
#             if 'roas' in question_lower:
#                 # Top products with ROAS
#                 return """
#                     SELECT 
#                         t.item_id,
#                         SUM(t.total_sales) as total_sales,
#                         SUM(t.total_units_ordered) as total_units,
#                         COALESCE(SUM(a.ad_sales) / NULLIF(SUM(a.ad_spend), 0), 0) as roas
#                     FROM total_sales_metrics t
#                     LEFT JOIN ad_sales_metrics a ON t.item_id = a.item_id
#                     GROUP BY t.item_id 
#                     ORDER BY total_sales DESC 
#                     LIMIT 10
#                 """
#             else:
#                 # Top products by sales
#                 return """
#                     SELECT 
#                         t.item_id,
#                         SUM(t.total_sales) as total_sales,
#                         SUM(t.total_units_ordered) as total_units
#                     FROM total_sales_metrics t
#                     GROUP BY t.item_id 
#                     ORDER BY total_sales DESC 
#                     LIMIT 10
#                 """
#         else:
#             return "SELECT COUNT(*) as total_records FROM total_sales_metrics"
    
#     def _fallback_response(self, question: str, results: List[Dict]) -> str:
#         """Generate fallback response when LLM fails"""
#         if not results:
#             return f"No data found for your question: '{question}'"
        
#         question_lower = question.lower()
        
#         if 'total sales' in question_lower and results:
#             total = results[0].get('total_sales', 0)
#             return f"Your total sales amount to ${total:,.2f}"
        
#         elif 'roas' in question_lower and results:
#             data = results[0]
#             roas = data.get('roas', 0)
#             ad_sales = data.get('total_ad_sales', 0)
#             ad_spend = data.get('total_ad_spend', 0)
#             return f"Your Return on Ad Spend (ROAS) is {roas:.2f}x. You've generated ${ad_sales:,.2f} in ad sales from ${ad_spend:,.2f} in ad spend."
        
#         elif 'cpc' in question_lower and results:
#             if results:
#                 item = results[0]
#                 cpc = item.get('cpc', 0)
#                 item_id = item.get('item_id', 'Unknown')
#                 return f"Product {item_id} has the highest CPC at ${cpc:.2f} per click."
        
#         elif 'top' in question_lower and 'product' in question_lower:
#             if results:
#                 top_items = []
#                 for i, item in enumerate(results[:5], 1):
#                     item_id = item.get('item_id', 'Unknown')
#                     total_sales = item.get('total_sales', 0)
#                     top_items.append(f"{i}. Product {item_id}: ${total_sales:,.2f}")
                
#                 return f"Top products by sales:\n" + "\n".join(top_items)
        
#         return f"Found {len(results)} results for your query: '{question}'"

import asyncio
import subprocess
import json
import logging
import re
import requests
from typing import List, Dict, Any
from config import OLLAMA_MODEL

logger = logging.getLogger(__name__)

class MistralService:
    def __init__(self):
        self.model = OLLAMA_MODEL or "mistral:7b-instruct"
        self.ollama_url = "http://localhost:11434/api/generate"
        self.schema_context = self._get_schema_context()
    
    def _get_schema_context(self) -> str:
        """Get simplified database schema context"""
        return """
        Table 'ad_sales_metrics' has columns: date, item_id, ad_sales, impressions, ad_spend, clicks, units_sold
        Table 'product_eligibility' has columns: eligibility_datetime_utc, item_id, eligibility, message
        Table 'total_sales_metrics' has columns: date, item_id, total_sales, total_units_ordered
        """
    
    def _clean_sql_from_response(self, raw_response: str) -> str:
        """
        Cleans the raw LLM output by finding all SQL queries and returning only the last one.
        """
        # Find all snippets that look like SQL queries ending with a semicolon
        queries = re.findall(r'SELECT.*?;', raw_response, re.IGNORECASE | re.DOTALL)
        
        if not queries:
            # Fallback for queries that don't end with a semicolon
            queries = re.findall(r'SELECT.*', raw_response, re.IGNORECASE | re.DOTALL)
            if not queries:
                return ""

        last_query = queries[-1].strip()
        return last_query
    
    def _should_use_fallback(self, question: str) -> bool:
        """Determine if we should skip AI and use fallback directly for reliable queries"""
        question_lower = question.lower()
        
        # Use fallback for these critical business queries
        fallback_triggers = [
            'total sales',
            'roas',
            'return on ad spend', 
            'cpc',
            'cost per click',
            'top products',
            'highest cpc',
            'conversion rate'
        ]
        
        return any(trigger in question_lower for trigger in fallback_triggers)
    
    async def generate_sql(self, question: str) -> str:
        """
        Generate SQL query - use fallback for critical business queries
        """
        
        # For critical business queries, skip AI and use reliable fallback
        if self._should_use_fallback(question):
            logger.info(f"Using fallback SQL for reliable query: {question}")
            return self._fallback_sql(question)
        
        # For other queries, try AI first
        prompt = f"""You are an expert SQLite data analyst.
Given the following database schema:
{self.schema_context}

Here is an example of how to answer a question:
Question: "What were the top 5 products by total sales?"
SQL Query:
SELECT
  item_id,
  SUM(total_sales) AS total_sales_amount
FROM total_sales_metrics
GROUP BY
  item_id
ORDER BY
  total_sales_amount DESC
LIMIT 5;

---

Now, please answer this new question.
Question: "{question}"
Your response MUST contain ONLY the SQL query.
SQL Query:
"""
        
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.0
                }
            }
            
            response = requests.post(self.ollama_url, json=payload, timeout=30)
            response.raise_for_status()
            
            response_data = response.json()
            raw_response = response_data.get("response", "")
            
            sql_query = self._clean_sql_from_response(raw_response)
            
            if not sql_query or len(sql_query.split()) < 3:
                logger.error(f"Failed to generate complete SQL. Raw response: {raw_response}")
                return self._fallback_sql(question)
            
            logger.info(f"Generated SQL: {sql_query}")
            return sql_query
            
        except Exception as e:
            logger.error(f"Error generating SQL: {e}")
            return self._fallback_sql(question)
    
    async def generate_response(self, question: str, sql_query: str, results: List[Dict]) -> str:
        """Generate human-readable response"""
        formatted_results = self._format_results(results)
        
        prompt = f"""Based on the SQL query results, provide a clear business answer.

Question: {question}
SQL Query: {sql_query}
Results: {formatted_results}

Provide a concise, business-friendly answer with specific numbers and insights.
"""
        
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3
                }
            }
            
            response = requests.post(self.ollama_url, json=payload, timeout=30)
            response.raise_for_status()
            
            response_data = response.json()
            return response_data.get("response", "").strip()
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return self._fallback_response(question, results)
    
    def _format_results(self, results: List[Dict]) -> str:
        """Format query results for LLM consumption"""
        if not results:
            return "No results found"
        
        if len(results) > 5:
            formatted = json.dumps(results[:5], indent=2, default=str)
            formatted += f"\n... and {len(results) - 5} more rows"
        else:
            formatted = json.dumps(results, indent=2, default=str)
        
        return formatted
    
    def _fallback_sql(self, question: str) -> str:
        """Generate reliable fallback SQL queries for business metrics"""
        question_lower = question.lower()
        
        if 'total sales' in question_lower:
            return "SELECT SUM(total_sales) as total_sales FROM total_sales_metrics"
            
        elif 'roas' in question_lower or 'return on ad spend' in question_lower:
            # Simple, reliable ROAS calculation
            return """
                SELECT 
                    SUM(ad_sales) / NULLIF(SUM(ad_spend), 0) as roas,
                    SUM(ad_sales) as total_ad_sales,
                    SUM(ad_spend) as total_ad_spend,
                    COUNT(DISTINCT item_id) as products_with_ads
                FROM ad_sales_metrics 
                WHERE ad_spend > 0
            """
            
        elif ('cpc' in question_lower or 'cost per click' in question_lower) and 'highest' in question_lower:
            # Find product with highest CPC
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
                LIMIT 1
            """
            
        elif 'cpc' in question_lower or 'cost per click' in question_lower:
            # General CPC analysis
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
            
        elif 'top' in question_lower and ('product' in question_lower or 'item' in question_lower):
            # Top products by sales
            return """
                SELECT 
                    item_id,
                    SUM(total_sales) as total_sales,
                    SUM(total_units_ordered) as total_units
                FROM total_sales_metrics 
                GROUP BY item_id 
                ORDER BY total_sales DESC 
                LIMIT 10
            """
            
        elif 'conversion rate' in question_lower:
            # Conversion rate analysis
            return """
                SELECT 
                    item_id,
                    SUM(units_sold) / NULLIF(SUM(clicks), 0) as conversion_rate,
                    SUM(units_sold) as total_units_sold,
                    SUM(clicks) as total_clicks
                FROM ad_sales_metrics 
                WHERE clicks > 0 
                GROUP BY item_id
                ORDER BY conversion_rate DESC 
                LIMIT 10
            """
            
        else:
            return "SELECT COUNT(*) as total_records FROM total_sales_metrics"
    
    def _fallback_response(self, question: str, results: List[Dict]) -> str:
        """Generate fallback response when LLM fails"""
        if not results:
            return f"No data found for your question: '{question}'"
        
        question_lower = question.lower()
        
        if 'total sales' in question_lower and results:
            total = results[0].get('total_sales', 0)
            return f"Your total sales amount to ${total:,.2f} across all products and time periods."
        
        elif 'roas' in question_lower and results:
            data = results[0]
            roas = data.get('roas', 0)
            ad_sales = data.get('total_ad_sales', 0)
            ad_spend = data.get('total_ad_spend', 0)
            products = data.get('products_with_ads', 0)
            return f"Your Return on Ad Spend (ROAS) is {roas:.2f}x. You've generated ${ad_sales:,.2f} in ad sales from ${ad_spend:,.2f} in ad spend across {products} products."
        
        elif 'cpc' in question_lower and 'highest' in question_lower and results:
            item = results[0]
            cpc = item.get('cpc', 0)
            item_id = item.get('item_id', 'Unknown')
            total_spend = item.get('total_spend', 0)
            total_clicks = item.get('total_clicks', 0)
            return f"Product {item_id} has the highest Cost Per Click at ${cpc:.2f}. This product spent ${total_spend:,.2f} and received {total_clicks:,} clicks."
        
        elif 'top' in question_lower and ('product' in question_lower or 'item' in question_lower):
            if results:
                response = "Top products by sales:\n"
                for i, item in enumerate(results[:5], 1):
                    item_id = item.get('item_id', 'Unknown')
                    sales = item.get('total_sales', 0)
                    units = item.get('total_units', 0)
                    response += f"{i}. Product {item_id}: ${sales:,.2f} ({units:,} units)\n"
                return response.strip()
        
        return f"Found {len(results)} results for your query: '{question}'"
