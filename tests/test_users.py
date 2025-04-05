import pytest
from unittest.mock import patch
from http import HTTPStatus
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_session
from app.models import User, table_registry
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session    
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import User  # Replace 'models' with your database models module

# Test database setup
DATABASE_URL = "sqlite:///./tests/test.db"  # Test database file in the current directory
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Ensure test database and schema are created
table_registry.metadata.create_all(bind=engine)

# Dependency override function
def override_get_session():
    """Provide the test database session instead of the production session."""
    with TestingSessionLocal() as session:
        yield session


# FastAPI TestClient
@pytest.fixture
def client():
    app.dependency_overrides[get_session] = override_get_session
    return TestClient(app)


def test_post_json(client):

	#Faz requisição no caminho especificado
    response = client.post(
	   '/users/create',
	   json = {
		    "username": "test_user",
            "email": "test_user2@example.com",
            "password": "test_password"
		}
    )
    
    test_session = next(override_get_session())
    #Tenta conseguir dado do usuário criado
    db_user = test_session.scalar(
        select(User)\
        .where(
            User.email == "test_user2@example.com"
        )
    )

	#Validação se resposta é de sucesso, e se usuário foi criado
    assert response.status_code == HTTPStatus.CREATED
    assert db_user.username == "test_user"
