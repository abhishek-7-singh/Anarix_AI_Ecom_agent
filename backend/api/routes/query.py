# from fastapi import APIRouter, HTTPException, BackgroundTasks
# from fastapi.responses import StreamingResponse, JSONResponse
# import asyncio
# import json
# import time
# import logging
# from typing import AsyncGenerator

# from core.models import QueryRequest, QueryResponse
# from core.database import DatabaseManager
# from services.mistral_service import MistralService
# from services.chart_service import ChartService

# router = APIRouter()
# logger = logging.getLogger(__name__)

# # Initialize services
# db_manager = DatabaseManager()
# mistral_service = MistralService()
# chart_service = ChartService()

# @router.post("/query")
# async def process_query(request: QueryRequest):
#     """Process a natural language query and return results"""
#     start_time = time.time()
    
#     try:
#         logger.info(f"Processing query: {request.question}")
        
#         # Generate SQL query using Mistral
#         sql_query = await mistral_service.generate_sql(request.question)
        
#         # Execute the SQL query
#         results = await db_manager.execute_query(sql_query)
        
#         # Generate human-readable response
#         response_text = await mistral_service.generate_response(
#             request.question, sql_query, results
#         )
        
#         # Generate chart data if requested
#         chart_data = None
#         if request.include_chart:
#             chart_data = chart_service.generate_chart_data(request.question, results)
        
#         execution_time = time.time() - start_time
        
#         # FIXED: Always return JSON response to avoid header issues
#         return JSONResponse({
#             "response": response_text,
#             "sql_query": sql_query,
#             "results": results,
#             "chart_data": chart_data,
#             "execution_time": execution_time,
#             "stream": request.stream  # Include stream preference in response
#         })
        
#     except Exception as e:
#         logger.error(f"Error processing query: {e}")
#         raise HTTPException(status_code=500, detail=f"Query processing failed: {str(e)}")

# @router.post("/query/stream")
# async def stream_query(request: QueryRequest):
#     """Stream query response with typing effect"""
#     try:
#         # Generate SQL and get results first
#         sql_query = await mistral_service.generate_sql(request.question)
#         results = await db_manager.execute_query(sql_query)
#         response_text = await mistral_service.generate_response(
#             request.question, sql_query, results
#         )
        
#         # FIXED: Use simpler headers
#         return StreamingResponse(
#             stream_response(response_text),
#             media_type="text/plain"
#         )
        
#     except Exception as e:
#         logger.error(f"Error streaming query: {e}")
#         raise HTTPException(status_code=500, detail=f"Streaming failed: {str(e)}")

# async def stream_response(text: str) -> AsyncGenerator[str, None]:
#     """Stream text with typing effect"""
#     for char in text:
#         yield char
#         await asyncio.sleep(0.02)  # Adjust speed as needed

# @router.get("/query/examples")
# async def get_example_queries():
#     """Get example queries for the UI"""
#     examples = [
#         "What is my total sales?",
#         "Calculate the Return on Ad Spend (ROAS)",
#         "Which product had the highest CPC (Cost Per Click)?",
#         "Show me the top 10 products by revenue",
#         "What's the conversion rate by product?",
#         "How many products are eligible for advertising?",
#         "What's my total ad spend this month?",
#         "Which products have the best ROAS?",
#         "Show me products with zero sales",
#         "What's the average order value?",
#         "Which products get the most impressions?",
#         "Calculate the click-through rate for each product"
#     ]
    
#     return {"examples": examples}

# @router.post("/sql/execute")
# async def execute_raw_sql(sql_query: str):
#     """Execute a raw SQL query (for advanced users)"""
#     try:
#         # Basic SQL injection protection
#         dangerous_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'CREATE']
#         query_upper = sql_query.upper().strip()
        
#         for keyword in dangerous_keywords:
#             if keyword in query_upper:
#                 raise HTTPException(
#                     status_code=400, 
#                     detail=f"Dangerous SQL keyword '{keyword}' not allowed"
#                 )
        
#         results = await db_manager.execute_query(sql_query)
        
#         return {
#             "sql_query": sql_query,
#             "results": results,
#             "count": len(results)
#         }
        
#     except Exception as e:
#         logger.error(f"Error executing SQL: {e}")
#         raise HTTPException(status_code=500, detail=f"SQL execution failed: {str(e)}")
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse, JSONResponse
import asyncio
import json
import time
import logging
from typing import AsyncGenerator

from core.models import QueryRequest, QueryResponse
from core.database import DatabaseManager
from services.mistral_service import MistralService
from services.chart_service import ChartService
from config import AI_RESPONSE_CONFIG, PERFORMANCE_CONFIG

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize services
db_manager = DatabaseManager()
mistral_service = MistralService()
chart_service = ChartService()

@router.post("/query")
async def process_query(request: QueryRequest):
    """Process a natural language query with enhanced AI capabilities"""
    start_time = time.time()
    
    try:
        logger.info(f"Processing query: {request.question}")
        
        # Generate SQL query using enhanced Mistral service
        sql_query = await mistral_service.generate_sql(request.question)
        
        # Log the generated SQL for debugging
        logger.info(f"Generated SQL: {sql_query}")
        
        # Execute the SQL query
        results = await db_manager.execute_query(sql_query)
        
        # Log query results count
        logger.info(f"Query returned {len(results) if results else 0} results")
        
        # Generate human-readable response
        response_text = await mistral_service.generate_response(
            request.question, sql_query, results
        )
        
        # Generate enhanced chart data with Plotly support
        chart_data = None
        if request.include_chart:
            chart_data = chart_service.generate_chart_data(request.question, results)
            if chart_data:
                logger.info(f"Generated {chart_data.get('type', 'unknown')} chart with {len(chart_data.get('data', []))} data points")
        
        execution_time = time.time() - start_time
        
        # Log slow queries for performance monitoring
        if execution_time > PERFORMANCE_CONFIG.get("slow_query_threshold", 5.0):
            logger.warning(f"Slow query detected: {execution_time:.2f}s for '{request.question}'")
        
        # Enhanced response with more metadata
        response_data = {
            "response": response_text,
            "sql_query": sql_query,
            "results": results,
            "chart_data": chart_data,
            "execution_time": execution_time,
            "data_points": len(results) if results else 0,
            "stream": request.stream,
            "enhanced_features": {
                "plotly_charts": chart_data.get("plotly_config") is not None if chart_data else False,
                "chart_type": chart_data.get("type") if chart_data else None,
                "has_visualization": chart_data is not None
            },
            "query_metadata": {
                "question_length": len(request.question),
                "sql_length": len(sql_query),
                "result_count": len(results) if results else 0,
                "timestamp": time.time()
            }
        }
        
        return JSONResponse(response_data)
        
    except Exception as e:
        logger.error(f"Error processing query '{request.question}': {e}")
        
        # Enhanced error response with more context
        error_response = {
            "error": "Query processing failed",
            "detail": str(e),
            "question": request.question,
            "execution_time": time.time() - start_time,
            "timestamp": time.time(),
            "suggestions": _get_error_suggestions(str(e))
        }
        
        raise HTTPException(status_code=500, detail=error_response)

@router.post("/query/analyze")
async def analyze_query_complexity(request: QueryRequest):
    """Analyze query complexity and suggest optimizations"""
    try:
        # Generate SQL without executing
        sql_query = await mistral_service.generate_sql(request.question)
        
        # Analyze the query
        analysis = {
            "original_question": request.question,
            "generated_sql": sql_query,
            "complexity_score": _calculate_complexity_score(sql_query),
            "estimated_performance": _estimate_performance(sql_query),
            "suggestions": _get_optimization_suggestions(sql_query),
            "chart_recommendations": _recommend_chart_type(request.question)
        }
        
        return JSONResponse(analysis)
        
    except Exception as e:
        logger.error(f"Error analyzing query: {e}")
        raise HTTPException(status_code=500, detail=f"Query analysis failed: {str(e)}")

@router.post("/query/batch")
async def process_batch_queries(requests: list[QueryRequest]):
    """Process multiple queries in batch for dashboard loading"""
    start_time = time.time()
    results = []
    
    try:
        for i, request in enumerate(requests[:10]):  # Limit to 10 queries
            try:
                logger.info(f"Processing batch query {i+1}/{len(requests)}: {request.question}")
                
                sql_query = await mistral_service.generate_sql(request.question)
                query_results = await db_manager.execute_query(sql_query)
                response_text = await mistral_service.generate_response(
                    request.question, sql_query, query_results
                )
                
                chart_data = None
                if request.include_chart:
                    chart_data = chart_service.generate_chart_data(request.question, query_results)
                
                results.append({
                    "query_index": i,
                    "question": request.question,
                    "response": response_text,
                    "sql_query": sql_query,
                    "results": query_results,
                    "chart_data": chart_data,
                    "success": True
                })
                
            except Exception as e:
                logger.error(f"Error in batch query {i+1}: {e}")
                results.append({
                    "query_index": i,
                    "question": request.question,
                    "error": str(e),
                    "success": False
                })
        
        total_time = time.time() - start_time
        
        return JSONResponse({
            "batch_results": results,
            "total_execution_time": total_time,
            "successful_queries": sum(1 for r in results if r.get("success")),
            "failed_queries": sum(1 for r in results if not r.get("success")),
            "timestamp": time.time()
        })
        
    except Exception as e:
        logger.error(f"Error processing batch queries: {e}")
        raise HTTPException(status_code=500, detail=f"Batch processing failed: {str(e)}")

@router.post("/query/stream")
async def stream_query(request: QueryRequest):
    """Stream query response with typing effect"""
    try:
        # Generate SQL and get results first
        sql_query = await mistral_service.generate_sql(request.question)
        results = await db_manager.execute_query(sql_query)
        response_text = await mistral_service.generate_response(
            request.question, sql_query, results
        )
        
        return StreamingResponse(
            stream_response(response_text),
            media_type="text/plain",
            headers={
                "X-SQL-Query": sql_query[:200] + "..." if len(sql_query) > 200 else sql_query,
                "X-Result-Count": str(len(results) if results else 0)
            }
        )
        
    except Exception as e:
        logger.error(f"Error streaming query: {e}")
        raise HTTPException(status_code=500, detail=f"Streaming failed: {str(e)}")

async def stream_response(text: str) -> AsyncGenerator[str, None]:
    """Stream text with typing effect"""
    for char in text:
        yield char
        await asyncio.sleep(0.02)  # Adjust speed as needed

@router.get("/query/examples")
async def get_example_queries():
    """Get enhanced example queries categorized by type"""
    examples = {
        "basic_analytics": [
            "What is my total sales?",
            "How much did I spend on advertising?",
            "How many products are in my catalog?"
        ],
        "performance_metrics": [
            "Calculate the Return on Ad Spend (ROAS)",
            "Which product had the highest CPC (Cost Per Click)?",
            "What's the conversion rate by product?",
            "Calculate the click-through rate for each product"
        ],
        "top_performers": [
            "Show me the top 10 products by revenue",
            "Which products have the best ROAS?",
            "What are the top 5 products by ad sales?",
            "Which products get the most impressions?"
        ],
        "trend_analysis": [
            "Show me sales trends over time",
            "How has my ad spend changed monthly?",
            "What's the trend in my ROAS performance?"
        ],
        "product_insights": [
            "Show me products with zero sales",
            "Which products are not eligible for advertising?",
            "What's the average order value by product?",
            "Compare ad sales vs total sales by product"
        ]
    }
    
    return {
        "examples": examples,
        "total_examples": sum(len(category) for category in examples.values()),
        "categories": list(examples.keys())
    }

@router.post("/sql/execute")
async def execute_raw_sql(request: dict):
    """Execute a raw SQL query with enhanced security and logging"""
    sql_query = request.get("sql_query", "")
    
    try:
        # Enhanced SQL injection protection
        dangerous_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'CREATE', 'TRUNCATE', 'REPLACE']
        query_upper = sql_query.upper().strip()
        
        for keyword in dangerous_keywords:
            if keyword in query_upper:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Dangerous SQL keyword '{keyword}' not allowed for security reasons"
                )
        
        # Limit query complexity
        if len(sql_query) > 1000:
            raise HTTPException(
                status_code=400,
                detail="Query too long. Maximum 1000 characters allowed."
            )
        
        start_time = time.time()
        results = await db_manager.execute_query(sql_query)
        execution_time = time.time() - start_time
        
        # Log the execution for monitoring
        logger.info(f"Raw SQL executed in {execution_time:.2f}s: {sql_query[:100]}...")
        
        return {
            "sql_query": sql_query,
            "results": results,
            "count": len(results) if results else 0,
            "execution_time": execution_time,
            "timestamp": time.time()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error executing raw SQL: {e}")
        raise HTTPException(status_code=500, detail=f"SQL execution failed: {str(e)}")

# Helper functions for enhanced features

def _get_error_suggestions(error_message: str) -> list[str]:
    """Provide helpful suggestions based on error type"""
    suggestions = []
    
    if "no such table" in error_message.lower():
        suggestions.append("Check if the table name is correct")
        suggestions.append("Verify that the database has been properly initialized")
    elif "no such column" in error_message.lower():
        suggestions.append("Check the column name spelling")
        suggestions.append("Use DESCRIBE or PRAGMA table_info to see available columns")
    elif "syntax error" in error_message.lower():
        suggestions.append("Check SQL syntax for typos")
        suggestions.append("Ensure proper use of quotes and parentheses")
    else:
        suggestions.append("Try rephrasing your question")
        suggestions.append("Check the example queries for reference")
    
    return suggestions

def _calculate_complexity_score(sql_query: str) -> int:
    """Calculate a complexity score for the SQL query"""
    score = 0
    query_upper = sql_query.upper()
    
    # Basic complexity indicators
    score += query_upper.count('JOIN') * 2
    score += query_upper.count('SUBQUERY') * 3
    score += query_upper.count('GROUP BY') * 1
    score += query_upper.count('ORDER BY') * 1
    score += query_upper.count('HAVING') * 2
    score += len(sql_query) // 100  # Length factor
    
    return min(score, 10)  # Cap at 10

def _estimate_performance(sql_query: str) -> str:
    """Estimate query performance"""
    complexity = _calculate_complexity_score(sql_query)
    
    if complexity <= 2:
        return "Fast"
    elif complexity <= 5:
        return "Medium"
    else:
        return "Slow"

def _get_optimization_suggestions(sql_query: str) -> list[str]:
    """Suggest query optimizations"""
    suggestions = []
    query_upper = sql_query.upper()
    
    if 'SELECT *' in query_upper:
        suggestions.append("Consider selecting specific columns instead of SELECT *")
    
    if 'ORDER BY' in query_upper and 'LIMIT' not in query_upper:
        suggestions.append("Consider adding LIMIT clause for large result sets")
    
    if query_upper.count('JOIN') > 2:
        suggestions.append("Multiple JOINs detected - ensure proper indexing")
    
    return suggestions

def _recommend_chart_type(question: str) -> dict:
    """Recommend the best chart type for the question"""
    question_lower = question.lower()
    
    if any(word in question_lower for word in ['top', 'highest', 'lowest']):
        return {"type": "bar", "reason": "Best for comparing ranked items"}
    elif any(word in question_lower for word in ['percentage', 'proportion', 'breakdown']):
        return {"type": "pie", "reason": "Best for showing proportions"}
    elif any(word in question_lower for word in ['trend', 'over time', 'monthly', 'daily']):
        return {"type": "line", "reason": "Best for showing trends over time"}
    else:
        return {"type": "bar", "reason": "Default for general comparisons"}