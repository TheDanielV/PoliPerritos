from typing import List

import pytz
from fastapi import APIRouter, BackgroundTasks, Form
from pydantic import EmailStr

from fastapi.security import OAuth2PasswordRequestForm

from app.crud.token import create_token, verify_token
from app.crud.user import get_user_id_by_email, create_auth_user, update_auth_user_basic_information, \
    update_auth_user_password, delete_auth_user, auto_create_auth_user, read_all_users
from app.models.domain.token import AuthToken
from app.core.security import *
from app.models.domain.user import Role
from app.models.schema.user import Token, TokenData, UserUpdate, UserCreate, UserResponse
from app.db.session import get_db
from app.services.crypt import verify_password
from app.services.email_service import send_email
from app.services.generator import user_generator
from app.services.multi_crud_service import reset_password
from app.services.verify import verify_password_, verify_email

router = APIRouter()

ALL_AUTH_ROLES = [Role.ADMIN, Role.AUXILIAR]


@router.post("/", response_model=dict)
def create_new_auth_user(user: UserCreate,
                         db: Session = Depends(get_db),
                         current_user: TokenData = Depends(get_current_user)):
    """
       English:
       --------
       Create a new User:

       - **username** (required): Username to login.
       - **password** (required): Password with:
            - One Letter in UpperCase.
            - One Number.
            - 8 character length.
            - One Special character.
       - **email** (required): New email.
       - **role** (required): Role of the user. Must be one of:
            - **admin**: An admin user.
            - **auxiliar**: An auxiliar user.
       Español:
       --------
       Crear un nuevo usuario:

       - **username** (required): Nombre de usuario para iniciar sesión.
       - **password** (required): Contraseña con:
            - Una letra en mayúscula.
            - Un número.
            - Longitud de 8 caracteres.
            - Un caracter especial.
       - **email** (required): Correo electrónico.
       - **role** (required): Rol del usuario. Debe ser uno de los siguientes:
            - **admin**: Usuario administrador.
            - **auxiliar**: Usuario auxiliar.
       """
    if current_user.role.value not in [Role.ADMIN]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if not verify_email(user.email):
        raise HTTPException(status_code=400, detail="Correo inválido")
    if not verify_password_(user.password):
        raise HTTPException(status_code=400, detail="La contraseña debe contener almenos una letra y un numero")
    auth_user = create_auth_user(db, user)
    return auth_user


@router.post("/generate_user", response_model=dict)
def generate_new_auth_user(background_tasks: BackgroundTasks,
                           email: str,
                           role: Role,
                           db: Session = Depends(get_db),
                           current_user: TokenData = Depends(get_current_user)):
    """
       English:
       --------
       Generate a new User:

       - **email** (required): New email.
       - **role** (required): Role of the user. Must be one of:
            - **admin**: An admin user.
            - **auxiliar**: An auxiliar user.

       Español:
       --------
       Generar un nuevo usuario:

       - **email** (required): Correo electrónico.
       - **role** (required): Rol del usuario. Debe ser uno de los siguientes:
            - **admin**: Usuario administrador.
            - **auxiliar**: Usuario auxiliar.
       """
    if current_user.role.value not in [Role.ADMIN]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if not verify_email(email):
        raise HTTPException(status_code=400, detail="Correo inválido")
    user, data_for_email = user_generator(email, role)
    auth_user = auto_create_auth_user(db, user)
    if not isinstance(auth_user, HTTPException):
        background_tasks.add_task(send_email, email, "Credenciales de acceso", data_for_email, "user.html")
        return auth_user
    else:
        return auth_user


@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                           db: Session = Depends(get_db)):
    """
       English:
       --------
       Login for Access Token:

       - **username** (required): Username to login.
       - **password** (required): Password of the user.

       Español:
       --------
       Iniciar sesión para obtener un token de acceso:

       - **username** (requerido): Nombre de usuario.
       - **password** (requerido): Contraseña del usuario.

       """
    user = get_user(db, username=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get('/', response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db),
                  current_user: TokenData = Depends(get_current_user)):
    if current_user.role.value not in ALL_AUTH_ROLES:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    response = read_all_users(db)
    if not response:
        raise HTTPException(status_code=404, detail="No se encontraron Usuarios")
    return response


@router.put("/update", response_model=dict)
def update_user_basic_information(user: UserUpdate,
                                  db: Session = Depends(get_db),
                                  current_user: TokenData = Depends(get_current_user)):
    """
       English:
       --------
       Update User:

       - **username** (optional): New username.
       - **email** (optional): New email.

       Español:
       --------
       Actualizar usuario:

       - **username** (optional): Nuevo nombre de usuario.
       - **email** (optional): Nuevo email.
       """
    if current_user.role.value not in ALL_AUTH_ROLES:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if user.email and not verify_email(user.email):
        raise HTTPException(status_code=400, detail="Correo inválido")
    user = update_auth_user_basic_information(db, user, current_user.username)
    return user


@router.put("/update/password", response_model=dict)
def update_user_password(actual_password: str,
                         new_password: str,
                         db: Session = Depends(get_db),
                         current_user: TokenData = Depends(get_current_user)):
    """
       English:
       --------
       Update password:

       - **actual_password** (required): Actual user password.
       - **new_password** (required): New user password.

       Español:
       --------
       Actualizar contraseña:

       - **actual_password** (required): Actual user password.
       - **new_password** (required): New user password.
       """
    if current_user.role.value not in ALL_AUTH_ROLES:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if not verify_password_(new_password):
        raise HTTPException(status_code=400, detail="La contraseña debe contener almenos una letra y un numero")
    user = update_auth_user_password(db, current_user.username, actual_password, new_password)
    return user


@router.post('/reset_password/send')
async def send_reset_password_code(
        background_tasks: BackgroundTasks,
        email: EmailStr = Form(...),
        db: Session = Depends(get_db)
):
    """
       English:
       --------
       Send recovery password email:

       - **email** (required): Email of a existing user.

       Español:
       --------
        Enviar un correo electrónico para la recuperación de contraseña:

       - **email** (required): Correo electrónico de un usuario existente.
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
                background_tasks.add_task(send_email, email, subject, context, "email.html")
        return {"message": "Si el correo existe, el código sera enviado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/reset_password/verify', response_model=dict)
async def verify_password_code(
        code: int,
        db: Session = Depends(get_db)
):
    """
           English:
           --------
           Verify recovery password code:

           - **code** (required): Code sent.

           Español:
           --------
            Verificar código de recuperación de contraseña:

           - **code** (required): Código enviado.
    """
    is_verified, id_user = verify_token(db, code)
    if is_verified and is_verified is not None:
        return {'is_valid': True, 'message': 'Código valido'}
    if not is_verified and is_verified is not None:
        raise HTTPException(status_code=410, detail="Código expirado")
    raise HTTPException(status_code=400, detail="Código invalido")


@router.post('/reset_password/reset', response_model=dict)
async def reset_forgotten_password(
        code: int,
        new_password: str,
        db: Session = Depends(get_db)):
    """
           English:
           --------
           Reset password with a verify code:

           - **code** (required): Code sent.
           - **password** (required): New password with:
                - One Letter in UpperCase
                - One Number
                - 8 character length
                - One Special character

           Español:
           --------
            Resetear la contraseña con un código de recuperación:

           - **code** (required): Código enviado.
           - **new_password** (required): Nueva contraseña con:
                - Una letra en mayúscula
                - Un número
                - Longitud de 8 caracteres
                - Un caracter especial
        """
    if not verify_password_(new_password):
        raise HTTPException(status_code=400, detail="La contraseña debe contener almenos una letra y un numero")
    return reset_password(db, code, new_password)


@router.delete('/delete/{user_id}', response_model=dict)
def delete_auth_user_by_id(user_id: int, db: Session = Depends(get_db),
                           current_user: TokenData = Depends(get_current_user)):
    """
           English:
           --------
           Delete user by id:

           - **user_id** (required): User id to be eliminated.

           Español:
           --------
            Eliminar usuario por su id:

           - **user_id** (required): Id de usuario a ser eliminado.
    """
    if current_user.role.value not in [Role.ADMIN]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    auth_response = delete_auth_user(db, user_id, current_user.username)
    return auth_response
