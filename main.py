from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import dog, owner, auth, visit, course, applicant
from app.core.init_data import create_admin_user
from app.db.init_db import init_db

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dog.router, prefix="/dog", tags=["dog"])
app.include_router(owner.router, prefix="/owner", tags=["owner"])
app.include_router(visit.router, prefix="/visits", tags=["visits"])
app.include_router(course.router, prefix="/course", tags=["course"])
app.include_router(applicant.router, prefix="/applicant", tags=["applicant"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])


@app.on_event("startup")
def on_startup():
    init_db()
    create_admin_user()
