from conftest import client


def test_register():
    response = client.post('/auth/register', json=
    {
        "email": "user@example.com",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "string",
        "role_id": 0
    })
    assert response.status_code == 201, 'Код не 201'
