from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo
import os

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, ExpiredSignatureError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_session
from models import User
from schemas import TokenData
from exceptions import (
    NotAuthenticated,
    ExpiredToken
)

#settings = Settings()
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.environ['ACCESS_TOKEN_EXPIRE_MINUTES'])
ALGORITHM = os.environ['ALGORITHM']
SECRET_KEY = os.environ['SECRET_KEY']

pwd_context = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')

def create_access_token(data: dict):
    # Cria um JWT com base nas informações especificadas no arquivo de configuração .env (importadas através da constante settings)
    #   Algoritmo: HS256
    #   Tempo de duracao: 30 minutos
    #
    # Argumentos:
    #   data: É um parâmetro contendo informações desejadas para serem incluídas no JWT (no caso, o email do usuário)
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes= ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})
    encoded_jwt = encode(
        to_encode, SECRET_KEY, algorithm= ALGORITHM
    )
    return encoded_jwt


def get_password_hash(password: str):
    # Retorna o hash (a partir do algoritmo argon2) da senha fornecida
    #
    # Argumentos:
    #   password: É um parâmetro contendo a senha que terá o hash calculado
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    # Retorna se o hash da senha em clear text é o mesmo que o hash sendo fornecido
    #
    # Argumentos:
    #   plain_password: É um parâmetro contendo a senha em clear text
    #   hashed_password: É um parâmetro contendo o hash desejado (a ser comparado com o hash a ser calculado
    #                       baseado na senha fornecida no parâmetro anterior)
    return pwd_context.verify(plain_password, hashed_password)


def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):
    # Retorna se o usuário existe no Banco de dados e se o JWT fornecido através do header da request não expirou
    #
    # Argumentos:
    #   token: É um parâmetro contendo as informacoes do token JWT do usuário
    #   session: É apenas um parâmetro para que seja possível iniciar uma sessão com o banco de dados

    try:
        payload = decode(
            token, SECRET_KEY, algorithms=[ALGORITHM]
        )
        user_email: str = payload.get('sub')
        if not user_email:
            raise NotAuthenticated
        token_data = TokenData(user_email=user_email)
    except DecodeError:
        raise NotAuthenticated
    except ExpiredSignatureError:
        raise ExpiredToken

    user = session.scalar(
        select(User).where(User.email == token_data.user_email)
    )

    if not user:
        raise NotAuthenticated

    return user