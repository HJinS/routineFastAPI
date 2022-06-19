from fastapi.testclient import TestClient

from .routes import user_app

client = TestClient(user_app)


def test_register():
    register_data = {
        'email': 'test_user@example.com',
        'first_name': 'test_firstname',
        'last_name': 'test_lastname',
        'password': 'test_password1234!@#$',
        'confirm_password': 'test_password1234!@#$',
    }
    response = client.post('/users/v1/register', json=register_data)
    response_json = response.json()
    assert response.status_code == 200
    assert 'access_token' in response_json
    assert 'refresh_token' in response_json


def test_register_short_password():
    register_data = {
        'email': 'test_user@example.com',
        'first_name': 'test_firstname',
        'last_name': 'test_lastname',
        'password': 'test12!',
        'confirm_password': 'test12!',
    }
    response = client.post('/users/v1/register', json=register_data)
    response_json = response.json()
    assert response.status_code == 400
    assert {'Validation Error': 'The length should be greater than 8'} == response_json
