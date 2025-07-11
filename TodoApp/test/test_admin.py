from fastapi import status
from .utils import *
from .utils import override_get_current_user
from ..router.admin import get_current_user,get_db
from ..model import Todos

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_admin_read_all_authentication(test_todos):
    response = client.get('/admin/todos')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'title': 'Learn to code',
    'description': 'Learn more about code',
    'priority': 1,
    'complete': False,
    'id': 1,
    'owner_id': 1}]

def test_admin_deleting_all_todos(test_todos):
    response = client.delete('/admin/todos/1')
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None

# def test_admin_deleting_all_todos_not_found():
#     response = client.delete('/admin/todos/99')
#     assert response.status_code == 404
#     assert response.json()=={'details':'Todo not found'}