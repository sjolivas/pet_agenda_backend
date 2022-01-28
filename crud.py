from sqlalchemy.orm import Session
import models, schemas

# User READ utility functions
def get_user(db:Session, user_id:int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# User Create utility function
# look up security for the password hashing
def create_user(db: Session, user: schemas.UserCreate):
    # fake_hashed_password = user.password + "not really hashed"
    db_user = models.User(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Pet READ utility functions
def get_pets(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Pet).filter(models.Pet.owner_id == user_id).offset(skip).limit(limit).all()

# Pet Create utility function
def create_user_pet(db: Session, pet: schemas.PetCreate, user_id: int):
    db_pet = models.Pet(**pet.dict(), owner_id=user_id)
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return db_pet
