from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
import os

file = APIRouter(
    prefix="/file",
    tags=["file"],
)

UPLOAD_PATH = "./uploads/"

@file.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        os.makedirs(UPLOAD_PATH, exist_ok=True)
        file_path = os.path.join(UPLOAD_PATH, file.filename)
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        return JSONResponse(content={"success": True, "message": "Archivo subido correctamente", "file_path": file_path})
    except Exception as e:
        return JSONResponse(content={"success": False, "message": f"Error al subir archivo: {str(e)}"})
