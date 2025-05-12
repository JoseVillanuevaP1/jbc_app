from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Rol(BaseModel):
    id: Optional[int] = None
    nombre: str
    status: Optional[bool] = True
    created_date: Optional[datetime] = None
    updated_date: Optional[datetime] = None