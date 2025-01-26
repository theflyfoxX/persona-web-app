import pytest
from app.schemas.user_schema import  UserResponse
from app.schemas.token_schema import  Token
from app.configuration import settings
from jose import jwt

def test_create_user(client):
    res = client.post(
        "/users/", json={"username": "hello", "email": "hello@email.com","password": "Password123@","confirm_password": "Password123@"})

    new_user = UserResponse(**res.json())
    assert new_user.email == "hello@email.com"
    assert res.status_code == 201


def test_login_user(test_user, client):
    res = client.post(
        "/auth/login", data={"username": test_user['username'], "password": test_user['password']}
    )
    login_res = Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200



@pytest.mark.parametrize("email, password, status_code", [
    ('saad', 'password123', 403),
    ('marwa', 'wrongpassword', 403),
    ('samuel', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('sara', None, 422),
])
def test_incorrect_login(client, email, password, status_code):
    data = {}
    if email is not None:
        data["username"] = email
    if password is not None:
        data["password"] = password
    
    res = client.post("/auth/login", data=data)

    assert res.status_code == status_code
    if status_code == 403:
        assert res.json().get('detail') in ['Invalid Credentials', 'Incorrect username or password']
    elif status_code == 422:
        # Optionally, check for validation error details
        assert res.json().get('detail') is not None
