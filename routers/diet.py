from fastapi import APIRouter, Depends, HTTPException, status
from crud.diet import create_pet_diet, get_diet, delete_diet
from crud.pet import get_pet
import database
import schemas


router = APIRouter(prefix="/users", tags=["diet"])

# Create
@router.post(
    "/{user_id}/pet/{pet_id}/diet",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Diet,
)
def create_diet(
    user_id: int,
    pet_id: int,
    diet: schemas.DietCreate,
    db: database.SessionLocal = Depends(database.get_db),
):
    pet = get_pet(db, pet_id=pet_id, user_id=user_id)
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")
    return create_pet_diet(db=db, diet=diet, pet_id=pet_id)


# Read
@router.get(
    "/{user_id}/pet/{pet_id}/diet/{diet_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.Diet,
)
def read_diet(
    pet_id: int,
    diet_id: int,
    user_id: int,
    db: database.SessionLocal = Depends(database.get_db),
):
    pet = get_pet(db, pet_id=pet_id, user_id=user_id)
    diet = get_diet(db, diet_id, pet_id)
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")
    if diet is None:
        raise HTTPException(status_code=404, detail="Diet not found")
    return diet


# Delete
@router.delete(
    "/{user_id}/pet/{pet_id}/diet/{diet_id}",
    status_code=status.HTTP_200_OK,
)
def delete_pet_diet(
    pet_id: int,
    diet_id: int,
    user_id: int,
    db: database.SessionLocal = Depends(database.get_db),
):
    pet = get_pet(db, pet_id=pet_id, user_id=user_id)
    diet = get_diet(db, diet_id, pet_id)
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")
    if diet is None:
        raise HTTPException(status_code=404, detail="Diet not found")
    return delete_diet(db, diet_id, pet_id)
