from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr.database import get_session
from madr.models import Book, User
from madr.sanitize import sanitize
from madr.schemas import BookList, BookPublic, BookSchema, BookUpdate, Message
from madr.security import get_current_user

router = APIRouter(prefix='/livro', tags=['livros'])
T_Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', response_model=BookPublic, status_code=HTTPStatus.CREATED)
def create_book(book: BookSchema, user: CurrentUser, session: T_Session):
    db_book = session.scalar(select(Book).where(Book.titulo == book.titulo))

    if db_book:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Livro já consta no MADR',
        )

    db_book = Book(ano=book.ano, titulo=sanitize(book.titulo))

    session.add(db_book)
    session.commit()
    session.refresh(db_book)

    return db_book


@router.delete('/{book_id}', response_model=Message)
def delete_book(book_id: int, session: T_Session, user: CurrentUser):
    db_book = session.scalar(select(Book).where(Book.id == book_id))

    if not db_book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Livro não consta no MADR'
        )

    session.delete(db_book)
    session.commit()

    return {'message': 'Livro deletado no MADR'}


@router.patch('/{book_id}', response_model=BookPublic)
def patch_book(
    book_id: int, book: BookUpdate, session: T_Session, user: CurrentUser
):
    db_book = session.scalar(select(Book).where(Book.id == book_id))

    if not db_book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Livro não consta no MADR',
        )

    for key, value in book.model_dump(exclude_unset=True).items():
        if key == 'titulo':
            value = sanitize(value)  # noqa
        setattr(db_book, key, value)

    session.add(db_book)
    session.commit()
    session.refresh(db_book)

    return db_book


@router.get('/{book_id}', response_model=BookPublic)
def get_book(book_id: int, session: T_Session):
    db_book = session.scalar(select(Book).where(Book.id == book_id))

    if not db_book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Livro não consta no MADR'
        )

    return db_book


@router.get('/', response_model=BookList)
def get_book_by_params(
    session: T_Session,
    titulo: str | None = Query(None),
    ano: str | None = Query(None),
):
    query = select(Book)

    if titulo:
        query = query.filter(Book.titulo.contains(titulo))

    if ano:
        query = query.filter(Book.ano.contains(ano))

    books = session.scalars(query.limit(20)).all()

    return {'livros': books}
