from typing import Generator, Any
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import pytest

from commons.config.db import Base
from root.routes import app as _app

db_url = 'postgresql://routine_fast_test:test_user@localhost/routine_fast_api'
db_engine = create_engine(db_url, echo=False)
test_session = sessionmaker(autocommit=False, autoflush=True, bind=db_engine)


def start_application():
    test_app = FastAPI()
    test_app.mount(_app)
    return test_app


@pytest.fixture(scope='function')
def app() -> Generator[FastAPI, Any, None]:
    Base.metadata.create_all(db_engine)
    test_application = start_application()
    yield test_application
    Base.metadata.drop_all(db_engine)


@pytest.fixture(scope='function')
def db_session(app: FastAPI) -> Generator[test_session, Any, None]:
    connection = db_engine.connect()
    transaction = connection.begin()
    session = test_session(bine=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope='function')
def client(app: FastAPI, db_sesion: test_session) -> Generator[TestClient, Any, None]:

    def _get_test_db():
        try:
            yield db_sesion
        finally:
            pass
    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client
