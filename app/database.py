import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# from settings import Settings
DATABASE_URL = os.environ['DATABASE_URL']

engine = create_engine(DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session