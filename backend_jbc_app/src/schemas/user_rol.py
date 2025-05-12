from pydantic import BaseModel

class UserRole(BaseModel):
    id_user: int
    id_rol: int
