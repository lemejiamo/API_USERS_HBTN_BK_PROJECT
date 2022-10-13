import logging
from fastapi import APIRouter, status, Body
from fastapi.responses import JSONResponse
from models.user import LoginModel, UserModel, TokenCreateModel, ChangePasswordModel
from services.user import (
    login_service,
    register_service,
    update_password_service,
    create_token_service,
    validate_token_service
)
from settings import Settings

settings = Settings()

router = APIRouter(
    prefix="/login",
    tags=["Login"],
)

@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Login to the App",
)
def login_controller(data: LoginModel):
    """
    get all users records from database
    Args:
        user_id (str): user's user id
    Returns:
        JSON Response
    """
    json_response = login_service(data)
    if type(json_response) is str:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail":json_response}
        )
    else:
        return json_response

@router.post(
    "/register/",
    status_code=status.HTTP_200_OK,
    summary="get a single user record from database",
)
def register_controller(
    data: UserModel,
):
    """
    get a single user record from database
    Args:
        user_id (str): user's user id
    Returns:
        JSON Response
    """
    json_response = register_service(data)
    if type(json_response) is str:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail":json_response}
        )
    else:
        return json_response

@router.patch(
    "/update/password/",
    status_code=status.HTTP_201_CREATED,
    summary="create a single user record in database",
)
def update_password_controller(
    data: ChangePasswordModel,
):
    """
    create a single user record in database
    Args:
        user_id (str): user's user id
    Returns:
        JSON Response
    """
    json_response = update_password_service(data)
    if type(json_response) is str:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail":json_response}
        )
    else:
        return json_response

@router.post(
    "/token/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="update a single user record in database",
)
def create_token_controller(
    token_object: TokenCreateModel,
):
    """
    update a single user record in database
    Args:
        user_id (str): user's user id
    Returns:
        JSON Response
    """
    token = create_token_service(token_object)
    return token

@router.post(
    "/token/validate/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="delete a single user record in database",
)
def validate_token_controller(
    token: str = Body(embed=True),
):
    """
    delete a single user record in database
    Args:
        user_id (str): user's user id
    Returns:
        JSON Response
    """
    check_token = validate_token_service(token)
    return check_token
