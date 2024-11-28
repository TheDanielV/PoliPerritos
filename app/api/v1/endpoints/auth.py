import pytz
from fastapi import APIRouter, BackgroundTasks, Form
from pydantic import EmailStr

from fastapi.security import OAuth2PasswordRequestForm

from app.crud.token import create_token, verify_token
from app.crud.user import get_user_id_by_email
from app.models.domain.token import AuthToken
from app.core.security import *
from app.models.schema.user import Token
from app.db.session import get_db
from app.services.crypt import verify_password
from app.services.email_service import send_email
from app.services.password import reset_password
from app.services.verify import verify_password_, verify_email

router = APIRouter()


@router.post("/", response_model=dict)
def create_new_auth_user(user: UserCreate, db: Session = Depends(get_db)):
    if not verify_email(user.email):
        raise HTTPException(status_code=400, detail="Correo inválido")
    if not verify_password_(user.password):
        raise HTTPException(status_code=400, detail="La contraseña debe contener almenos una letra y un numero")
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


@router.post('/reset_password/verify', response_model=dict)
async def verify_password_code(
        code: int,
        db: Session = Depends(get_db)
):
    is_verified, id_user = verify_token(db, code)
    print(is_verified)
    if is_verified and is_verified is not None:
        return {'is_valid': True, 'message': 'Código valido'}
    if not is_verified and is_verified is not None:
        raise HTTPException(status_code=410, detail="Código expirado")
    raise HTTPException(status_code=400, detail="Código invalido")


@router.post('/reset_password/reset', response_model=dict)
async def reset_passwor(
        code: int,
        new_password: str,
        db: Session = Depends(get_db)
):
    if not verify_password_(new_password):
        raise HTTPException(status_code=400, detail="La contraseña debe contener almenos una letra y un numero")
    return reset_password(db, code, new_password)
