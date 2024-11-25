import pytz
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Form
from pydantic import EmailStr
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from starlette.requests import Request

from app.crud.token import create_token
from app.crud.user import get_user_id_by_email
from app.models.domain.token import AuthToken
from app.models.schema.user import UserCreate

from app.core.security import *
from app.models.schema.user import Token
from app.db.session import get_db
from app.services.email_service import send_email

router = APIRouter()


@router.post("/", response_model=dict)
def create_new_auth_user(user: UserCreate, db: Session = Depends(get_db)):
    auth_user = create_auth_user(db, user)
    if auth_user is None:
        raise HTTPException(status_code=404, detail="Ocurrio un error")
    return auth_user


@router.post("/token", response_model=Token)
def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = get_user(db, username=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post('/reset_password/send')
async def send_reset_password_code(
        background_tasks: BackgroundTasks,
        email: EmailStr = Form(...),
        db: Session = Depends(get_db)
):
    """
    Endpoint para enviar un correo electrónico.
    """
    subject = 'Recuperación de contraseña'
    try:
        # Enviar el correo en segundo plano
        user_id = get_user_id_by_email(db, email)
        if user_id:
            reset_token = AuthToken()
            reset_token.generate_token(user_id)
            if create_token(db, reset_token):
                ecuador_tz = pytz.timezone("America/Guayaquil")
                context = {
                    "body": {
                        "title": "Poliperros App",
                        "code": reset_token.value,
                        "date": reset_token.date_expiration.replace(tzinfo=pytz.utc)
                        .astimezone(ecuador_tz)
                        .strftime("%Y-%m-%d %H:%M:%S")
                    }
                }
                background_tasks.add_task(send_email, email, subject, context)
        return {"message": "Si el correo existe, el código sera enviado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/reset_password/verify')
async def verify_password_code(
        background_tasks: BackgroundTasks,
        code: int,
        db: Session = Depends(get_db)
):
    pass
