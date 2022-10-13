import logging
from datetime import datetime

from enums.bootcamp import OperationType
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from repositories.bootcamp.hunty import update_hunty
from schemas.bootcamp.session import SessionSchema
from settings import Settings

from . import db, db_app

settings = Settings


def create_product_repository(hunty_id: str, session: SessionSchema):
    """
    CRUD method to create a bootcamp session
    """
    try:
        ref = db.reference(f"/{hunty_id}/sessions", db_app)
        created_session = ref.push(jsonable_encoder(session))
        session = session.dict()
        session.update({"session_id": created_session.key})

        ref = db.reference(
            f"/{hunty_id}/historical_events/sessions/{created_session.key}", db_app
        )

        hist_sessions = ref.get() if ref.get() else []

        hist_sessions.append(
            {
                "mentor_id": session.get("mentor_id"),
                "stage_id": session.get("stage_id"),
                "session_date": session.get("session_date"),
                "duration_id": session.get("duration_id"),
                "operation_type": OperationType.create.value,
                "operation_date": datetime.utcnow(),
            }
        )

        ref.set(jsonable_encoder(hist_sessions))

        update_hunty(
            hunty_id=hunty_id, hunty={"update_date": datetime.utcnow()}, database="BE"
        )

        return session

    except Exception as ex:
        logging.error(f"create_bootcamp_session: {ex}")
        return JSONResponse(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            content=ex,
        )


def delete_product_repository(hunty_id: str, mentor_id: str, session_id: str):
    """
    CRUD method to create a bootcamp session
    """
    try:
        ref = db.reference(f"/{hunty_id}/sessions/{session_id}", db_app)

        deleted_session = ref.get()
        if not deleted_session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Session {session_id} not found",
            )

        ref.delete()

        ref = db.reference(
            f"/{hunty_id}/historical_events/sessions/{session_id}", db_app
        )

        hist_tracking_sessions = ref.get() if ref.get() else []

        hist_tracking_sessions.append(
            {
                "mentor_id": mentor_id,
                "stage_id": deleted_session.get("stage_id"),
                "session_date": deleted_session.get("session_date"),
                "duration_id": deleted_session.get("duration_id"),
                "operation_type": OperationType.delete.value,
                "operation_date": datetime.utcnow(),
            }
        )

        ref.set(jsonable_encoder(hist_tracking_sessions))

        update_hunty(
            hunty_id=hunty_id, hunty={"update_date": datetime.utcnow()}, database="BE"
        )

        return deleted_session

    except HTTPException as ex:
        logging.error(f"delete_bootcamp_session: {ex}")
        raise HTTPException(status_code=ex.status_code, detail=ex.detail)
    except Exception as ex:
        logging.error(f"delete_bootcamp_session: {ex}")
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="repository: delete_bootcamp_session",
        )
