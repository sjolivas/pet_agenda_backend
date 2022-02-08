from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
import crud
import database
import schemas


router = APIRouter()

# Create
@router.post(
    "/users/", status_code=status.HTTP_201_CREATED, response_model=schemas.User
)
def create_user(
    user: schemas.UserCreate, db: database.SessionLocal = Depends(database.get_db)
):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=409, detail="Email already registered")
    return crud.create_user(db=db, user=user)


# Read
@router.get(
    "/users/", status_code=status.HTTP_200_OK, response_model=List[schemas.User]
)
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: database.SessionLocal = Depends(database.get_db),
):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get(
    "/users/{user_id}", status_code=status.HTTP_200_OK, response_model=schemas.User
)
def read_user(user_id: int, db: database.SessionLocal = Depends(database.get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# Delete
@router.delete("/user/{user_id}", status_code=200)
def delete_user(user_id: int, db: database.SessionLocal = Depends(database.get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.delete_user(db, user_id)
