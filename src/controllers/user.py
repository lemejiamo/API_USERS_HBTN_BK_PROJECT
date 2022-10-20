from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from models.user import ChangePasswordModel, LoginModel, TokenCreateModel, UserModel
from services.user import (
    create_token_service,
    login_service,
    register_service,
    update_password_service,
    validate_token_service,
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
    Allows the user to login to the app
    Args:
        data (LoginModel): user's email and password
    Returns:
        JSON Response
    """
    json_response = login_service(data)
    if type(json_response) is str:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": json_response}
        )
    else:
        return json_response


@router.post(
    "/register/",
    status_code=status.HTTP_201_CREATED,
    summary="Register to the App",
)
def register_controller(
    data: UserModel,
):
    """
    Create a new user at DB
    Args:
        data (UserModel): user's info
    Returns:
        JSON Response
    """
    json_response = register_service(data)
    return JSONResponse(
        status_code=json_response.status_code, content=json_response.text
    )

@router.patch(
    "/update/password/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Update user's password",
)
def update_password_controller(
    data: ChangePasswordModel,
):
    """
    Update user's password at DB
    Args:
        user_id (str): user's user id
    Returns:
        JSON Response
    """
    json_response = update_password_service(data)
    if type(json_response) is str:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"detail": json_response}
        )
    else:
        return json_response


@router.post(
    "/token/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Create a valid login token for the app",
)
def create_token_controller(
    token_object: TokenCreateModel,
):
    """
    Create a new token for the user
    Args:
        token_object (TokenCreateModel): user's info required for the token
    Returns:
        JSON Response
    """
    user_id = token_object.user_id
    raw_data = jsonable_encoder(token_object)
    json_data = {}
    json_data[user_id] = raw_data
    token = create_token_service(json_data, user_id)
    return token


@router.get(
    "/token/validate/{token}",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Validate a login token for the app",
)
def validate_token_controller(
    token: str,
):
    """
    Validate a login token for the app
    Args:
        user_id (str): user's user id
    Returns:
        JSON Response
    """
    check_token = validate_token_service(token)
    return check_token
