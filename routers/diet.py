from fastapi import APIRouter, Depends, HTTPException, status
from crud.diet import create_pet_diet, get_diet, delete_diet
from crud.pet import get_pet
from crud.user import get_user
import database, schemas

# import oauth2


router = APIRouter(prefix="/users", tags=["Diet"])

# Create - post operation
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
    # get_current_user: schemas.User = Depends(oauth2.get_current_user),
):
    db_user = get_user(db, user_id=user_id)
    pet = get_pet(db, pet_id=pet_id, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")
    return create_pet_diet(db=db, diet=diet, pet_id=pet_id)


# Read - get operation
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
    # get_current_user: schemas.User = Depends(oauth2.get_current_user),
):
    db_user = get_user(db, user_id=user_id)
    pet = get_pet(db, pet_id=pet_id, user_id=user_id)
    diet = get_diet(db, diet_id, pet_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")
    if diet is None:
        raise HTTPException(status_code=404, detail="Diet not found")
    return diet


# Update - patch operation
@router.patch(
    "/{user_id}/pet/{pet_id}/diet/{diet_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.Diet,
)
def patch_diet_info(
    diet_id: int,
    pet_id: int,
    user_id: int,
    diet: schemas.DietUpdate,
    db: database.SessionLocal = Depends(database.get_db),
    # get_current_user: schemas.User = Depends(oauth2.get_current_user),
):
    db_user = get_user(db, user_id=user_id)
    db_pet = get_pet(db, pet_id=pet_id, user_id=user_id)
    db_diet = get_diet(db, diet_id, pet_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")
    if db_diet is None:
        raise HTTPException(status_code=404, detail="Diet not found")
    diet_data = diet.dict(exclude_unset=True)
    for key, value in diet_data.items():
        setattr(db_diet, key, value)
    db.add(db_diet)
    db.commit()
    db.refresh(db_diet)
    return db_diet


# Delete - delete operation
@router.delete(
    "/{user_id}/pet/{pet_id}/diet/{diet_id}",
    status_code=status.HTTP_200_OK,
)
def delete_pet_diet(
    pet_id: int,
    diet_id: int,
    user_id: int,
    db: database.SessionLocal = Depends(database.get_db),
    # get_current_user: schemas.User = Depends(oauth2.get_current_user),
):
    db_user = get_user(db, user_id=user_id)
    pet = get_pet(db, pet_id=pet_id, user_id=user_id)
    diet = get_diet(db, diet_id, pet_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")
    if diet is None:
        raise HTTPException(status_code=404, detail="Diet not found")
    return delete_diet(db, diet_id, pet_id)
