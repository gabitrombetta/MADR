from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr.database import get_session
from madr.models import Author, User
from madr.sanitize import sanitize
from madr.schemas import (
    AuthorList,
    AuthorPublic,
    AuthorSchema,
    AuthorUpdate,
    Message,
)
from madr.security import get_current_user

router = APIRouter(prefix='/author', tags=['authors'])
T_Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', response_model=AuthorPublic, status_code=HTTPStatus.CREATED)
def create_author(author: AuthorSchema, user: CurrentUser, session: T_Session):
    db_author = session.scalar(
        select(Author).where(Author.name == author.name)
    )

    if db_author:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Autor já consta no MADR',
        )

    db_author = Author(
        name=sanitize(author.name),
    )

    session.add(db_author)
    session.commit()
    session.refresh(db_author)

    return db_author


@router.delete('/{author_id}', response_model=Message)
def delete_author(author_id: int, session: T_Session, user: CurrentUser):
    db_author = session.scalar(select(Author).where(Author.id == author_id))

    if not db_author:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Autor não consta no MADR',
        )

    session.delete(db_author)
    session.commit()

    return {'message': 'Autor deletado no MADR'}


@router.patch('/{author_id}', response_model=AuthorPublic)
def patch_author(
    author_id: int,
    session: T_Session,
    user: CurrentUser,
    author: AuthorUpdate,
):
    db_author = session.scalar(select(Author).where(Author.id == author_id))

    if not db_author:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Autor não consta no MADR',
        )

    for key, value in author.model_dump(exclude_unset=True).items():
        if key == 'name':
            value = sanitize(value)  # noqa
        setattr(db_author, key, value)

    session.add(db_author)
    session.commit()
    session.refresh(db_author)

    return db_author


@router.get('/{author_id}', response_model=AuthorPublic)
def get_author(
    author_id: int,
    session: T_Session,
):
    db_author = session.scalar(select(Author).where(Author.id == author_id))

    if not db_author:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Autor não consta no MADR',
        )

    return db_author


@router.get('/', response_model=AuthorList)
def get_author_by_params(session: T_Session, name: str | None = Query(None)):
    query = select(Author)

    if name:
        query = query.filter(Author.name.contains(name))

    authors = session.scalars(query.limit(20)).all()

    return {'autores': authors}
