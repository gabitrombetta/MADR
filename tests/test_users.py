from http import HTTPStatus


def test_create_user(client, session):
    response = client.post(
        '/conta/',
        json={
            'username': 'test',
            'email': 'test@email.com',
            'password': 'testpassword',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'test',
        'email': 'test@email.com',
    }


def test_create_duplicate_user(client, user):
    response = client.post(
        '/conta/',
        json={
            'username': user.username,
            'email': user.email,
            'password': 'test',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Conta já consta no MADR'}


def test_update_user(client, user):
    response = client.put(
        f'/conta/{user.id}',
        json={
            'username': 'testusername2',
            'email': 'test2@email.com',
            'password': 'test',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'testusername2',
        'email': 'test2@email.com',
        'id': 1,
    }


def test_update_wrong_user(client):
    response = client.put(
    '/conta/999',
        json={
            'username': 'testusername',
            'email': 'test@email.com',
            'password': 'test',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client, user):
    response = client.delete(
        f'/conta/{user.id}',
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Conta deletada com sucesso'}


def test_delete_wrong_user(client,):
    response = client.delete(
        '/conta/999',
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
