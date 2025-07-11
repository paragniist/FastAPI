import pytest
from sqlalchemy import create_engine, StaticPool, text
from sqlalchemy.orm import sessionmaker
from ..database import base
from ..main import app
from ..model import Todos,Users
from fastapi.testclient import TestClient
from ..router.auth import bcrypt_context

SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username': 'Jas', 'id': 1, 'role':'admin'}

client = TestClient(app)


@pytest.fixture
def test_todos():
    db = TestingSessionLocal()
    db.query(Todos).delete()
    db.commit()
    todo = Todos(
        title='Learn to code',
        description='Learn more about code',
        priority=1,
        complete=False,
        owner_id=1
    )
    db.add(todo)
    db.commit()
    db.refresh(todo)
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


@pytest.fixture
def test_users():
    user = Users(
        username='Jas',
        email='jaspreet@gmail.com',
        first_name = 'Jaspreet',
        last_name = 'kaur',
        hashed_password=bcrypt_context.hash('test1234'),
        role='admin',
        phone_number='999999999'
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()

