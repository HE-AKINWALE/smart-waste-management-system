from datetime import date, timedelta


def calculate_priority(fill_level: int):
    """
    Determine collection priority based on waste bin fill level.
    """

    if fill_level >= 90:
        return "Critical"

    if fill_level >= 75:
        return "High"

    if fill_level >= 50:
        return "Medium"

    return "Low"


def recommend_collection_date(fill_level: int):
    """
    Recommend a collection date based on the waste bin fill level.
    """

    today = date.today()

    if fill_level >= 90:
        return today

    if fill_level >= 75:
        return today + timedelta(days=1)

    if fill_level >= 50:
        return today + timedelta(days=3)

    return today + timedelta(days=7)


def requires_collection(fill_level: int):
    """
    Determine whether a waste bin currently requires
    a collection schedule.
    """

    return fill_level >= 50