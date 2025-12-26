from pydantic import BaseModel, EmailStr

class User(BaseModel):
    user_id: int
    name: str
    username: str
    password: str
    email: EmailStr

class create_User(BaseModel):
    name: str
    username: str
    password: str
    email: EmailStr

class read_User(BaseModel):
    name: str
    username: str
    email: EmailStr

class UserInDB(BaseModel):
    user_id: int
    name: str
    username: str
    hashed_password: str
    email: EmailStr