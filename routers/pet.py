from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from crud.user import get_user
from crud.pet import get_pet, create_user_pet, get_pets, delete_pet
import database
import schemas


router = APIRouter(prefix="/users", tags=["pets"])

# Create
@router.post(
    "/{user_id}/pets/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Pet,
)
def create_pet_for_user(
    user_id: int,
    pet: schemas.PetCreate,
    db: database.SessionLocal = Depends(database.get_db),
):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return create_user_pet(db=db, pet=pet, user_id=user_id)


# Read
@router.get(
    "/{user_id}/pets/",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.Pet],
)
def read_pets(
    user_id: int,
    skip: int = 0,
    limit: int = 10,
    db: database.SessionLocal = Depends(database.get_db),
):
    pets = get_pets(db, user_id, skip=skip, limit=limit)
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return pets


@router.get(
    "/{user_id}/pets/{pet_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.Pet,
)
def read_pet(
    pet_id: int, user_id: int, db: database.SessionLocal = Depends(database.get_db)
):
    db_user = get_user(db, user_id=user_id)
    pet = get_pet(db, pet_id=pet_id, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet


# Delete
@router.delete("/{user_id}/pets/{pet_id}", status_code=200)
def delete_pet(
    pet_id: int, user_id: int, db: database.SessionLocal = Depends(database.get_db)
):
    db_user = get_user(db, user_id=user_id)
    pet = get_pet(db, pet_id=pet_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")
    return delete_pet(db, pet_id, user_id)
