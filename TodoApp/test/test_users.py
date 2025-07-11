from fastapi import FastAPI
from starlette import status

from .utils import *
from ..router.users import get_current_user,get_db
from ..model import Todos,Users


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_all_information_user(test_users):
    response = client.get("/user/get_users_information")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]['username'] =='Jas'
    assert response.json()[0]['email'] == 'jaspreet@gmail.com'
    assert response.json()[0]['first_name'] == 'Jaspreet'
    assert response.json()[0]['last_name'] == 'kaur'
    assert response.json()[0]['role'] == 'admin'
    assert response.json()[0]['phone_number'] =='999999999'

def test_change_password_success(test_users):
    response = client.put("/user/update_password",json={'password':'test1234','new_password':'test12345'})
    assert response.status_code == status.HTTP_204_NO_CONTENT

# def test_change_password_failure():
#     response = client.put("/user/update_password", json={'password': 'testwrongpassword', 'new_password': 'test12345'})
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED
#     assert response.json()=={'detail':"Incorrect password."}

def test_change_phone_number_success(test_users):
    response = client.put("/user/update_phone_number/999999999")
    assert response.status_code == status.HTTP_204_NO_CONTENT

# def test_change_phone_number_failure():
#     response = client.put("/user/update_phone_number/222")
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED
#     assert response.json()=={'detail':"Incorrect phone number."}