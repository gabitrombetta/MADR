from http import HTTPStatus

from tests.conftest import BookFactory


def test_create_book(client, token):
    response = client.post(
        '/livro/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'ano': '1999',
            'titulo': 'test book',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'ano': '1999',
        'titulo': 'test book',
    }


def test_create_duplicate_book(client, book, token):
    response = client.post(
        '/livro/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'ano': book.ano,
            'titulo': book.titulo,
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Livro já consta no MADR'}


def test_delete_book(client, book, token):
    response = client.delete(
        f'/livro/{book.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Livro deletado no MADR'}


def test_delete_book_error(client, token):
    response = client.delete(
        f'/livro/{10}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Livro não consta no MADR'}


def test_patch_book(client, book, token):
    response = client.patch(
        f'/livro/{book.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'titulo': 'Teste Change', 'ano': '2000'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['titulo'] == 'teste change'


def test_patch_book_error(client, book, token):
    response = client.patch(
        f'/livro/{10}',
        headers={'Authorization': f'Bearer {token}'},
        json={'titulo': 'Teste Change', 'ano': '2000'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Livro não consta no MADR'}


def test_get_book(client, book):
    response = client.get(f'/livro/{book.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'id': 1, 'titulo': 'test book 4', 'ano': '1994'}


def test_get_book_by_params(client, session):
    expected_books = 2

    session.bulk_save_objects(
        BookFactory.create_batch(1, titulo='Test Name 1', ano='1991')
    )

    session.bulk_save_objects(
        BookFactory.create_batch(1, titulo='Test Name 2', ano='1992')
    )
    session.commit()

    response = client.get(
        '/livro/?titulo=Test&ano=199',
    )

    assert len(response.json()['livros']) == expected_books


def test_get_book_error(client):
    response = client.get(f'/livro/{999}')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Livro não consta no MADR'}
