from fastapi import HTTPException

from app.services.permission_service import (
    get_permissions
)


def require_permission(permission: str):

    def checker(user):

        permissions = get_permissions(user["role"])

        if permission not in permissions:

            raise HTTPException(

                status_code=403,

                detail="Permission denied"

            )

        return user

    return checker