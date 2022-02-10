from sqlalchemy.orm import Session
import models, schemas

# Pet Create utility function
def create_user_pet(db: Session, pet: schemas.PetCreate, user_id: int):
    db_pet = models.Pet(**pet.dict(), owner_id=user_id)
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return db_pet


# Pet READ utility functions
def get_pets(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Pet)
        .filter(models.Pet.owner_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_pet(db: Session, pet_id: int, user_id: int):
    return (
        db.query(models.Pet)
        .filter(models.Pet.owner_id == user_id)
        .filter(models.Pet.id == pet_id)
        .first()
    )


# Pet DELETE utility functions
def delete_user_pet(db: Session, pet_id: int, user_id: int):
    (
        db.query(models.Pet)
        .filter(models.Pet.owner_id == user_id)
        .filter(models.Pet.id == pet_id)
        .delete(synchronize_session=False)
    )
    db.commit()

    return "Successfully Deleted"
