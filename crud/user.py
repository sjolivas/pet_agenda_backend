from sqlalchemy.orm import Session
import models, schemas
from passlib.hash import bcrypt
from datetime import datetime

# User Create Utility Function
def create_new_user(db: Session, user: schemas.UserCreate):
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


# User READ utility functions
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


# User Update Utility Function
def update_user():
    pass


# User DELETE utility functions
def delete_user(db: Session, user_id: int):
    (
        db.query(models.User)
        .filter(models.User.id == user_id)
        .delete(synchronize_session=False)
    )
    db.commit()

    return {"message" ": Successfully Deleted"}
