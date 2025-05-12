from fastapi import APIRouter
from fastapi.responses import JSONResponse
from datetime import datetime
from src.config.db import conn
from src.models.rol import roles
from src.schemas.rol import Rol

rol = APIRouter(prefix="/rol", tags=["rol"])

def serialize(row):
    data = dict(row._mapping)
    data["created_date"] = data["created_date"].isoformat()
    if data.get("updated_date"):
        data["updated_date"] = data["updated_date"].isoformat()
    return data

@rol.get("/")
def index():
    result = conn.execute(roles.select().where(roles.c.status == True)).fetchall()
    return JSONResponse(content={"success": True, "data": [serialize(r) for r in result]})

@rol.post("/")
def store(priv: Rol):
    new_priv = {
        "nombre": priv.nombre,
        "status": True,
        "created_date": datetime.now()
    }
    result = conn.execute(roles.insert().values(new_priv))
    conn.commit()
    created = conn.execute(roles.select().where(roles.c.id == result.lastrowid)).first()
    return JSONResponse(content={"success": True, "message": "Rol creado", "data": serialize(created)})
