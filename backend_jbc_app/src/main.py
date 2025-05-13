from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from pathlib import Path
from src.routes.user import user
from src.routes.rol import rol
from src.routes.user_rol import user_rol
from src.routes.client import client
from src.routes.document_type import document_type

import mimetypes
mimetypes.init()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user, prefix="/api")
app.include_router(rol, prefix="/api")
app.include_router(user_rol, prefix="/api")
app.include_router(document_type, prefix="/api")
app.include_router(client, prefix="/api")

app.mount("/uploads", StaticFiles(directory="./uploads"), name="uploads")
try:
    build_dir = Path(__file__).resolve().parent.parent.parent / "fronted_jbc_app" / "dist"
    index_path = build_dir / "index.html"

    # Serve assets files from the build directory
    app.mount("/static", StaticFiles(directory=build_dir, html=False), name="static")

    # Catch-all route for SPA
    @app.get("/{catchall:path}", response_class=HTMLResponse)
    async def serve_spa(catchall: str):
        mimetypes.add_type('application/javascript', '.js')
        mimetypes.add_type('text/css', '.css')
        mimetypes.add_type('image/svg+xml', '.svg')
        path = build_dir / catchall
        if path.is_file():
            return FileResponse(path)
        return FileResponse(index_path)


except RuntimeError:
    print("No build directory found. Running in development mode.")