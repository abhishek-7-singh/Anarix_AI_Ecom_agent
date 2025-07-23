import re
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, validator
import logging

logger = logging.getLogger(__name__)

class QueryValidator:
    def __init__(self):
        self.max_query_length = 1000
        self.dangerous_patterns = [
            r'\b(DROP|DELETE|UPDATE|INSERT|ALTER|CREATE|TRUNCATE)\b',
            r'--',
            r'/\*.*?\*/',
            r';\s*DROP',
            r'UNION.*SELECT',
            r'OR.*1\s*=\s*1'
        ]

    def validate_query_input(self, question: str) -> Dict[str, Any]:
        """Validate user query input"""
        errors = []
        warnings = []
        
        # Check length
        if len(question) > self.max_query_length:
            errors.append(f"Question too long. Maximum {self.max_query_length} characters allowed.")
        
        # Check for empty input
        if not question.strip():
            errors.append("Question cannot be empty.")
        
        # Check for dangerous patterns
        for pattern in self.dangerous_patterns:
            if re.search(pattern, question, re.IGNORECASE):
                errors.append("Question contains potentially harmful content.")
                break
        
        # Check for valid characters
        if not re.match(r'^[a-zA-Z0-9\s\?\.\,\!\-\(\)\'\"]+$', question):
            warnings.append("Question contains special characters that might affect processing.")
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'cleaned_input': self._clean_input(question)
        }

    def validate_sql_query(self, sql_query: str) -> Dict[str, Any]:
        """Validate generated SQL query"""
        errors = []
        warnings = []
        
        # Check for dangerous operations
        dangerous_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'CREATE', 'TRUNCATE']
        query_upper = sql_query.upper()
        
        for keyword in dangerous_keywords:
            if keyword in query_upper:
                errors.append(f"SQL contains dangerous keyword: {keyword}")
        
        # Check for valid SELECT structure
        if not sql_query.strip().upper().startswith('SELECT'):
            if not sql_query.strip().upper().startswith('WITH'):
                errors.append("SQL query must start with SELECT or WITH")
        
        # Check for table existence
        valid_tables = ['product_eligibility', 'ad_sales_metrics', 'total_sales_metrics']
        for table in valid_tables:
            if table in sql_query.lower():
                break
        else:
            warnings.append("Query doesn't reference any known tables")
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }

    def _clean_input(self, question: str) -> str:
        """Clean and sanitize input"""
        # Remove extra whitespace
        cleaned = re.sub(r'\s+', ' ', question.strip())
        
        # Remove potentially harmful characters
        cleaned = re.sub(r'[<>"\']', '', cleaned)
        
        return cleaned

class DataValidator:
    @staticmethod
    def validate_eligibility_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate eligibility data format"""
        errors = []
        
        required_fields = ['eligibility_datetime_utc', 'item_id', 'eligibility']
        for field in required_fields:
            if field not in data:
                errors.append(f"Missing required field: {field}")
        
        # Validate data types
        if 'item_id' in data and not isinstance(data['item_id'], int):
            try:
                data['item_id'] = int(data['item_id'])
            except (ValueError, TypeError):
                errors.append("item_id must be an integer")
        
        if 'eligibility' in data and not isinstance(data['eligibility'], bool):
            if data['eligibility'] in ['True', 'true', '1', 1]:
                data['eligibility'] = True
            elif data['eligibility'] in ['False', 'false', '0', 0]:
                data['eligibility'] = False
            else:
                errors.append("eligibility must be a boolean")
        
        return {'is_valid': len(errors) == 0, 'errors': errors, 'data': data}

    @staticmethod
    def validate_metrics_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate metrics data format"""
        errors = []
        
        # Validate numeric fields
        numeric_fields = ['ad_sales', 'impressions', 'ad_spend', 'clicks', 'units_sold']
        for field in numeric_fields:
            if field in data:
                try:
                    data[field] = float(data[field])
                    if data[field] < 0:
                        errors.append(f"{field} cannot be negative")
                except (ValueError, TypeError):
                    errors.append(f"{field} must be a number")
        
        # Validate logical relationships
        if 'clicks' in data and 'impressions' in data:
            if data['clicks'] > data['impressions']:
                errors.append("Clicks cannot exceed impressions")
        
        return {'is_valid': len(errors) == 0, 'errors': errors, 'data': data}
