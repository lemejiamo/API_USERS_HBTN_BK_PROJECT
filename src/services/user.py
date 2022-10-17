from fastapi import status
from fastapi.encoders import jsonable_encoder

from clients.user import (
    create_object_client,
    get_by_email_client,
    update_password_client,
)
from models.user import LoginModel, UserModel
from settings import Settings
from utils.token import validate_token, write_token

settings = Settings()


def login_service(data: LoginModel):
    response_data = validate_user_by_email_service(data.email)
    if response_data.status_code == status.HTTP_200_OK:
        user_info = response_data.json()
        user_id = list(user_info.keys())[0]
        json_token = create_token_service(user_info, user_id)
        check_password = user_info[user_id]["password"]
        if check_password == data.password:
            return json_token
        else:
            return "Wrong password"
    else:
        return "User not found"


def register_service(data: UserModel):
    response_data = validate_user_by_email_service(data.email)
    if response_data.status_code == status.HTTP_200_OK:
        return "User already exists"
    request_data = jsonable_encoder(data)
    json_token = create_token_service(request_data)
    if json_token["token"]:
        token = json_token["token"]
        create_object_client(request_data, token)
        return json_token


def update_password_service(data: UserModel):
    response_data = validate_user_by_email_service(data.email)
    if response_data.status_code == status.HTTP_200_OK:
        user_info = response_data.json()
        user_id = list(user_info.keys())[0]
        json_token = create_token_service(user_info, user_id)
        request_data = jsonable_encoder(data)
        token = json_token["token"]
        update_password_client(request_data, user_id, token)
        return json_token
    else:
        return "User not found"


def create_token_service(user_info, user_id=None):
    if user_id is not None:
        name = user_info[user_id]["name"]
        email = user_info[user_id]["email"]
        data_encode = {"user_id": user_id, "email": name, "name": email}
    else:
        name = user_info["name"]
        email = user_info["email"]
        data_encode = {"email": name, "name": email}
    token = write_token(data_encode)
    token_dict = {"token": token}
    json_data = {**data_encode, **token_dict}
    return json_data


def validate_token_service(token: str):
    json_data = validate_token(token, output=True)
    return json_data


def validate_user_by_email_service(email):
    check_user = get_by_email_client(email)
    return check_user
