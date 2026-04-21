from fastapi.testclient import TestClient

from src.main import app
client = TestClient(app)

# Существующие пользователи
users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]

def test_get_existed_user():
    '''Получение существующего пользователя'''
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]


def test_get_unexisted_user():
    '''Получение несуществующего пользователя'''
    response = client.get("/api/v1/user", params={'email': 'unknown@mail.com'})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    data = {
        "name": "Sergey Sergeev",
        "email": "s.s.sergeev@mail.com"
    }

    response = client.post("/api/v1/user", json=data)
    assert response.status_code == 201

    new_user_id = response.json()
    assert isinstance(new_user_id, int)

    get_response = client.get("/api/v1/user", params={"email": data["email"]})
    assert get_response.status_code == 200
    assert get_response.json() == {
        "id": new_user_id,
        "name": data["name"],
        "email": data["email"]
    }


def test_create_user_with_invalid_email():
    '''Создание пользователя с почтой, которую использует другой пользователь'''
    data = {
        "name": "Another User",
        "email": users[0]["email"]
    }

    response = client.post("/api/v1/user", json=data)
    assert response.status_code == 409
    assert response.json() == {"detail": "User with this email already exists"}


def test_delete_user():
    '''Удаление пользователя'''
    data = {
        "name": "Delete Me",
        "email": "delete.me@mail.com"
    }

    create_response = client.post("/api/v1/user", json=data)
    assert create_response.status_code == 201

    delete_response = client.delete("/api/v1/user", params={"email": data["email"]})
    assert delete_response.status_code == 204

    get_response = client.get("/api/v1/user", params={"email": data["email"]})
    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "User not found"}
