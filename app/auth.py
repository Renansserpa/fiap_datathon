from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import get_session
from .exceptions import UserNotFound
from .models import User
from .schemas import Token
from .security import (
    create_access_token,
    verify_password,
)

router = APIRouter(prefix='/auth', tags=['auth'])

OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
Session = Annotated[Session, Depends(get_session)]


@router.post('/token', response_model=Token)
def login_for_access_token(form_data: OAuth2Form, session: Session):
    # Verifica se a combinação de usuário e senha fornecidos no formulário de login são válidos e retorna um JWT caso positivo
    #
    # Argumentos:
    #   form_data: É um parâmetro contendo a credencial fornecida no formulario de login
    #   session: É apenas um parâmetro para que seja possível iniciar uma sessão com o banco de dados
    user = session.scalar(select(User).where(User.email == form_data.username))

    if not user or not verify_password(form_data.password, user.password):
        raise UserNotFound

    access_token = create_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'bearer'}