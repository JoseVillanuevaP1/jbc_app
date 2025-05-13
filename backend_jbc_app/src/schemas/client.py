from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class Client(BaseModel):
    id: Optional[str] = None
    first_name: str
    last_name: str
    document_number: str
    document_type_id: int
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    status: Optional[bool] = True
    created_date: Optional[datetime] = None
    updated_date: Optional[datetime] = None