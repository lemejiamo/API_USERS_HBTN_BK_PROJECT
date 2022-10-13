from datetime import datetime
from typing import Union

from pydantic import BaseModel, Field


class CompanyModel(BaseModel):
    cmp_cellphone: str
    cmp_date_load: str
    cmp_date_update: str
    cmp_location: str
    cmp_name: str
    cmp_rating: int
    cmp_telephone: int
