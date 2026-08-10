from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.auth.dependencies import get_current_user

from app.models.user import User

from app.schemas.waste_bin_schema import (
    WasteBinCreate,
    WasteBinResponse,
    WasteBinUpdate,
)

from app.services.waste_bin_service import (
    create_bin,
    get_all_bins,
    get_bin,
    update_bin,
    delete_bin,
)


router = APIRouter(
    prefix="/bins",
    tags=["Waste Bins"],
)


# =========================================================
# CREATE WASTE BIN
# =========================================================

@router.post(
    "/",
    response_model=WasteBinResponse,
)
def add_bin(
    bin_data: WasteBinCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_bin(
        bin_data,
        db,
        current_user.user_id,
    )


# =========================================================
# GET ALL WASTE BINS
# =========================================================

@router.get(
    "/",
    response_model=list[WasteBinResponse],
)
def view_bins(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_all_bins(
        db,
        current_user,
    )


# =========================================================
# GET SINGLE WASTE BIN
# =========================================================

@router.get(
    "/{bin_id}",
    response_model=WasteBinResponse,
)
def view_bin(
    bin_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    waste_bin = get_bin(
        bin_id,
        db,
        current_user,
    )

    if not waste_bin:
        raise HTTPException(
            status_code=404,
            detail="Waste bin not found.",
        )

    return waste_bin


# =========================================================
# UPDATE WASTE BIN
# =========================================================

@router.put(
    "/{bin_id}",
    response_model=WasteBinResponse,
)
def edit_bin(
    bin_id: int,
    bin_data: WasteBinUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    waste_bin = update_bin(
        bin_id,
        bin_data,
        db,
        current_user,
    )

    if waste_bin is None:
        raise HTTPException(
            status_code=404,
            detail="Waste bin not found.",
        )

    return waste_bin


# =========================================================
# DELETE WASTE BIN
# =========================================================

@router.delete(
    "/{bin_id}",
)
def remove_bin(
    bin_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted = delete_bin(
        bin_id,
        db,
        current_user,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Waste bin not found.",
        )

    return {
        "message": "Waste bin deleted successfully.",
    }