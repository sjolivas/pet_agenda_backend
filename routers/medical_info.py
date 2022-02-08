from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
import crud
import database
import schemas


router = APIRouter()

# Create
@router.post(
    "/users/{user_id}/pets/{pet_id}/medicalinfo",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.MedicalInfo,
)
def create_medinfo(
    pet_id: int,
    medical_info: schemas.MedicalInfoCreate,
    db: database.SessionLocal = Depends(database.get_db),
):
    return crud.create_pet_medinfo(db=db, medical_info=medical_info, pet_id=pet_id)
