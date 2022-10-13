import logging
from datetime import datetime
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from settings import Settings
from models.user import UserModel
from . import db, db_app

settings = Settings()

def get_all_users_repository(collection: str):
    """
    CRUD method for get all users
    """
    try:
        ref = db.reference(f"{collection}", db_app)
        json_to_return = ref.get()
        if json_to_return is None:
            return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "Users not found"},
            )
        return json_to_return

    except HTTPException as ex:
        logging.error(f"At get_all_users_repository: {ex.detail}")
        return JSONResponse(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            content={"error": f"failed to get all users", "message": f"{ex.detail}"},
        )

def get_user_by_id_repository(collection: str, user_id: str):
    """
    CRUD method for get a user by id
    """
    try:
        ref = db.reference(f"{collection}/{user_id}", db_app)
        json_to_return = ref.get()
        if json_to_return is None:
            return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "User with id {user_id} not found"},
            )
        return json_to_return

    except HTTPException as ex:
        logging.error(f"At get_user_by_id_repository: {ex.detail}")
        return JSONResponse(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            content={"error": f"failed to get a user with id {user_id}", "message": f"{ex.detail}"},
        )

def get_user_by_email_repository(collection: str, email: str):
    """
    CRUD method for get a user by id
    """
    try:
        ref = db.reference(f"{collection}", db_app)
        all_results = dict(ref.order_by_child('Users_email').equal_to(email).get())
        if all_results is None or all_results == {}:
            return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "User with email {email} not found"},
            )
        json_user = {list(all_results.keys())[0] : all_results[list(all_results.keys())[0]]}
        return json_user

    except HTTPException as ex:
        logging.error(f"At get_user_by_id_repository: {ex}")
        return JSONResponse(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            content={"error": f"failed to get a user with id {email}", "message": f"{ex.detail}"}
        )


def create_user_repository(collection: str, user: UserModel, id: str):
    """
    CRUD method for create a user
    """
    try:
        check_not_exist = get_user_by_email_repository(collection, user.Users_email)
        if type(check_not_exist) == JSONResponse:
            ref = db.reference(f"{collection}/{id}/", db_app)
            user.Users_date_load = datetime.now()
            user.Users_date_update = user.Users_date_load
            user_created = jsonable_encoder(user)
            ref.set(user_created)
            return user_created
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with email {user.Users_email} already exists",
            )

    except HTTPException as ex:
        logging.error(f"At create_user_repository: {ex}")
        return JSONResponse(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            content={"error": f"failed to create a user", "message": f"{ex.detail}"}
        )


# def delete_user_repository(hunty_id: str, mentor_id: str, session_id: str):
#     """
#     CRUD method to create a bootcamp session
#     """
#     try:
#         ref = db.reference(f"/{hunty_id}/sessions/{session_id}", db_app)
#
#         deleted_session = ref.get()
#         if not deleted_session:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail=f"Session {session_id} not found",
#             )
#
#         ref.delete()
#
#         ref = db.reference(
#             f"/{hunty_id}/historical_events/sessions/{session_id}", db_app
#         )
#
#         hist_tracking_sessions = ref.get() if ref.get() else []
#
#         hist_tracking_sessions.append(
#             {
#                 "mentor_id": mentor_id,
#                 "stage_id": deleted_session.get("stage_id"),
#                 "session_date": deleted_session.get("session_date"),
#                 "duration_id": deleted_session.get("duration_id"),
#                 "operation_type": OperationType.delete.value,
#                 "operation_date": datetime.utcnow(),
#             }
#         )
#
#         ref.set(jsonable_encoder(hist_tracking_sessions))
#
#         update_hunty(
#             hunty_id=hunty_id, hunty={"update_date": datetime.utcnow()}, database="BE"
#         )
#
#         return deleted_session
#
#     except HTTPException as ex:
#         logging.error(f"delete_bootcamp_session: {ex}")
#         raise HTTPException(status_code=ex.status_code, detail=ex.detail)
#     except Exception as ex:
#         logging.error(f"delete_bootcamp_session: {ex}")
#         raise HTTPException(
#             status_code=status.HTTP_424_FAILED_DEPENDENCY,
#             detail="repository: delete_bootcamp_session",
#         )
