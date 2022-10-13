import email
from typing import List, Union
import requests
from fastapi import HTTPException, status
from settings import Settings

settings = Settings()

def get_by_email_client(email: str):
    request_url = f"{settings.CRUD_API_URL}/user/email/{email}"
    response = requests.get(
        url=request_url
    )

    if response.status_code == status.HTTP_200_OK or response.status_code == status.HTTP_404_NOT_FOUND:
        return response
    else:
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail={
                "client": "get_by_email_client",
                "detail": f"The API can't get a record at DB for user with email {email}",
            },
        )


def create_object_client(json_object):
    request_url = f"{settings.CRUD_API_URL}/user/"
    email = json_object["email"]
    response = requests.post(
        url=request_url, json=json_object
    )

    if response.status_code == status.HTTP_201_CREATED:
        return response.json()
    elif response.status_code == status.HTTP_406_NOT_ACCEPTABLE:
        return {}
    else:
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail={
                "client": "create_object_client",
                "detail": f"The API can't create a record at DB for user with email {email}",
            },
        )


def update_password_client(json_object, user_id: str):
    request_url = f"{settings.CRUD_API_URL}/user/update/password/user/{user_id}"
    email = json_object["email"]
    response = requests.patch(
        url=request_url, json=json_object
    )

    if response.status_code == status.HTTP_200_OK:
        return response.json()
    elif response.status_code == status.HTTP_404_NOT_FOUND:
        return {}
    else:
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail={
                "client": "update_object_client",
                "detail": f"The API can't update a record at DB for user with email {email}",
            },
        )
