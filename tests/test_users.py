from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from app.database import get_session
from app.main import app
from app.models import User, table_registry

# Test database setup
DATABASE_URL = "sqlite:///./tests/test.db"  # Test database file in the current directory
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Ensure test database and schema are created
table_registry.metadata.create_all(bind=engine)

usuario_teste = {
    "username": "test_user",
    "email": "test_user2@example.com",
    "password": "test_password"
}


# Dependency override function
def override_get_session():
    """Provide the test database session instead of the production session."""
    with TestingSessionLocal() as session:
        yield session


headers = {"Authorization": "Bearer <token>"}


# FastAPI TestClient
@pytest.fixture
def client():
    app.dependency_overrides[get_session] = override_get_session
    return TestClient(app)


@pytest.fixture
def session():
    with TestingSessionLocal() as test_session:
        yield test_session


def test_create_user(client, session):
	# Faz requisição no caminho especificado
    response = client.post(
        '/users/create',
        json={
            "username": usuario_teste['username'],
            "email": usuario_teste['email'],
            "password": usuario_teste['password']
		}
    )

    # Tenta conseguir dado do usuário criado
    db_user = session.scalar(
        select(User)\
        .where(
            User.email == usuario_teste['email']
        )
    )

	# Validação se resposta é de sucesso, e se usuário foi criado
    assert response.status_code == HTTPStatus.CREATED
    assert db_user.username == usuario_teste['username']


def test_update_user(client, session):

    # Realiza autenticação gerando token
    token = client.post(
        '/auth/token',
        data={
            "username": usuario_teste["email"],
            "password": usuario_teste['password']
		},
    )
    token = token.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}

    # Faz requisição no caminho especificado
    response = client.put(
        f'/users/update/{usuario_teste["email"]}',
        json={
            "username": 'updated_user',
            "password": usuario_teste['password']
		},
        headers=headers
    )

    # Tenta conseguir dado do usuário criado
    db_user = session.scalar(
        select(User)\
        .where(
            User.email == usuario_teste['email']
        )
    )

	# Validação se resposta é de sucesso, e se usuário foi criado
    assert response.status_code == HTTPStatus.OK
    assert db_user.username == 'updated_user'


def test_delete_user(client, session):

    # Realiza autenticação gerando token
    token = client.post(
        '/auth/token',
        data={
        "username": usuario_teste["email"],
        "password": usuario_teste['password']
		},
    )
    token = token.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}

    # Faz requisição no caminho especificado
    response = client.delete(
        f'/users/delete/{usuario_teste["email"]}',
        headers=headers
    )

    # Tenta conseguir dado do usuário criado
    db_user = session.scalar(
        select(User)\
        .where(
            User.email == usuario_teste['email']
        )
    )

	# Validação se resposta é de sucesso, e se usuário foi criado
    assert response.status_code == HTTPStatus.OK
    assert db_user is None