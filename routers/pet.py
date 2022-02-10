from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from crud.user import get_user
from crud.pet import get_pet, create_user_pet, get_pets, delete_user_pet
import database, schemas, oauth2


router = APIRouter(prefix="/users", tags=["Pets"])

# Create - post operation
@router.post(
    "/{user_id}/pets/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Pet,
)
def create_pet_for_user(
    user_id: int,
    pet: schemas.PetCreate,
    db: database.SessionLocal = Depends(database.get_db),
    get_current_user: schemas.User = Depends(oauth2.get_current_user),
):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return create_user_pet(db=db, pet=pet, user_id=user_id)


# Read - get operation
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
    get_current_user: schemas.User = Depends(oauth2.get_current_user),
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
    pet_id: int,
    user_id: int,
    db: database.SessionLocal = Depends(database.get_db),
    get_current_user: schemas.User = Depends(oauth2.get_current_user),
):
    db_user = get_user(db, user_id=user_id)
    pet = get_pet(db, pet_id=pet_id, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet


# Update - patch operation
@router.patch(
    "/{user_id}/pets/{pet_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.Pet,
)
def patch_pet_info(
    pet_id: int,
    user_id: int,
    pet: schemas.PetUpdate,
    db: database.SessionLocal = Depends(database.get_db),
    get_current_user: schemas.User = Depends(oauth2.get_current_user),
):
    db_user = get_user(db, user_id)
    db_pet = get_pet(db, pet_id=pet_id, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if db_pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")
    pet_data = pet.dict(exclude_unset=True)
    for key, value in pet_data.items():
        setattr(db_pet, key, value)
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return db_pet


# Delete - delete operation
@router.delete("/{user_id}/pets/{pet_id}", status_code=200)
def delete_pet(
    pet_id: int,
    user_id: int,
    db: database.SessionLocal = Depends(database.get_db),
    get_current_user: schemas.User = Depends(oauth2.get_current_user),
):
    db_user = get_user(db, user_id=user_id)
    pet = get_pet(db, pet_id=pet_id, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")
    return delete_user_pet(db, pet_id, user_id)
