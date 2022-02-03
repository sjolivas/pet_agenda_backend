from sqlalchemy.orm import Session
import models, schemas
from passlib.hash import bcrypt

def create_user(db: Session, user: schemas.UserCreate):

    db_user = models.User(
        email=user.email,
        hashed_password=bcrypt.hash(user.hashed_password),
        first_name=user.first_name,
        last_name=user.last_name,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Pet Create utility function
def create_user_pet(db: Session, pet: schemas.PetCreate, user_id: int):
    db_pet = models.Pet(**pet.dict(), owner_id=user_id)
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return db_pet


# User READ utility functions
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


# Pet READ utility functions
def get_pets(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Pet)
        .filter(models.Pet.owner_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_pet(db: Session, pet_id: int):
    return db.query(models.Pet).filter(models.Pet.id == pet_id).first()


# User UPDATE utility functions
def update_user():
    pass

def patch_user():
    pass

# Pet UPDATE utility functions
def update_pet():
    pass

def patch_pet():
    pass


# User DELETE utility functions
def delete_user(db: Session, user_id: int):
    (db.query(models.User).filter(models.User.id == user_id).delete(synchronize_session=False))
    db.commit()

    return "Successfully Deleted"

# Pet DELETE utility functions
def delete_pet(db: Session, pet_id: int):
    (db.query(models.Pet).filter(models.Pet.id == pet_id).delete(synchronize_session=False))
    db.commit()

    return "Successfully Deleted"

