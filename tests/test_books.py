from http import HTTPStatus

from madr.models import Book
from madr.sanitize import sanitize


def test_create_book(client, token, author):
    response = client.post(
        '/book/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'year': '2024',
            'title': 'New Book',
            'author_id': author.id,
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'year': '2024',
        'title': 'new book',
        'author_id': author.id,
    }


def test_create_book_author_doesnt_exist(client, token):
    response = client.post(
        '/book/',
        headers={'Authorization': f'Bearer {token}'},
        json={'year': '2024', 'title': 'New Book', 'author_id': 999},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Autor não consta no MADR'}


def test_create_duplicate_book(client, token, book):
    response = client.post(
        '/book/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'year': book.year,
            'title': book.title,
            'author_id': book.author_id,
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Livro já consta no MADR'}


def test_delete_book(client, book, token):
    response = client.delete(
        f'/book/{book.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Livro deletado no MADR'}


def test_delete_book_error(client, token):
    response = client.delete(
        f'/book/{10}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Livro não consta no MADR'}


def test_patch_book(client, book, token):
    response = client.patch(
        f'/book/{book.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'Teste Change', 'year': '2000'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['title'] == 'teste change'


def test_patch_book_error(client, book, token):
    response = client.patch(
        f'/book/{10}',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'Teste Change', 'year': '2000'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Livro não consta no MADR'}


def test_get_book(client, book):
    response = client.get(f'/book/{book.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'title': 'test book',
        'year': '1999',
        'author_id': 1,
    }


def test_get_book_error(client):
    response = client.get(f'/book/{999}')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Livro não consta no MADR'}


def test_get_book_by_params_should_return_2(client, session, author):
    expected_books = 2

    book1 = Book(
        year='1999', title=sanitize('Test Book 1'), author_id=author.id
    )

    book2 = Book(
        year='1999', title=sanitize('Test Book 2'), author_id=author.id
    )

    session.add(book1)
    session.add(book2)
    session.commit()

    response = client.get(
        '/book/?title=test&year=199',
    )

    assert len(response.json()['livros']) == expected_books


def test_get_book_by_params_should_return_nothing(
    client
):
    response = client.get(
        '/book/?title=test&year=199',
    )

    assert response.json() == {'livros': []}
