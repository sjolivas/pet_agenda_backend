from http.client import HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
import os

import models, schemas
from passlib.hash import bcrypt
# from jwt import encode, decode

# from fastapi.security import sec

# oauth2schema = OAuth2PasswordBearer(tokenUrl="/api/token")

# User Create utility function
# look up security for the password hashing
def create_user(db: Session, user: schemas.UserCreate):
    # fake_hashed_password = user.password + "not really hashed"
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


# def authenticate_user(email: str, password: str, db: Session):
#     user = get_user_by_email(db=db, email=email)
#     if not user or not user.verify_password(password):
#         return False

#     return user


# def create_token(user: models.User):
#     user_obj = {"email": schemas.User.from_orm(user).dict()["email"]}
#     token = encode(user_obj, JWT_SECRET)
#     return {"access_token": token, "token_type": "bearer"}


# def get_current_user(db: Session = Depends(Session), token: str = Depends(oauth2schema)):
#     try:
#         payload = decode(token, JWT_SECRET, algorithms=["HS256"])
#         user = db.query(models.User).get(payload["id"])
#     except:
#         raise HTTPException(status_code=401, detail="Invalid Email or Password")

#     return schemas.User.from_orm(user)


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
# Pet UPDATE utility functions
# User DELETE utility functions
# Pet DELETE utility functions
