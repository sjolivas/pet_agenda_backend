from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

# from fastapi.security import OAuth2PasswordRequestForm
from crud.user import (
    get_user,
    get_users,
    get_user_by_email,
    destroy_user,
    create_new_user,
    # create_access_token,
    # authenticate_user_login,
)
import schemas, database, oauth2


router = APIRouter(tags=["Users"])

# Create - post operation
# @router.post("/token")
# def generate_token(
#     form_data: OAuth2PasswordRequestForm = Depends(),
#     db: database.SessionLocal = Depends(database.get_db),
# ):
#     user = authenticate_user_login(db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
#         )
#     access_token = create_access_token(data={"sub": user.email})
#     return {"access_token": access_token, "token_type": "bearer"}


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(
    user: schemas.UserCreate, db: database.SessionLocal = Depends(database.get_db)
):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=409, detail="Email already registered")
    return create_new_user(db=db, user=user)


# Read - get operations
# @router.get("/users/me")
# def get_me(user: schemas.User = Depends(oauth2.get_current_user)):
#     return user


@router.get("/users", status_code=status.HTTP_200_OK, response_model=List[schemas.User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: database.SessionLocal = Depends(database.get_db),
    # get_current_user: schemas.User = Depends(oauth2.get_current_user),
):
    users = get_users(db, skip=skip, limit=limit)
    return users


@router.get(
    "/users/{user_id}", status_code=status.HTTP_200_OK, response_model=schemas.User
)
def read_user(
    user_id: int,
    db: database.SessionLocal = Depends(database.get_db),
    # get_current_user: schemas.User = Depends(oauth2.get_current_user),
):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# Update - put and patch operation
@router.put(
    "/users/{user_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.User,
)
def update_all_user_info(
    user_id: int,
    user: schemas.User,
    db: database.SessionLocal = Depends(database.get_db),
    # get_current_user: schemas.User = Depends(oauth2.get_current_user),
):
    db_user = get_user(
        db,
        user_id=user_id,
    )
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.first_name = user.first_name
    db_user.last_name = user.last_name
    db_user.email = user.email

    db.commit()
    db.refresh(db_user)

    return schemas.User.from_orm(db_user)


# Patch - patch operation
@router.patch(
    "/users/{user_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.User,
)
def patch_user_info(
    user_id: int,
    user: schemas.UserUpdate,
    db: database.SessionLocal = Depends(database.get_db),
    # get_current_user: schemas.User = Depends(oauth2.get_current_user),
):
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Delete - delete operation
@router.delete("/users/{user_id}", status_code=200)
def delete_user(
    user_id: int,
    db: database.SessionLocal = Depends(database.get_db),
    # get_current_user: schemas.User = Depends(oauth2.get_current_user),
):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return destroy_user(db, user_id)
