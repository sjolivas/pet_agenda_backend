from sqlalchemy.orm import Session
import models, schemas
from passlib.hash import bcrypt
from datetime import datetime


# ======================================================================================
# CREATE
# ======================================================================================

# User Create Utility Function
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


# Diet Create Utiliyy Function
def create_pet_diet(db: Session, diet: schemas.DietCreate, pet_id: int):
    db_diet = models.Diet(**diet.dict(), owner_id=pet_id)
    db.add(db_diet)
    db.commit()
    db.refresh(db_diet)
    return db_diet


# MedicalInfo Create Utiliyy Function
def create_pet_medinfo(
    db: Session, medical_info: schemas.MedicalInfoCreate, pet_id: int
):
    db_medical_info = models.MedicalInfo(**medical_info.dict(), owner_id=pet_id)
    db.add(db_medical_info)
    db.commit()
    db.refresh(db_medical_info)
    return db_medical_info


# Note Create Utiliyy Function
def create_note(db: Session, note: schemas.NoteCreate, user_id: int):
    db_note = models.Note(**note.dict(), owner_id=user_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


# ======================================================================================
# READ
# ======================================================================================

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


def get_pet(db: Session, pet_id: int, user_id: int):
    return (
        db.query(models.Pet)
        .filter(models.Pet.owner_id == user_id)
        .filter(models.Pet.id == pet_id)
        .first()
    )


# Diet READ utility functions
def get_diets(db: Session, pet_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Diet)
        .filter(models.Diet.owner_id == pet_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_diet(db: Session, diet_id: int, user_id: int):
    return (
        db.query(models.Diet)
        .filter(models.Diet.owner_id == user_id)
        .filter(models.Diet.id == diet_id)
        .first()
    )


# MedicalInfo READ utility functions
def get_all_medinfo(db: Session, pet_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.MedicalInfo)
        .filter(models.MedicalInfo.owner_id == pet_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_medicalinfo(db: Session, medicalinfo_id: int, user_id: int):
    return (
        db.query(models.MedicalInfo)
        .filter(models.MedicalInfo.id == medicalinfo_id)
        .filter(models.MedicalInfo.owner_id == user_id)
        .first()
    )


# Note READ utility functions
def get_all_notes(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Note)
        .filter(models.Note.owner_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_note(db: Session, note_id: int, user_id: int):
    return (
        db.query(models.Note)
        .filter(models.Note.owner_id == user_id)
        .filter(models.Note.id == note_id)
        .first()
    )


# ======================================================================================
# DELETE
# ======================================================================================

# User DELETE utility functions
def delete_user(db: Session, user_id: int):
    (
        db.query(models.User)
        .filter(models.User.id == user_id)
        .delete(synchronize_session=False)
    )
    db.commit()

    return {"message" ": Successfully Deleted"}


# Pet DELETE utility functions
def delete_pet(db: Session, pet_id: int):
    (
        db.query(models.Pet)
        .filter(models.Pet.id == pet_id)
        .delete(synchronize_session=False)
    )
    db.commit()

    return "Successfully Deleted"


# Diet DELETE utility functions
def delete_pet(db: Session, pet_id: int):
    (
        db.query(models.Pet)
        .filter(models.Pet.id == pet_id)
        .delete(synchronize_session=False)
    )
    db.commit()

    return "Successfully Deleted"


# Medical Info DELETE utility functions
def delete_pet(db: Session, pet_id: int):
    (
        db.query(models.Pet)
        .filter(models.Pet.id == pet_id)
        .delete(synchronize_session=False)
    )
    db.commit()

    return "Successfully Deleted"


# Note DELETE utility functions
def delete_pet(db: Session, pet_id: int):
    (
        db.query(models.Pet)
        .filter(models.Pet.id == pet_id)
        .delete(synchronize_session=False)
    )
    db.commit()

    return "Successfully Deleted"
