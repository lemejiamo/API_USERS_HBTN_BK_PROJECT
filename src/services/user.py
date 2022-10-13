from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from settings import Settings
from models.user import LoginModel, UserModel, TokenCreateModel
from clients.user import get_by_email_client, create_object_client, update_password_client
from utils.token import write_token, validate_token
from datetime import datetime

settings = Settings()

collections = '/Users/'

def login_service(data: LoginModel):
    email = data.email
    check_user = get_by_email_client(email)
    if check_user.status_code == status.HTTP_200_OK:
        json_data = check_user.json()
        user_id = list(json_data.keys())[0]
        check_password = json_data[user_id]['password']
        if check_password == data.password:
            user_email = json_data[user_id]['email']
            user_name = json_data[user_id]['name']
            data_encode = {"user_id": user_id,"email": user_email, "name": user_name}
            token = write_token(data_encode)
            token_dict = {"token": token}
            last_dict = {**data_encode, **token_dict}
            return last_dict
        else:
            return "Wrong password"
    else:
        return "User not found"

def register_service(data: UserModel):
    email = data.email
    data.date_load = datetime.now()
    data.date_update = data.date_load
    check_user = get_by_email_client(email)
    if check_user.status_code == status.HTTP_404_NOT_FOUND:
        json_data = jsonable_encoder(data)
        response = create_object_client(json_data)
        user_id = list(response.keys())[0]
        user_email = response[user_id]['email']
        user_name = response[user_id]['name']
        data_encode = {"user_id": user_id,"email": user_email, "name": user_name}
        token = write_token(data_encode)
        token_dict = {"token": token}
        last_dict = {**data_encode, **token_dict}
        return last_dict
    else:
        return "User already exists"

def update_password_service(data: UserModel):
    email = data.email
    check_user = get_by_email_client(email)
    if check_user.status_code == status.HTTP_200_OK:
        json_data = jsonable_encoder(data)
        user_id = list(check_user.json().keys())[0]
        response = update_password_client(json_data, user_id)
        return response
    else:
        return "User not found"

def create_token_service(token_object: TokenCreateModel):
    json_data = jsonable_encoder(token_object)
    data_encode = {"user_id": token_object.user_id,"email": token_object.email, "name": token_object.name}
    token = write_token(data_encode)
    token_dict = {"token": token}
    last_dict = {**data_encode, **token_dict}
    return last_dict

def validate_token_service(token: str):
    check = validate_token(token, output=True)
    return check
