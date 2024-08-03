from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


# Users
class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr


# Token
class Token(BaseModel):
    access_token: str
    token_type: str


# Novelists
class NovelistSchema(BaseModel):
    name: str


class NovelistPublic(BaseModel):
    id: int
    name: str


class NovelistUpdate(BaseModel):
    name: str | None


class NovelistList(BaseModel):
    romancistas: list[NovelistPublic]
