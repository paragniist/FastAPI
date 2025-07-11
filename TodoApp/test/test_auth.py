from jose import jwt

from .utils import *
from ..router.auth import get_db,authenticate_user,create_access_token,SECRET_KEY,ALGORITHM,get_current_user
from datetime import timedelta
import pytest
from fastapi import HTTPException
app.dependency_overrides[get_db] = override_get_db

def test_authenticate_user(test_users):
    db = TestingSessionLocal()
    authenticated_user = authenticate_user(test_users.username,'test1234',db)
    assert authenticated_user is not False
    assert authenticated_user.username == test_users.username

    non_existent_user = authenticate_user('username','test1234',db)
    assert non_existent_user is False

    wrong_password = authenticate_user(test_users.username,'1234sdt',db)
    assert wrong_password is False


def test_create_access_token(test_users):
    username = 'testuser'
    user_id =1
    role = 'admin'
    expires_delta = timedelta(days=1)

    token = create_access_token(username,user_id,role,expires_delta)
    decode_token = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM],options={'verify_signatures':False})

    assert decode_token['sub'] == username
    assert decode_token['id'] ==  user_id
    assert decode_token['role'] == role

@pytest.mark.asyncio
async def  test_get_current_user():
    encode = {'sub':'testuser','id':1,'role':'admin'}
    token = jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)

    user = await get_current_user(token=token)
    assert user == {'username':'testuser','id':1,'role':'admin'}


@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
     encode = {'role':'user'}
     token = jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)

     with pytest.raises(HTTPException) as excinfo:
          await get_current_user(token=token)

     assert excinfo.value.status_code == 401
     assert excinfo.value.detail == 'Invalid token'
