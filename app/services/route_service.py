from sqlalchemy.orm import Session

from app.models.waste_bin import WasteBin


def optimize_collection_route(db: Session):

    bins = (
        db.query(WasteBin)
        .filter(WasteBin.fill_level > 0)
        .all()
    )

    # Highest fill level first
    bins = sorted(
        bins,
        key=lambda x: x.fill_level,
        reverse=True
    )

    route = []

    for index, waste_bin in enumerate(bins, start=1):

        if waste_bin.fill_level >= 90:
            priority = "Critical"

        elif waste_bin.fill_level >= 75:
            priority = "High"

        elif waste_bin.fill_level >= 50:
            priority = "Medium"

        else:
            priority = "Low"

        route.append({
            "order": index,
            "bin_id": waste_bin.bin_id,
            "location": waste_bin.bin_location,
            "fill_level": waste_bin.fill_level,
            "priority": priority
        })

    return route