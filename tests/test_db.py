from sqlalchemy import select

from madr.models import Novelist, User


def test_create_user(session):
    user = User(
        username='testusername', email='test@email.com', password='test'
    )

    session.add(user)
    session.commit()

    result = session.scalar(select(User).where(User.email == 'test@email.com'))

    assert result.username == 'testusername'


def test_create_novelist(session):
    novelist = Novelist(
        name='Test Name',
    )

    session.add(novelist)
    session.commit()

    result = session.scalar(
        select(Novelist).where(Novelist.name == 'Test Name')
    )

    assert result.id == 1
