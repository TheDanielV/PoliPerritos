from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import dog, owner, auth
from app.db.init_db import init_db

app = FastAPI()

# Aquí agregas el middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos
    allow_headers=["*"],  # Permitir todas las cabeceras
)

app.include_router(dog.router, prefix="/dog", tags=["dog"])
app.include_router(owner.router, prefix="/owner", tags=["owner"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])


@app.on_event("startup")
def on_startup():
    init_db()
