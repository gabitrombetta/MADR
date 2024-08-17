from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]


@table_registry.mapped_as_dataclass
class Author:
    __tablename__ = 'authors'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    books: Mapped[list['Book']] = relationship(
        'Book',
        init=False,
        back_populates='author',
        cascade='all, delete-orphan',
    )


@table_registry.mapped_as_dataclass
class Book:
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    year: Mapped[str]
    title: Mapped[str] = mapped_column(unique=True)

    author_id: Mapped[int] = mapped_column(ForeignKey('authors.id'))

    author: Mapped[Author] = relationship(
        'Author', init=False, back_populates='books'
    )
