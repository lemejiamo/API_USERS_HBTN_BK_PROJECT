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
        response_data = check_user.json()
        user_id = list(response_data.keys())[0]
        check_password = response_data[user_id]['password']
        if check_password == data.password:
            user_email = response_data[user_id]['email']
            user_name = response_data[user_id]['name']
            data_encode = {"user_id": user_id,"email": user_email, "name": user_name}
            token = write_token(data_encode)
            token_dict = {"token": token}
            json_data = {**data_encode, **token_dict}
            return json_data
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
        request_data = jsonable_encoder(data)
        response_data = create_object_client(request_data)
        user_id = list(response_data.keys())[0]
        user_email = response_data[user_id]['email']
        user_name = response_data[user_id]['name']
        data_encode = {"user_id": user_id,"email": user_email, "name": user_name}
        token = write_token(data_encode)
        token_dict = {"token": token}
        json_data = {**data_encode, **token_dict}
        return json_data
    else:
        return "User already exists"

def update_password_service(data: UserModel):
    email = data.email
    check_user = get_by_email_client(email)
    if check_user.status_code == status.HTTP_200_OK:
        response_data = check_user.json()
        request_data = jsonable_encoder(data)
        user_id = list(response_data.keys())[0]
        json_data = update_password_client(request_data, user_id)
        return json_data
    else:
        return "User not found"

def create_token_service(token_object: TokenCreateModel):
    email = token_object.email
    check_user = get_by_email_client(email)
    if check_user.status_code == status.HTTP_200_OK:
        data_encode = {"user_id": token_object.user_id,"email": token_object.email, "name": token_object.name}
        token = write_token(data_encode)
        token_dict = {"token": token}
        json_data = {**data_encode, **token_dict}
        return json_data

def validate_token_service(token: str):
    json_data = validate_token(token, output=True)
    return json_data
