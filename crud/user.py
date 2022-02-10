from fastapi import Depends
from sqlalchemy.orm import Session
import models, schemas, database
from passlib.hash import bcrypt
from datetime import datetime, timedelta
from jose import JWTError, jwt
from core.config import SECRET_KEY, ALGORITHM


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


# AUTHENTICATION AND TOKENS
def authenticate_user_login(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not user.verify_password(password):
        return False
    return user


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    return token_data


# User READ utility functions
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


# User DELETE utility functions
def destroy_user(db: Session, user_id: int):
    (
        db.query(models.User)
        .filter(models.User.id == user_id)
        .delete(synchronize_session=False)
    )
    db.commit()

    return {"message": "Successfully Deleted"}
