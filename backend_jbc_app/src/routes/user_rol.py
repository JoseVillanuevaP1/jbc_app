from fastapi import APIRouter
from fastapi.responses import JSONResponse
from src.config.db import conn
from src.models.user_rol import user_roles
from src.schemas.user_rol import UserRole

user_rol = APIRouter(prefix="/user-rol", tags=["user_rol"])

@user_rol.post("/")
def assign(data: UserRole):
    conn.execute(user_roles.insert().values({
        "id_user": data.id_user,
        "id_rol": data.id_rol
    }))
    conn.commit()
    return JSONResponse(content={"success": True, "message": "Rol asignado al usuario"})

@user_rol.get("/{id_user}")
def get_roles(id_user: int):
    result = conn.execute(user_roles.select().where(user_roles.c.id_user == id_user)).fetchall()
    return JSONResponse(content={"success": True, "data": [dict(r._mapping) for r in result]})
