from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class DocumentType(BaseModel):
    name: str
    status: Optional[bool] = True
    created_date: Optional[datetime] = None
    updated_date: Optional[datetime] = None