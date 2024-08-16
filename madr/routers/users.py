from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr.database import get_session
from madr.models import User
from madr.schemas import Message, UserPublic, UserSchema
from madr.security import get_current_user, get_password_hash

router = APIRouter(prefix='/conta', tags=['users'])
T_Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', response_model=UserPublic, status_code=HTTPStatus.CREATED)
def create_user(user: UserSchema, session: T_Session):
    db_user = session.scalar(
        select(User).where(
            User.username == user.username, User.email == user.email
        )
    )

    if db_user:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Conta já consta no MADR',
        )

    db_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.put('/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int,
    user: UserSchema,
    session: T_Session,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail='Não autorizado'
        )

    current_user.username = user.username
    current_user.email = user.email
    current_user.password = get_password_hash(user.password)

    session.commit()
    session.refresh(current_user)

    return current_user


@router.delete('/{user_id}', response_model=Message)
def delete_user(user_id: int, session: T_Session, current_user: CurrentUser):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail='Não autorizado'
        )

    session.delete(current_user)
    session.commit()

    return {'message': 'Conta deletada com sucesso'}
