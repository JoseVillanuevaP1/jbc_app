from fastapi import APIRouter
from fastapi.responses import JSONResponse
from src.config.db import conn
from src.models.client import clients
from src.schemas.client import Client
from datetime import datetime
from sqlalchemy import func

client = APIRouter(prefix="/client", tags=["Client"])

def serialize(row):
    obj = dict(row._mapping)
    obj["created_at"] = obj["created_at"].isoformat()
    if obj.get("updated_at"):
        obj["updated_at"] = obj["updated_at"].isoformat()
    return obj

@client.get("/")
def index(name: str = None, document_number: str = None, document_type_id: int = None):
    query = clients.select().where(clients.c.status == True)

    # Filtrar por el nombre completo (first_name + last_name)
    if name:
        query = query.where(
            func.concat(clients.c.first_name, " ", clients.c.last_name).ilike(f"%{name}%")
        )

    if document_number:
        query = query.where(clients.c.document_number.ilike(f"%{document_number}%"))
    
    if document_type_id:
        query = query.where(clients.c.document_type_id == document_type_id)

    # Ejecutar la consulta
    rows = conn.execute(query).fetchall()
    return JSONResponse(content={"success": True, "data": [serialize(r) for r in rows]})

@client.post("/")
def store(c: Client):
    values = {
        "first_name": c.first_name,
        "last_name": c.last_name,
        "document_number": c.document_number,
        "document_type_id": c.document_type_id,
        "phone": c.phone,
        "email": c.email,
        "address": c.address,
        "status": c.status,
        "created_at": datetime.now()
    }
    result = conn.execute(clients.insert().values(values))
    conn.commit()
    row = conn.execute(clients.select().where(clients.c.id == result.lastrowid)).first()
    return JSONResponse(content={"success": True, "data": serialize(row)})

@client.get("/{id}")
def show(id: int):
    row = conn.execute(clients.select().where(clients.c.id == id)).first()
    if not row:
        return JSONResponse(content={"success": False, "message": "Not found"})
    return JSONResponse(content={"success": True, "data": serialize(row)})

@client.put("/{id}")
def update(id: int, c: Client):
    values = {
        "first_name": c.first_name,
        "last_name": c.last_name,
        "document_number": c.document_number,
        "document_type_id": c.document_type_id,
        "phone": c.phone,
        "email": c.email,
        "address": c.address,
        "status": c.status,
        "updated_at": datetime.now()
    }
    conn.execute(clients.update().values(values).where(clients.c.id == id))
    conn.commit()
    row = conn.execute(clients.select().where(clients.c.id == id)).first()
    return JSONResponse(content={"success": True, "data": serialize(row)})

@client.delete("/{id}")
def destroy(id: int):
    conn.execute(clients.delete().where(clients.c.id == id))
    conn.commit()
    return JSONResponse(content={"success": True, "message": "Deleted"})
