from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User

from app.schemas.user_schema import (
    UserCreate,
    UserProfileUpdate
)

from app.schemas.password_schema import (
    ChangePasswordRequest
)

from app.auth.password import (
    hash_password,
    verify_password
)

from app.auth.jwt_handler import (
    create_access_token
)


def register_user(
    user: UserCreate,
    db: Session
):

    existing_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if existing_user:
        return None

    new_user = User(
        full_name=user.full_name,
        email=user.email,
        password=hash_password(user.password),
        role=user.role
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return new_user


def login_user(
    email: str,
    password: str,
    db: Session
):

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if not user:
        return None

    if not verify_password(
        password,
        user.password
    ):
        return None

    token = create_access_token(
        {
            "sub": str(user.user_id),
            "role": user.role
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "user_id": user.user_id,
            "full_name": user.full_name,
            "email": user.email,
            "role": user.role
        }
    }


def change_user_password(
    user_id: int,
    data: ChangePasswordRequest,
    db: Session
):

    user = (
        db.query(User)
        .filter(User.user_id == user_id)
        .first()
    )

    if user is None:

        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    if not verify_password(
        data.current_password,
        user.password
    ):

        raise HTTPException(
            status_code=400,
            detail="Current password is incorrect."
        )

    if data.new_password != data.confirm_password:

        raise HTTPException(
            status_code=400,
            detail="New passwords do not match."
        )

    if verify_password(
        data.new_password,
        user.password
    ):

        raise HTTPException(
            status_code=400,
            detail=(
                "New password must be different "
                "from the current password."
            )
        )

    user.password = hash_password(
        data.new_password
    )

    db.commit()

    db.refresh(user)

    return {
        "message": "Password changed successfully."
    }


def update_user_profile(
    user_id: int,
    data: UserProfileUpdate,
    db: Session
):

    user = (
        db.query(User)
        .filter(User.user_id == user_id)
        .first()
    )

    if user is None:

        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    existing_user = (
        db.query(User)
        .filter(
            User.email == data.email,
            User.user_id != user_id
        )
        .first()
    )

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="This email address is already in use."
        )

    user.full_name = data.full_name
    user.email = data.email

    db.commit()

    db.refresh(user)

    return user

def update_user_profile(
    user_id: int,
    data: UserProfileUpdate,
    db: Session
):
    user = (
        db.query(User)
        .filter(User.user_id == user_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    existing_email = (
        db.query(User)
        .filter(
            User.email == data.email,
            User.user_id != user_id
        )
        .first()
    )

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email address is already in use."
        )

    user.full_name = data.full_name.strip()
    user.email = data.email

    db.commit()
    db.refresh(user)

    return user