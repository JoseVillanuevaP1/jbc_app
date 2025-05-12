from fastapi import APIRouter
from fastapi.responses import JSONResponse
from src.config.db import conn
from src.models.user import users
from src.schemas.user import User
from src.schemas.login import Login
from cryptography.fernet import Fernet
from datetime import datetime, time
import os
from dotenv import load_dotenv

load_dotenv()
ENCRYPTION_KEY='BdSOu3s5mGNw7TBPW-UQc1XHZosajErzzwpPx1Orv2I='
key = os.getenv('ENCRYPTION_KEY')
f = Fernet(key)

user = APIRouter(prefix="/user", tags=["user"])

def serialize_user(row):
    user_dict = dict(row._mapping)
    user_dict["created_at"] = user_dict["created_at"].isoformat()
    if user_dict.get("updated_at"):
        user_dict["updated_at"] = user_dict["updated_at"].isoformat()
    return user_dict

@user.get("/")
def index():
    result = conn.execute(users.select().where(users.c.status == True)).fetchall()
    if not result:
        return JSONResponse(content={"success": False, "message": "No se encontraron resultados"})
    data = [serialize_user(row) for row in result]
    return JSONResponse(content={"success": True, "message": "Lista de usuarios", "data": data})

@user.post("/")
def store(user: User):
    if user.password != user.repeatPassword:
        return JSONResponse(content={"success": False, "message": "Las contraseñas no coinciden"})
    
    encrypted_password = f.encrypt(user.password.encode("utf-8"))
    new_user = {
        "name": user.name,
        "email": user.email,
        "password": encrypted_password,
        "created_at": datetime.now()
    }
    
    result = conn.execute(users.insert().values(new_user))
    conn.commit()
    user_created = conn.execute(users.select().where(users.c.id == result.lastrowid)).first()
    
    if not user_created:
        return JSONResponse(content={"success": False, "message": "Ocurrió un error al crear el usuario"})
    
    return JSONResponse(content={"success": True, "message": "Usuario creado", "data": serialize_user(user_created)})

@user.put("/{id}", response_model=User)
def update(id: str, user: User):
    encrypted_password = f.encrypt(user.password.encode("utf-8"))
    updated_user = {
        "name": user.name,
        "email": user.email,
        "password": encrypted_password,
        "updated_at": datetime.now()
    }
    
    conn.execute(users.update().values(updated_user).where(users.c.id == id))
    conn.commit()
    user_updated = conn.execute(users.select().where(users.c.id == id)).first()
    
    if not user_updated:
        return JSONResponse(content={"success": False, "message": "Ocurrió un error al actualizar el usuario"})
    
    return JSONResponse(content={"success": True, "message": "Usuario actualizado", "data": serialize_user(user_updated)})

@user.get("/{id}", response_model=User)
def show(id: str):
    user_found = conn.execute(users.select().where(users.c.id == id)).first()
    if not user_found:
        return JSONResponse(content={"success": False, "message": "No se encontró al usuario"})
    return JSONResponse(content={"success": True, "message": "Usuario encontrado", "data": serialize_user(user_found)})

@user.delete("/{id}")
def destroy(id: str):
    conn.execute(users.delete().where(users.c.id == id))
    conn.commit()
    return JSONResponse(content={"success": True, "message": "Usuario eliminado"})

WORK_HOURS = (time(8, 0), time(19, 0))
BLOCK_DURATION = 600

@user.post("/login")
async def login(login: Login):
    now = datetime.now()
    row = conn.execute(users.select().where((users.c.name == login.email) | (users.c.email == login.email))).first()
    if not row:
        return JSONResponse(content={"success": False, "message": "Credenciales inválidas", "data": {"email": True}})
    
    user = dict(row._mapping)
    if user['failed_attempts'] >= 3 and (not user['lock_time'] or (now - user['lock_time']).total_seconds() < BLOCK_DURATION):
        return JSONResponse(content={"success": False, "message": "Usuario bloqueado. Intente más tarde."})

    if user.get('role') != 'gerente':
        if not (WORK_HOURS[0] <= now.time() <= WORK_HOURS[1]):
            return JSONResponse(content={"success": False, "message": "Fuera del horario laboral."})

    try:
        if f.decrypt(user['password']).decode() != login.password:
            attempts = user['failed_attempts'] + 1
            conn.execute(users.update().where(users.c.id == user['id']).values(
                failed_attempts=attempts,
                lock_time=now if attempts >= 3 else None
            ))
            return JSONResponse(content={"success": False, "message": "Contraseña incorrecta", "data": {"password": True}})
    except:
        return JSONResponse(content={"success": False, "message": "Error al validar la contraseña."})

    # Login exitoso
    conn.execute(users.update().where(users.c.id == user['id']).values(failed_attempts=0, lock_time=None))
    return JSONResponse(content={"success": True, "message": "Login exitoso", "data": user["id"]})