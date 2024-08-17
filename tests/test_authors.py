from http import HTTPStatus

from madr.models import Author
from madr.sanitize import sanitize


def test_create_author(client, token):
    response = client.post(
        '/author/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'Test Author',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'name': 'test author',
    }


def test_create_duplicate_author(client, author, token):
    response = client.post(
        '/author/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': author.name,
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Autor já consta no MADR'}


def test_delete_author(client, author, token):
    response = client.delete(
        f'/author/{author.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Autor deletado no MADR'}


def test_delete_author_error(client, token):
    response = client.delete(
        f'/author/{10}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Autor não consta no MADR'}


def test_patch_author(client, author, token):
    response = client.patch(
        f'/author/{author.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'Test Changed'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['name'] == 'test changed'


def test_patch_author_error(client, author, token):
    response = client.patch(
        f'/author/{10}',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'Test!'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Autor não consta no MADR'}


def test_get_author_by_id(client, author):
    response = client.get(
        f'/author/{author.id}',
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'id': 1, 'name': 'test author'}


def test_get_author_by_id_error(client):
    response = client.get(f'/author/{9999}')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Autor não consta no MADR'}


def test_get_author_by_params(client, session):
    expected_authors = 2

    author1 = Author(name=sanitize('Test Novelist 1'))

    author2 = Author(name=sanitize('Test Novelist 2'))

    session.add(author1)
    session.add(author2)
    session.commit()

    response = client.get(
        '/author/?name=test',
    )

    assert len(response.json()['autores']) == expected_authors
