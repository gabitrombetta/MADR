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
