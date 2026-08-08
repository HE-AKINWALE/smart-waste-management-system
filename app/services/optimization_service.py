from sqlalchemy.orm import Session

from app.models.waste_bin import WasteBin


def optimize_collection(db: Session):

    bins = db.query(WasteBin).all()

    scored_bins = []

    for waste_bin in bins:

        # -------------------------------------------------
        # Normalize bin data
        # -------------------------------------------------

        fill_level = max(
            0,
            min(
                waste_bin.fill_level or 0,
                100
            )
        )

        capacity = max(
            waste_bin.capacity or 0,
            0
        )

        bin_status = (
            waste_bin.bin_status or "Unknown"
        ).strip().lower()


        # -------------------------------------------------
        # Estimate current waste quantity
        # -------------------------------------------------

        estimated_waste = (
            capacity * fill_level / 100
        )


        # -------------------------------------------------
        # Determine collection priority
        # -------------------------------------------------

        if fill_level >= 90:

            priority = "Critical"
            priority_score = 4
            recommended_action = (
                "Collect immediately"
            )

        elif fill_level >= 75:

            priority = "High"
            priority_score = 3
            recommended_action = (
                "Collect today"
            )

        elif fill_level >= 50:

            priority = "Medium"
            priority_score = 2
            recommended_action = (
                "Monitor and schedule collection"
            )

        else:

            priority = "Low"
            priority_score = 1
            recommended_action = (
                "Continue monitoring"
            )


        # -------------------------------------------------
        # Determine operational status
        # -------------------------------------------------

        inactive_statuses = {
            "inactive",
            "disabled",
            "maintenance",
            "closed",
        }

        is_operational = (
            bin_status not in inactive_statuses
        )


        # -------------------------------------------------
        # Prevent inactive bins from being recommended
        # for collection.
        # -------------------------------------------------

        if not is_operational:

            recommended_action = (
                "Do not collect - bin unavailable"
            )


        # -------------------------------------------------
        # Calculate optimization score
        # -------------------------------------------------

        operational_score = (
            10 if is_operational else -100
        )

        fill_score = (
            fill_level * 0.7
        )

        waste_score = min(
            estimated_waste / 10,
            20
        )

        priority_weight = (
            priority_score * 7.5
        )

        total_score = (
            fill_score
            + waste_score
            + priority_weight
            + operational_score
        )


        scored_bins.append({

            "bin_id":
                waste_bin.bin_id,

            "bin_location":
                waste_bin.bin_location,

            "fill_level":
                fill_level,

            "estimated_waste":
                estimated_waste,

            "priority":
                priority,

            "score":
                total_score,

            "recommended_action":
                recommended_action,

            "is_operational":
                is_operational,

        })


    # -------------------------------------------------
    # Only operational bins are included in the
    # recommended collection route.
    # -------------------------------------------------

    collection_bins = [

        item

        for item in scored_bins

        if item["is_operational"]

    ]


    # -------------------------------------------------
    # Rank bins from highest to lowest priority.
    # -------------------------------------------------

    collection_bins.sort(

        key=lambda item: (

            item["score"],

            item["fill_level"],

            item["estimated_waste"],

        ),

        reverse=True,

    )


    # -------------------------------------------------
    # Generate optimized collection sequence.
    # -------------------------------------------------

    optimized = []


    for index, item in enumerate(

        collection_bins,

        start=1

    ):

        optimized.append({

            "order":
                index,

            "bin_id":
                item["bin_id"],

            "location":
                item["bin_location"],

            "fill_level":
                item["fill_level"],

            "priority":
                item["priority"],

            "estimated_waste":
                round(
                    item["estimated_waste"],
                    2
                ),

            "optimization_score":
                round(
                    item["score"],
                    2
                ),

            "recommended_action":
                item["recommended_action"],

        })


    return optimized