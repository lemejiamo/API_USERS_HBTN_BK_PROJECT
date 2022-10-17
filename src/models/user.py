from datetime import datetime
from typing import Union

from pydantic import BaseModel, EmailStr


class TokenCreateModel(BaseModel):
    email: Union[EmailStr, None]
    user_id: Union[str, None]
    name: Union[str, None]


class TokenCheckModel(BaseModel):
    login_token: Union[str, None]


class LoginModel(BaseModel):
    email: Union[EmailStr, None]
    password: Union[str, None]


class UserModel(LoginModel):
    cel: Union[str, None]
    date_load: Union[datetime, None]
    date_update: Union[datetime, None]
    email: Union[EmailStr, None]
    name: Union[str, None]
    type: Union[int, None] = 1


class ChangePasswordModel(LoginModel):
    new_password: Union[str, None]
