from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    id: Optional[str] = None
    name: str
    email: str
    password: str
    repeatPassword: str = None
    photo: Optional[str] = None
    description: Optional[str] = None
    status: Optional[bool] = True
    created_date: Optional[datetime] = None
    updated_date: Optional[datetime] = None