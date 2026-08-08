from fastapi import APIRouter, Depends

from app.auth.auth_bearer import verify_token

from app.auth.permissions import require_permission

router = APIRouter(

    prefix="/permissions",

    tags=["Role Permissions"]

)


@router.get("/admin")

def admin_area(

    user=Depends(verify_token)

):

    require_permission("system_config")(user)

    return {

        "message": "Administrator access granted.",

        "user": user

    }


@router.get("/reports")

def reports_area(

    user=Depends(verify_token)

):

    require_permission("view_reports")(user)

    return {

        "message": "Report access granted.",

        "user": user

    }


@router.get("/dashboard")

def dashboard_area(

    user=Depends(verify_token)

):

    require_permission("view_dashboard")(user)

    return {

        "message": "Dashboard access granted.",

        "user": user

    }