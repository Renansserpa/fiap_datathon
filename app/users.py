from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import get_session
from models import User
from schemas import (
    Message,
    UserPublic,
    UserSchema,
)
from security import (
    get_current_user,
    get_password_hash,
)

router = APIRouter(prefix='/users', tags=['users'])
Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/create', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session):
    # Realiza o método POST no endpoint /users/create para criar um usuário no banco de dados
    #
    # Argumentos:
    #   user: É um parâmetro contendo as informações do usuário desejado
    #   session: É apenas um parâmetro para que seja possível iniciar uma sessão com o banco de dados
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists',
            )

    hashed_password = get_password_hash(user.password)

    db_user = User(
        email=user.email,
        username=user.username,
        password=hashed_password,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.put('/update/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int,
    user: UserSchema,
    session: Session,
    current_user: CurrentUser,
):
    # Realiza o método PUT no endpoint /users/update/{user_id} para atualizar um usuário no banco de dados
    #
    # Argumentos:
    #   user_id: É um parâmetro contendo o id de banco de dados do usuário desejado (a ser atualizado)
    #   user: É um parâmetro contendo as alterações para o usuario especificado no parâmetro anterior
    #   current_user: É um parâmetro contendo o usuario atual logado na API (se não estiver logado não será possível realizar a atualização)
    #   session: É apenas um parâmetro para que seja possível iniciar uma sessão com o banco de dados
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    try:
        current_user.username = user.username
        current_user.password = get_password_hash(user.password)
        current_user.email = user.email
        session.commit()
        session.refresh(current_user)

        return current_user

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or Email already exists',
        )


@router.delete('/delete/{user_id}', response_model=Message)
def delete_user(
    user_id: int,
    session: Session,
    current_user: CurrentUser,
):
    # Realiza o método DELETE no endpoint /users/delete/{user_id} para deletar um usuário no banco de dados
    #
    # Argumentos:
    #   user_id: É um parâmetro contendo o id de banco de dados do usuário desejado (a ser removido)
    #   current_user: É um parâmetro contendo o usuario atual logado na API (se não estiver logado não será possível realizar a remoção)
    #   session: É apenas um parâmetro para que seja possível iniciar uma sessão com o banco de dados
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    session.delete(current_user)
    session.commit()

    return {'message': 'User deleted'}