from datetime import datetime
from typing import Union, List

from pydantic import BaseModel, EmailStr


class TokenCreateModel(BaseModel):
    email: EmailStr
    user_id: str
    name: str

class TokenCheckModel(BaseModel):
    login_token: str

class LoginModel(BaseModel):
    email: EmailStr
    password: str

class UserModel(LoginModel):
    cel: Union[str, None]
    date_load: Union[datetime, None]
    date_update: Union[datetime, None]
    name: Union[str, None]
    type: Union[int, None] = 1

class ChangePasswordModel(LoginModel):
    new_password: str