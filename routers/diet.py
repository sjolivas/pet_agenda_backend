from fastapi import APIRouter, Depends, HTTPException, status
import crud
import database
import schemas


router = APIRouter()

# Create
@router.post(
    "/users/{user_id}/pet/{pet_id}/diets",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Diet,
)
def create_diet(
    pet_id: int,
    diet: schemas.DietCreate,
    db: database.SessionLocal = Depends(database.get_db),
):
    return crud.create_pet_diet(db=db, diet=diet, pet_id=pet_id)
