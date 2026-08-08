from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import SessionLocal

from app.schemas.route_schema import RouteResponse
from app.services.route_service import optimize_collection_route

router = APIRouter(
    prefix="/routes",
    tags=["Route Optimization"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get(
    "/optimized",
    response_model=list[RouteResponse]
)
def optimized_route(
    db: Session = Depends(get_db)
):
    return optimize_collection_route(db)