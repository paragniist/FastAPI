from fastapi import status
from ..router.todos import get_db, get_current_user
from .utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_read_all_authenticated(test_todos):
    response = client.get("/todos/read_all")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        'title': 'Learn to code',
        'id': 1,  # Dynamically match the ID
        'description': 'Learn more about code',
        'owner_id': 1,
        'complete': False,
        'priority': 1
    }]


def test_read_one_authenticated(test_todos):
    todo_id = test_todos.id
    response = client.get(f"/todos/read_todos_by_id/{todo_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'title': 'Learn to code',
        'id': 1,
        'description': 'Learn more about code',
        'owner_id': 1,
        'complete': False,
        'priority': 1
    }

def test_red_one_authenticated_not_found():
    response = client.get("/todos/999")
    assert response.status_code == status.HTTP_200_OK
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()== {'details':'Todo not found'}

def test_create_todo(test_todos):
    request_data={
        'title':'New Todos',
        'description':'New description',
        'priority':1,
        'complete':False,
    }
    response = client.post("/todos/creating_todo",json=request_data)
    assert response.status_code == status.HTTP_201_CREATED

    db= TestingSessionLocal()
    model =db.query(Todos).filter(Todos.id==2).first()
    assert model.title==request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')

def test_update_todo(test_todos):
    request_data={
        'title':'New Todos',
        'description':'New description',
        'priority':1,
        'complete':False,
    }
    response = client.put(f"/todos/updating_todo/1", json=request_data)
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == 'New Todos'

def test_update_todo_not_found():
    request_data={
        'title':'New Todos',
        'description':'New description',
        'priority':1,
        'complete':False,
    }
    response = client.put(f"/todos/updating_todo/99", json=request_data)
    assert response.status_code == 204
    assert response.json() == {'details':'Todo not found'}


def test_delete_todo(test_todos):
    response = client.delete("/todos/selecting_todo/1")
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None

def test_delete_todo_not_found():
    response = client.delete("/todos/selecting_todo/99")
    assert response.status_code == 204
    assert response.json() == {
        'details':'Todo not found'
    }
