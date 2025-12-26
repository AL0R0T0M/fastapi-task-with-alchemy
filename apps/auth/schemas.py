from pydantic import BaseModel, EmailStr

class register_user(BaseModel):
    name: str
    username: str
    password: str
    email: EmailStr

class login_user(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    type_token: str = 'bearer'