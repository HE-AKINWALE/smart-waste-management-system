from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.auth.auth_bearer import verify_token

from app.schemas.password_schema import (
    ChangePasswordRequest,
    ChangePasswordResponse,
)

from app.services.auth_service import (
    change_user_password,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.put(
    "/change-password",
    response_model=ChangePasswordResponse
)
def change_password(
    data: ChangePasswordRequest,
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):

    user_id = token_data.get("user_id")

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token."
        )

    return change_user_password(
        int(user_id),
        data,
        db
    )