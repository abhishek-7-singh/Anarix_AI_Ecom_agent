from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime

# For Python 3.9+, we can use built-in dict instead of typing.Dict

class QueryRequest(BaseModel):
    question: str
    stream: Optional[bool] = False
    include_chart: Optional[bool] = True

class QueryResponse(BaseModel):
    response: str
    sql_query: Optional[str] = None
    results: Optional[List[dict[str, Any]]] = None  # Fixed: use dict instead of Dict
    chart_data: Optional[dict[str, Any]] = None     # Fixed: use dict instead of Dict
    execution_time: Optional[float] = None

class ChartData(BaseModel):
    type: str  # 'bar', 'pie', 'line'
    title: str
    data: List[dict[str, Any]]                      # Fixed: use dict instead of Dict
    labels: List[str]
    values: List[float]

class MetricsSummary(BaseModel):
    total_sales: Optional[float] = 0.0
    total_ad_spend: Optional[float] = 0.0
    total_roas: Optional[float] = 0.0
    eligible_products: Optional[int] = 0
    total_products: Optional[int] = 0
    top_performing_product: Optional[str] = None

class ProductEligibility(BaseModel):
    eligibility_datetime_utc: str
    item_id: int
    eligibility: bool
    message: Optional[str] = None

class AdSalesMetrics(BaseModel):
    date: str
    item_id: int
    ad_sales: float
    impressions: int
    ad_spend: float
    clicks: int
    units_sold: int

class TotalSalesMetrics(BaseModel):
    date: str
    item_id: int
    total_sales: float
    total_units_ordered: int
