from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.models.user import User

from app.schemas.user_schema import (
    UserCreate,
    UserResponse,
    UserLogin,
    UserProfileUpdate
)

from app.schemas.password_schema import (
    ChangePasswordRequest
)

from app.services.auth_service import (
    register_user,
    login_user,
    update_user_profile,
    change_user_password
)

from app.auth.dependencies import get_current_user


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    new_user = register_user(
        user,
        db
    )

    if new_user is None:

        raise HTTPException(
            status_code=400,
            detail="Email already exists."
        )

    return new_user


@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    result = login_user(
        user.email,
        user.password,
        db
    )

    if result is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    return result


    result = login_user(
        form_data.username,
        form_data.password,
        db
    )

    if result is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    return {
        "access_token": result["access_token"],
        "token_type": "bearer"
    }


@router.put(
    "/profile",
    response_model=UserResponse
)
def update_profile(
    data: UserProfileUpdate,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    return update_user_profile(
        current_user.user_id,
        data,
        db
    )


@router.put(
    "/change-password"
)
def change_password(
    data: ChangePasswordRequest,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    return change_user_password(
        current_user.user_id,
        data,
        db
    )