from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr.database import get_session
from madr.models import Novelist, User
from madr.sanitize import sanitize
from madr.schemas import (
    Message,
    NovelistList,
    NovelistPublic,
    NovelistSchema,
    NovelistUpdate,
)
from madr.security import get_current_user

router = APIRouter(prefix='/romancista', tags=['romancistas'])
T_Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post(
    '/', response_model=NovelistPublic, status_code=HTTPStatus.CREATED
)
def create_novelist(
    novelist: NovelistSchema, user: CurrentUser, session: T_Session
):
    db_novelist = session.scalar(
        select(Novelist).where(Novelist.name == novelist.name)
    )

    if db_novelist:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Romancista já consta no MADR',
        )

    db_novelist = Novelist(
        name=sanitize(novelist.name),
    )

    session.add(db_novelist)
    session.commit()
    session.refresh(db_novelist)

    return db_novelist


@router.delete('/{novelist_id}', response_model=Message)
def delete_novelist(novelist_id: int, session: T_Session, user: CurrentUser):
    db_novelist = session.scalar(
        select(Novelist).where(Novelist.id == novelist_id)
    )

    if not db_novelist:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Romancista não consta no MADR',
        )

    session.delete(db_novelist)
    session.commit()

    return {'message': 'Romancista deletado no MADR'}


@router.patch('/{novelist_id}', response_model=NovelistPublic)
def patch_novelist(
    novelist_id: int,
    session: T_Session,
    user: CurrentUser,
    novelist: NovelistUpdate,
):
    db_novelist = session.scalar(
        select(Novelist).where(Novelist.id == novelist_id)
    )

    if not db_novelist:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Romancista não consta no MADR',
        )

    for key, value in novelist.model_dump(exclude_unset=True).items():
        setattr(db_novelist, key, value)

    session.add(db_novelist)
    session.commit()
    session.refresh(db_novelist)

    return db_novelist


@router.get('/{novelist_id}', response_model=NovelistPublic)
def get_novelist(
    novelist_id: int,
    session: T_Session,
):
    db_novelist = session.scalar(
        select(Novelist).where(Novelist.id == novelist_id)
    )

    if not db_novelist:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Romancista não consta no MADR',
        )

    return db_novelist


@router.get('/', response_model=NovelistList)
def get_novelist_by_params(session: T_Session, name: str | None = Query(None)):
    query = select(Novelist)

    if name:
        query = query.filter(Novelist.name.contains(name))

    novelists = session.scalars(query.limit(20)).all()

    return {'romancistas': novelists}
