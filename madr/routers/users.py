from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select

from madr.database import get_session
from madr.models import User
from madr.schemas import Message, UserPublic, UserSchema

router = APIRouter(prefix='/conta', tags=['users'])


@router.post('/', response_model=UserPublic, status_code=HTTPStatus.CREATED)
def create_user(user: UserSchema, session=Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail={'message': 'Conta já consta no MADR'},
        )

    db_user = User(
        username=user.username, email=user.email, password=user.password
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.put('/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema, session=Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail={'message': 'Conta não consta no MADR'},
        )

    db_user.username = user.username
    db_user.email = user.email
    db_user.password = user.password

    session.add(db_user)
    session.commit()

    return db_user


@router.delete('/{user_id}', response_model=Message)
def delete_user(user_id: int, session=Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail={'message': 'Conta não consta no MADR'},
        )

    session.delete(db_user)
    session.commit()

    return {'message': 'Conta deletada com sucesso'}
