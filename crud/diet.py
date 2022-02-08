from sqlalchemy.orm import Session
import models, schemas
from datetime import datetime

# Diet Create Utility Function
def create_pet_diet(db: Session, diet: schemas.DietCreate, pet_id: int):
    db_diet = models.Diet(**diet.dict(), owner_id=pet_id)
    db.add(db_diet)
    db.commit()
    db.refresh(db_diet)
    return db_diet


# Diet READ utility functions
def get_diet(db: Session, diet_id: int, pet_id: int):
    return (
        db.query(models.Diet)
        .filter(models.Diet.owner_id == pet_id)
        .filter(models.Diet.id == diet_id)
        .first()
    )


# diet Update Utility function
def update_diet():
    pass


# Diet DELETE utility functions
def delete_diet(db: Session, diet_id: int, pet_id: int):
    (
        db.query(models.Diet)
        .filter(models.Diet.owner_id == pet_id)
        .filter(models.Diet.id == diet_id)
        .delete(synchronize_session=False)
    )
    db.commit()

    return "Successfully Deleted"
