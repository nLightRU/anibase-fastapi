from fastapi import status

def test_register_success(client):
    payload = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'secretpass123',
    }
    response = client.post('/auth/register', json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data['username'] == 'testuser'
    assert data['email'] == 'test@example.com'
    assert 'id' in data

def test_login_success(client):
    payload = {
        'email': 'testuser@example.com',
        'password': 'asdfasdfasd',
    }
    response = client.post('/auth/login', json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert 'access_token' in data
    assert data['token_type'] == 'bearer'
