# import logging
# from typing import Dict, List, Any, Optional
# import json

# from config import CHART_COLORS, MAX_CHART_ITEMS

# logger = logging.getLogger(__name__)

# class ChartService:
#     def __init__(self):
#         self.colors = CHART_COLORS
    
#     def generate_chart_data(self, question: str, results: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
#         """Generate chart data based on query results and question context"""
#         if not results:
#             return None
        
#         try:
#             # Determine chart type based on question and data
#             chart_type = self._determine_chart_type(question, results)
            
#             if chart_type == "bar":
#                 return self._create_bar_chart(question, results)
#             elif chart_type == "pie":
#                 return self._create_pie_chart(question, results)
#             elif chart_type == "line":
#                 return self._create_line_chart(question, results)
#             else:
#                 return self._create_bar_chart(question, results)  # Default fallback
                
#         except Exception as e:
#             logger.error(f"Error generating chart data: {e}")
#             return None
    
#     def _determine_chart_type(self, question: str, results: List[Dict[str, Any]]) -> str:
#         """Determine the best chart type based on question and data structure"""
#         question_lower = question.lower()
        
#         # Check if we have time-series data
#         if any('date' in result for result in results) and len(results) > 1:
#             return "line"
        
#         # Check for distribution/comparison queries
#         if any(word in question_lower for word in ['top', 'highest', 'lowest', 'compare', 'distribution']):
#             if len(results) <= 6:
#                 return "pie"
#             else:
#                 return "bar"
        
#         # Check for percentage/proportion queries
#         if any(word in question_lower for word in ['percentage', 'proportion', 'share', 'breakdown']):
#             return "pie"
        
#         # Default to bar chart
#         return "bar"
    
#     def _create_bar_chart(self, question: str, results: List[Dict[str, Any]]) -> Dict[str, Any]:
#         """Create bar chart data"""
#         if not results:
#             return None
        
#         # Limit results for better visualization
#         limited_results = results[:MAX_CHART_ITEMS]
        
#         # Try to identify x and y axes
#         keys = list(limited_results[0].keys())
        
#         # Find the best label and value columns
#         label_col = self._find_label_column(keys)
#         value_col = self._find_value_column(keys)
        
#         if not label_col or not value_col:
#             return None
        
#         labels = []
#         values = []
        
#         for result in limited_results:
#             label = str(result.get(label_col, 'Unknown'))
#             value = float(result.get(value_col, 0))
            
#             labels.append(label)
#             values.append(value)
        
#         return {
#             "type": "bar",
#             "title": self._generate_chart_title(question),
#             "data": [
#                 {
#                     "label": labels[i],
#                     "value": values[i],
#                     "color": self.colors[i % len(self.colors)]
#                 }
#                 for i in range(len(labels))
#             ],
#             "labels": labels,
#             "values": values,
#             "config": {
#                 "xAxis": label_col,
#                 "yAxis": value_col,
#                 "colors": self.colors[:len(labels)]
#             }
#         }
    
#     def _create_pie_chart(self, question: str, results: List[Dict[str, Any]]) -> Dict[str, Any]:
#         """Create pie chart data"""
#         if not results:
#             return None
        
#         # Limit results for better visualization
#         limited_results = results[:MAX_CHART_ITEMS]
        
#         keys = list(limited_results[0].keys())
#         label_col = self._find_label_column(keys)
#         value_col = self._find_value_column(keys)
        
#         if not label_col or not value_col:
#             return None
        
#         labels = []
#         values = []
        
#         for result in limited_results:
#             label = str(result.get(label_col, 'Unknown'))
#             value = float(result.get(value_col, 0))
            
#             labels.append(label)
#             values.append(value)
        
#         # Calculate percentages
#         total = sum(values)
#         percentages = [round((value / total * 100), 2) if total > 0 else 0 for value in values]
        
#         return {
#             "type": "pie",
#             "title": self._generate_chart_title(question),
#             "data": [
#                 {
#                     "label": labels[i],
#                     "value": values[i],
#                     "percentage": percentages[i],
#                     "color": self.colors[i % len(self.colors)]
#                 }
#                 for i in range(len(labels))
#             ],
#             "labels": labels,
#             "values": values,
#             "config": {
#                 "colors": self.colors[:len(labels)]
#             }
#         }
    
#     def _create_line_chart(self, question: str, results: List[Dict[str, Any]]) -> Dict[str, Any]:
#         """Create line chart data for time series"""
#         if not results:
#             return None
        
#         keys = list(results[0].keys())
#         date_col = self._find_date_column(keys)
#         value_col = self._find_value_column(keys)
        
#         if not date_col or not value_col:
#             return self._create_bar_chart(question, results)  # Fallback
        
#         labels = []
#         values = []
        
#         for result in results:
#             date = str(result.get(date_col, 'Unknown'))
#             value = float(result.get(value_col, 0))
            
#             labels.append(date)
#             values.append(value)
        
#         return {
#             "type": "line",
#             "title": self._generate_chart_title(question),
#             "data": [
#                 {
#                     "x": labels[i],
#                     "y": values[i]
#                 }
#                 for i in range(len(labels))
#             ],
#             "labels": labels,
#             "values": values,
#             "config": {
#                 "xAxis": date_col,
#                 "yAxis": value_col,
#                 "color": self.colors[0]
#             }
#         }
    
#     def _find_label_column(self, keys: List[str]) -> Optional[str]:
#         """Find the best column to use as labels"""
#         # Prioritize certain column types
#         priority_cols = ['item_id', 'product_id', 'name', 'title', 'category']
        
#         for col in priority_cols:
#             if col in keys:
#                 return col
        
#         # Look for string-like columns
#         for key in keys:
#             if any(term in key.lower() for term in ['id', 'name', 'title', 'category', 'item']):
#                 return key
        
#         # Return first non-numeric column
#         return keys[0] if keys else None
    
#     def _find_value_column(self, keys: List[str]) -> Optional[str]:
#         """Find the best column to use as values"""
#         # Prioritize numeric columns
#         priority_cols = ['total_sales', 'ad_sales', 'ad_spend', 'sales', 'revenue', 'amount', 'value', 'count']
        
#         for col in priority_cols:
#             if col in keys:
#                 return col
        
#         # Look for numeric-sounding columns
#         for key in keys:
#             if any(term in key.lower() for term in ['sales', 'revenue', 'amount', 'total', 'count', 'spend']):
#                 return key
        
#         # Return last column as fallback
#         return keys[-1] if keys else None
    
#     def _find_date_column(self, keys: List[str]) -> Optional[str]:
#         """Find date column for time series charts"""
#         date_cols = ['date', 'datetime', 'time', 'timestamp']
        
#         for col in date_cols:
#             if col in keys:
#                 return col
        
#         for key in keys:
#             if any(term in key.lower() for term in ['date', 'time']):
#                 return key
        
#         return None
    
#     def _generate_chart_title(self, question: str) -> str:
#         """Generate an appropriate chart title"""
#         # Clean up the question for use as title
#         title = question.strip()
#         if title.endswith('?'):
#             title = title[:-1]
        
#         # Capitalize first letter
#         title = title[0].upper() + title[1:] if title else "Data Analysis"
        
#         return title


import logging
from typing import Dict, List, Any, Optional
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from config import CHART_COLORS, MAX_CHART_ITEMS, CHART_CONFIG

logger = logging.getLogger(__name__)

class ChartService:
    def __init__(self):
        self.colors = CHART_COLORS
        self.config = CHART_CONFIG
    
    def generate_chart_data(self, question: str, results: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Generate enhanced chart data using Streamlit's visualization logic"""
        if not results:
            return None
        
        try:
            # Convert results to DataFrame for easier manipulation
            df = pd.DataFrame(results)
            
            # Create both traditional chart data and Plotly chart
            chart_type = self._determine_chart_type(question, results)
            traditional_chart = self._create_traditional_chart(chart_type, question, results)
            plotly_chart = self._create_enhanced_visualization(df, question)
            
            # Combine both approaches
            chart_data = traditional_chart or {}
            if plotly_chart:
                chart_data["plotly_config"] = plotly_chart
                chart_data["enhanced_visualization"] = True
            
            return chart_data
            
        except Exception as e:
            logger.error(f"Error generating chart data: {e}")
            return None
    
    def _create_enhanced_visualization(self, df: pd.DataFrame, question: str):
        """
        Creates a Plotly chart using the improved logic from Streamlit version
        """
        if df is None or df.empty or len(df.columns) < 2:
            return None

        try:
            # Logic for 2-column charts (Bar or Line)
            if len(df.columns) == 2:
                x_col, y_col = df.columns[0], df.columns[1]
                
                # If the x-axis is a date, create a line chart
                try:
                    pd.to_datetime(df[x_col])
                    df[x_col] = pd.to_datetime(df[x_col])
                    fig = px.line(df, x=x_col, y=y_col, 
                                title=f"{y_col} over Time", 
                                markers=True,
                                color_discrete_sequence=self.colors)
                    fig.update_layout(
                        height=self.config.get("default_chart_height", 400),
                        template="plotly_dark"
                    )
                    return fig.to_json()
                except:
                    pass
                    
                # If the x-axis is text (categorical), create a bar chart
                if df.shape[0] < 30 and (pd.api.types.is_string_dtype(df[x_col]) or pd.api.types.is_integer_dtype(df[x_col])):
                    # Sort the data for a cleaner bar chart
                    df_sorted = df.sort_values(by=y_col, ascending=False)
                    fig = px.bar(df_sorted, x=x_col, y=y_col, 
                               title=f"Comparison of {y_col} by {x_col}",
                               color_discrete_sequence=self.colors)
                    fig.update_layout(
                        height=self.config.get("default_chart_height", 400),
                        template="plotly_dark"
                    )
                    return fig.to_json()

            # Logic for 3+ column charts (Scatter Plot)
            if len(df.columns) >= 3:
                # Check for numeric columns to use for axes
                numeric_cols = df.select_dtypes(include=['number']).columns
                if len(numeric_cols) >= 2:
                    x_col = numeric_cols[0]
                    y_col = numeric_cols[1]
                    # Use the first categorical column for color, if available
                    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
                    color_col = categorical_cols[0] if len(categorical_cols) > 0 else None
                    
                    title = f"{y_col} vs. {x_col}"
                    if color_col:
                        title += f" by {color_col}"

                    fig = px.scatter(df, x=x_col, y=y_col, color=color_col, 
                                   title=title,
                                   hover_data=df.columns,
                                   color_discrete_sequence=self.colors)
                    fig.update_layout(
                        height=self.config.get("default_chart_height", 400),
                        template="plotly_dark"
                    )
                    return fig.to_json()

            # Fallback: Simple bar chart
            if len(df.columns) >= 2:
                x_col, y_col = df.columns[0], df.columns[1]
                fig = px.bar(df, x=x_col, y=y_col, 
                           title=self._generate_chart_title(question),
                           color_discrete_sequence=self.colors)
                fig.update_layout(
                    height=self.config.get("default_chart_height", 400),
                    template="plotly_dark"
                )
                return fig.to_json()

            return None
            
        except Exception as e:
            logger.error(f"Error creating enhanced visualization: {e}")
            return None
    
    def _create_traditional_chart(self, chart_type: str, question: str, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create traditional chart data for 3D charts"""
        if chart_type == "bar":
            return self._create_bar_chart(question, results)
        elif chart_type == "pie":
            return self._create_pie_chart(question, results)
        elif chart_type == "line":
            return self._create_line_chart(question, results)
        else:
            return self._create_bar_chart(question, results)
    
    def _determine_chart_type(self, question: str, results: List[Dict[str, Any]]) -> str:
        """Determine the best chart type based on question and data structure"""
        question_lower = question.lower()
        
        # Convert to DataFrame for analysis
        df = pd.DataFrame(results)
        
        # Check if we have time-series data
        date_cols = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
        if date_cols and len(results) > 1:
            return "line"
        
        # Check for distribution/comparison queries
        if any(word in question_lower for word in ['top', 'highest', 'lowest', 'compare', 'distribution']):
            if len(results) <= 6:
                return "pie"
            else:
                return "bar"
        
        # Check for percentage/proportion queries
        if any(word in question_lower for word in ['percentage', 'proportion', 'share', 'breakdown']):
            return "pie"
        
        # Analyze data structure
        if len(df.columns) >= 3:
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) >= 2:
                return "scatter"
        
        # Default to bar chart
        return "bar"
    
    def _create_bar_chart(self, question: str, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create enhanced bar chart data"""
        if not results:
            return None
        
        # Limit results for better visualization
        limited_results = results[:MAX_CHART_ITEMS]
        
        # Try to identify x and y axes
        keys = list(limited_results[0].keys())
        
        # Find the best label and value columns
        label_col = self._find_label_column(keys)
        value_col = self._find_value_column(keys)
        
        if not label_col or not value_col:
            return None
        
        labels = []
        values = []
        chart_data = []
        
        for i, result in enumerate(limited_results):
            label = str(result.get(label_col, 'Unknown'))
            value = float(result.get(value_col, 0))
            
            # Enhanced data point with more information
            data_point = {
                "label": label,
                "value": value,
                "color": self.colors[i % len(self.colors)],
                "item_id": result.get('item_id', f'item_{i}'),
                "item_name": self._get_item_name(result, label),
                "additional_info": {k: v for k, v in result.items() if k not in [label_col, value_col]}
            }
            
            labels.append(label)
            values.append(value)
            chart_data.append(data_point)
        
        return {
            "type": "bar",
            "title": self._generate_chart_title(question),
            "data": chart_data,
            "labels": labels,
            "values": values,
            "config": {
                "xAxis": label_col,
                "yAxis": value_col,
                "colors": self.colors[:len(labels)],
                "enhanced": True
            }
        }
    
    def _create_pie_chart(self, question: str, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create enhanced pie chart data"""
        if not results:
            return None
        
        # Limit results for better visualization
        limited_results = results[:MAX_CHART_ITEMS]
        
        keys = list(limited_results[0].keys())
        label_col = self._find_label_column(keys)
        value_col = self._find_value_column(keys)
        
        if not label_col or not value_col:
            return None
        
        labels = []
        values = []
        chart_data = []
        
        # Calculate total for percentages
        total = sum(float(result.get(value_col, 0)) for result in limited_results)
        
        for i, result in enumerate(limited_results):
            label = str(result.get(label_col, 'Unknown'))
            value = float(result.get(value_col, 0))
            percentage = round((value / total * 100), 2) if total > 0 else 0
            
            data_point = {
                "label": label,
                "value": value,
                "percentage": percentage,
                "color": self.colors[i % len(self.colors)],
                "item_id": result.get('item_id', f'item_{i}'),
                "item_name": self._get_item_name(result, label)
            }
            
            labels.append(label)
            values.append(value)
            chart_data.append(data_point)
        
        return {
            "type": "pie",
            "title": self._generate_chart_title(question),
            "data": chart_data,
            "labels": labels,
            "values": values,
            "config": {
                "colors": self.colors[:len(labels)],
                "total": total,
                "enhanced": True
            }
        }
    
    def _create_line_chart(self, question: str, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create enhanced line chart data for time series"""
        if not results:
            return None
        
        keys = list(results[0].keys())
        date_col = self._find_date_column(keys)
        value_col = self._find_value_column(keys)
        
        if not date_col or not value_col:
            return self._create_bar_chart(question, results)  # Fallback
        
        # Sort by date
        try:
            sorted_results = sorted(results, key=lambda x: pd.to_datetime(x.get(date_col, '1900-01-01')))
        except:
            sorted_results = results
        
        labels = []
        values = []
        chart_data = []
        
        for result in sorted_results:
            date = str(result.get(date_col, 'Unknown'))
            value = float(result.get(value_col, 0))
            
            data_point = {
                "x": date,
                "y": value,
                "label": date,
                "value": value
            }
            
            labels.append(date)
            values.append(value)
            chart_data.append(data_point)
        
        return {
            "type": "line",
            "title": self._generate_chart_title(question),
            "data": chart_data,
            "labels": labels,
            "values": values,
            "config": {
                "xAxis": date_col,
                "yAxis": value_col,
                "color": self.colors[0],
                "enhanced": True
            }
        }
    
    def _get_item_name(self, result: Dict, fallback_label: str) -> str:
        """Extract meaningful item name from result"""
        # Try various column names that might contain item names
        name_columns = ['product_name', 'item_name', 'name', 'title', 'description']
        
        for col in name_columns:
            if col in result and result[col]:
                return str(result[col])
        
        # If item_id exists, format it nicely
        if 'item_id' in result:
            return f"Product {result['item_id']}"
        
        return fallback_label
    
    def _find_label_column(self, keys: List[str]) -> Optional[str]:
        """Find the best column to use as labels"""
        # Prioritize certain column types
        priority_cols = ['item_id', 'product_id', 'name', 'title', 'category']
        
        for col in priority_cols:
            if col in keys:
                return col
        
        # Look for string-like columns
        for key in keys:
            if any(term in key.lower() for term in ['id', 'name', 'title', 'category', 'item']):
                return key
        
        # Return first non-numeric column
        return keys[0] if keys else None
    
    def _find_value_column(self, keys: List[str]) -> Optional[str]:
        """Find the best column to use as values"""
        # Prioritize numeric columns
        priority_cols = ['total_sales', 'ad_sales', 'ad_spend', 'sales', 'revenue', 'amount', 'value', 'count', 'roas', 'cpc']
        
        for col in priority_cols:
            if col in keys:
                return col
        
        # Look for numeric-sounding columns
        for key in keys:
            if any(term in key.lower() for term in ['sales', 'revenue', 'amount', 'total', 'count', 'spend', 'cost', 'price']):
                return key
        
        # Return last column as fallback
        return keys[-1] if keys else None
    
    def _find_date_column(self, keys: List[str]) -> Optional[str]:
        """Find date column for time series charts"""
        date_cols = ['date', 'datetime', 'time', 'timestamp', 'eligibility_datetime_utc']
        
        for col in date_cols:
            if col in keys:
                return col
        
        for key in keys:
            if any(term in key.lower() for term in ['date', 'time']):
                return key
        
        return None
    
    def _generate_chart_title(self, question: str) -> str:
        """Generate an appropriate chart title"""
        # Clean up the question for use as title
        title = question.strip()
        if title.endswith('?'):
            title = title[:-1]
        
        # Capitalize first letter
        title = title[0].upper() + title[1:] if title else "Data Analysis"
        
        # Add contextual improvements
        if 'top' in title.lower():
            title = title.replace('top', 'Top')
        if 'sales' in title.lower():
            title += " - Sales Analysis"
        elif 'roas' in title.lower():
            title += " - ROAS Performance"
        elif 'cpc' in title.lower():
            title += " - Cost Analysis"
        
        return title
