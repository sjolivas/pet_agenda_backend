from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from crud.user import (
    get_user,
    get_users,
    get_user_by_email,
    delete_user,
    create_new_user,
)
import database
import schemas


router = APIRouter(prefix="/users", tags=["users"])

# Create - post operation
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(
    user: schemas.UserCreate, db: database.SessionLocal = Depends(database.get_db)
):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=409, detail="Email already registered")
    return create_new_user(db=db, user=user)


# Read - get operations
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: database.SessionLocal = Depends(database.get_db),
):
    users = get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=schemas.User)
def read_user(user_id: int, db: database.SessionLocal = Depends(database.get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# Update - patch operation
@router.patch(
    "/{user_id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.User
)
def patch_user_info():
    pass


# Delete - delete operation
@router.delete("/{user_id}", status_code=200)
def delete_user(user_id: int, db: database.SessionLocal = Depends(database.get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return delete_user(db, user_id)
