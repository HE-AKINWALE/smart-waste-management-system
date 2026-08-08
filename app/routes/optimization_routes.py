from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.optimization_schema import OptimizedRouteResponse

from app.services.optimization_service import optimize_collection


router = APIRouter(
    prefix="/optimization",
    tags=["Smart Collection Optimization"]
)


@router.get(
    "/",
    response_model=List[OptimizedRouteResponse]
)
def optimized_route(
    db: Session = Depends(get_db)
):
    return optimize_collection(db)