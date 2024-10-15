from fastapi import FastAPI
from app.api.v1.endpoints import dog,owner
from app.db.init_db import init_db

app = FastAPI()

app.include_router(dog.router, prefix="/dog", tags=["dog"])
app.include_router(owner.router, prefix="/owner", tags=["owner"])


@app.on_event("startup")
def on_startup():
    init_db()
