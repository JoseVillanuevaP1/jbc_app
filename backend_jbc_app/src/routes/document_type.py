from fastapi import APIRouter
from fastapi.responses import JSONResponse
from src.config.db import conn
from src.models.document_type import document_types
from src.schemas.document_type import DocumentType
from datetime import datetime

document_type = APIRouter(prefix="/document-type", tags=["Document Type"])

def serialize(row):
    obj = dict(row._mapping)
    obj["created_at"] = obj["created_at"].isoformat()
    if obj.get("updated_at"):
        obj["updated_at"] = obj["updated_at"].isoformat()
    return obj

@document_type.get("/")
def index():
    rows = conn.execute(document_types.select().where(document_types.c.status == True)).fetchall()
    return JSONResponse(content={"success": True, "data": [serialize(r) for r in rows]})

@document_type.post("/")
def store(doc: DocumentType):
    values = {
        "name": doc.name,
        "status": doc.status,
        "created_at": datetime.now()
    }
    result = conn.execute(document_types.insert().values(values))
    conn.commit()
    row = conn.execute(document_types.select().where(document_types.c.id == result.lastrowid)).first()
    return JSONResponse(content={"success": True, "data": serialize(row)})

@document_type.get("/{id}")
def show(id: int):
    row = conn.execute(document_types.select().where(document_types.c.id == id)).first()
    if not row:
        return JSONResponse(content={"success": False, "message": "Not found"})
    return JSONResponse(content={"success": True, "data": serialize(row)})

@document_type.put("/{id}")
def update(id: int, doc: DocumentType):
    values = {
        "name": doc.name,
        "status": doc.status,
        "updated_at": datetime.now()
    }
    conn.execute(document_types.update().values(values).where(document_types.c.id == id))
    conn.commit()
    row = conn.execute(document_types.select().where(document_types.c.id == id)).first()
    return JSONResponse(content={"success": True, "data": serialize(row)})

@document_type.delete("/{id}")
def destroy(id: int):
    conn.execute(document_types.delete().where(document_types.c.id == id))
    conn.commit()
    return JSONResponse(content={"success": True, "message": "Deleted"})