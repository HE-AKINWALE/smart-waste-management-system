from sqlalchemy.orm import Session
from app.models.waste_bin import WasteBin
from app.schemas.waste_bin_schema import WasteBinCreate, WasteBinUpdate


def create_bin(bin_data: WasteBinCreate, db: Session):

    waste_bin = WasteBin(
        bin_location=bin_data.bin_location,
        capacity=bin_data.capacity,
        fill_level=bin_data.fill_level,
        bin_status=calculate_status(bin_data.fill_level)
    )

    db.add(waste_bin)
    db.commit()
    db.refresh(waste_bin)

    return waste_bin


def get_all_bins(db: Session):
    return db.query(WasteBin).all()


def get_bin(bin_id: int, db: Session):
    return db.query(WasteBin).filter(
        WasteBin.bin_id == bin_id
    ).first()

def calculate_status(fill_level):

    if fill_level == 0:
        return "Empty"

    elif fill_level <= 49:
        return "Low"

    elif fill_level <= 79:
        return "Medium"

    elif fill_level <= 99:
        return "High"

    else:
        return "Full"
    
def update_bin(bin_id: int, bin_data: WasteBinUpdate, db: Session):

    waste_bin = db.query(WasteBin).filter(
        WasteBin.bin_id == bin_id
    ).first()

    if waste_bin is None:
        return None

    waste_bin.bin_location = bin_data.bin_location
    waste_bin.capacity = bin_data.capacity
    waste_bin.fill_level = bin_data.fill_level
    waste_bin.bin_status = calculate_status(
        bin_data.fill_level
    )

    db.commit()
    db.refresh(waste_bin)

    return waste_bin    

def delete_bin(bin_id: int, db: Session):

    waste_bin = db.query(WasteBin).filter(
        WasteBin.bin_id == bin_id
    ).first()

    if waste_bin is None:
        return False

    db.delete(waste_bin)
    db.commit()

    return True