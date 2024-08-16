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


def test_update_user(client, user, token):
    response = client.put(
        f'/conta/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
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


def test_update_user_error(client, token, other_user):
    response = client.put(
        f'/conta/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'testusername',
            'email': 'test@email.com',
            'password': 'test',
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Não autorizado'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/conta/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Conta deletada com sucesso'}


def test_delete_user_error(client, token, other_user):
    response = client.delete(
        f'/conta/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Não autorizado'}
