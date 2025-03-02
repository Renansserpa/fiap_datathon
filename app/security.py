from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, ExpiredSignatureError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_session
from models import User
from schemas import TokenData
from settings import Settings

settings = Settings()
pwd_context = PasswordHash.recommended()


def create_access_token(data: dict):
    # Cria um JWT com base nas informações especificadas no arquivo de configuração .env (importadas através da constante settings)
    #   Algoritmo: HS256
    #   Tempo de duracao: 30 minutos
    #
    # Argumentos:
    #   data: É um parâmetro contendo informações desejadas para serem incluídas no JWT (no caso, o email do usuário)
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})
    encoded_jwt = encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
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


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')


def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):
    # Retorna se o usuário existe no Banco de dados e se o JWT fornecido através do header da request não expirou
    #
    # Argumentos:
    #   token: É um parâmetro contendo as informacoes do token JWT do usuário
    #   session: É apenas um parâmetro para que seja possível iniciar uma sessão com o banco de dados
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get('sub')
        if not username:
            raise credentials_exception
        token_data = TokenData(username=username)
    except DecodeError:
        raise credentials_exception
    except ExpiredSignatureError:
        raise credentials_exception

    user = session.scalar(
        select(User).where(User.email == token_data.username)
    )

    if not user:
        raise credentials_exception

    return user