from datetime import datetime
from typing import Union

from pydantic import BaseModel, Field


class ProductModel(BaseModel):
    prd_date_load: str
    prd_date_update: str
    prd_location: str
    prd_name: str
    prd_price: int
