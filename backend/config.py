# import os
# from pathlib import Path

# # Base directories
# BASE_DIR = Path(__file__).parent.parent
# DATA_DIR = BASE_DIR / "data"
# MODELS_DIR = BASE_DIR / "models"

# # Database configuration
# DATABASE_URL = "sqlite:///./data/database/ecommerce_data.db"
# DATABASE_PATH = DATA_DIR / "database" / "ecommerce_data.db"

# # Data file paths - FIXED TO MATCH YOUR ACTUAL FILES
# ELIGIBILITY_FILE = DATA_DIR / "raw" / "Product-Level Eligibility Table (mapped).xlsx"
# AD_SALES_FILE = DATA_DIR / "raw" / "Product-Level Ad Sales and Metrics (mapped).xlsx"
# TOTAL_SALES_FILE = DATA_DIR / "raw" / "Product-Level Total Sales and Metrics (mapped).xlsx"

# # Mistral configuration
# MISTRAL_MODEL_PATH = MODELS_DIR / "mistral"
# OLLAMA_MODEL = "mistral:7b-instruct"

# # API configuration
# MAX_QUERY_LENGTH = 1000
# STREAMING_CHUNK_SIZE = 1
# QUERY_TIMEOUT = 30

# # Logging configuration
# LOG_LEVEL = "INFO"
# LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# # Environment variables
# DEBUG = os.getenv("DEBUG", "false").lower() == "true"
# ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# # Chart configuration
# CHART_COLORS = [
#     "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7",
#     "#DDA0DD", "#98D8C8", "#F7DC6F", "#BB8FCE", "#85C1E9"
# ]

# MAX_CHART_ITEMS = 20


import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"

# Database configuration
DATABASE_URL = "sqlite:///./data/database/ecommerce_data.db"
DATABASE_PATH = DATA_DIR / "database" / "ecommerce_data.db"

# Data file paths - FIXED TO MATCH YOUR ACTUAL FILES
ELIGIBILITY_FILE = DATA_DIR / "raw" / "Product-Level Eligibility Table (mapped).xlsx"
AD_SALES_FILE = DATA_DIR / "raw" / "Product-Level Ad Sales and Metrics (mapped).xlsx"
TOTAL_SALES_FILE = DATA_DIR / "raw" / "Product-Level Total Sales and Metrics (mapped).xlsx"

# Mistral/Ollama configuration - ENHANCED
MISTRAL_MODEL_PATH = MODELS_DIR / "mistral"
OLLAMA_MODEL = "mistral:7b-instruct"
OLLAMA_API_URL = "http://localhost:11434/api/generate"  # NEW: Direct API endpoint
OLLAMA_TEMPERATURE = 0.0  # NEW: For deterministic SQL generation
OLLAMA_TIMEOUT = 30  # NEW: Request timeout in seconds

# API configuration
MAX_QUERY_LENGTH = 1000
STREAMING_CHUNK_SIZE = 1
QUERY_TIMEOUT = 30

# Logging configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Environment variables
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Chart configuration
CHART_COLORS = [
    "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7",
    "#DDA0DD", "#98D8C8", "#F7DC6F", "#BB8FCE", "#85C1E9"
]

MAX_CHART_ITEMS = 20

# NEW: Enhanced SQL Generation Configuration
SQL_GENERATION_CONFIG = {
    "temperature": OLLAMA_TEMPERATURE,
    "max_tokens": 512,
    "stop_sequences": [";", "\n\n"],
    "retry_attempts": 3
}

# NEW: Database Schema Mapping (for cleaner AI context)
DATABASE_SCHEMA = {
    "product_eligibility": {
        "columns": ["eligibility_datetime_utc", "item_id", "eligibility", "message"],
        "description": "Product advertising eligibility status"
    },
    "ad_sales_metrics": {
        "columns": ["date", "item_id", "ad_sales", "impressions", "ad_spend", "clicks", "units_sold"],
        "description": "Advertising performance metrics"
    },
    "total_sales_metrics": {
        "columns": ["date", "item_id", "total_sales", "total_units_ordered"],
        "description": "Overall sales performance data"
    }
}

# NEW: Chart Generation Settings
CHART_CONFIG = {
    "default_chart_height": 400,
    "max_data_points": MAX_CHART_ITEMS,
    "color_palette": CHART_COLORS,
    "enable_plotly": True,
    "enable_3d_charts": True
}

# NEW: AI Response Configuration
AI_RESPONSE_CONFIG = {
    "max_response_length": 2000,
    "include_sql_in_response": True,
    "include_execution_time": True,
    "fallback_enabled": True,
    "response_temperature": 0.3  # Slightly creative for responses
}

# NEW: Performance Monitoring
PERFORMANCE_CONFIG = {
    "log_query_times": True,
    "slow_query_threshold": 5.0,  # seconds
    "enable_caching": True,
    "cache_ttl": 300  # 5 minutes
}
