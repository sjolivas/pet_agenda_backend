from fastapi import APIRouter, Depends, HTTPException, status
from crud.medical_info import get_medicalinfo, create_pet_medinfo, delete_medicalinfo
from crud.pet import get_pet
import database
import schemas


router = APIRouter(prefix="/users", tags=["medical info"])

# Create
@router.post(
    "/{user_id}/pets/{pet_id}/medicalinfo",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.MedicalInfo,
)
def create_medinfo(
    pet_id: int,
    medical_info: schemas.MedicalInfoCreate,
    db: database.SessionLocal = Depends(database.get_db),
):
    return create_pet_medinfo(db=db, medical_info=medical_info, pet_id=pet_id)


# Read
@router.get(
    "/{user_id}/pet/{pet_id}/medicalinfo/{medicalinfo_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.MedicalInfo,
)
def read_medicalinfo(
    pet_id: int,
    medicalinfo_id: int,
    user_id: int,
    db: database.SessionLocal = Depends(database.get_db),
):
    pet = get_pet(db, pet_id=pet_id, user_id=user_id)
    medicalinfo = get_medicalinfo(db, medicalinfo_id, pet_id)
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")
    if medicalinfo is None:
        raise HTTPException(status_code=404, detail="No medical information found")
    return medicalinfo


# Delete
@router.delete(
    "/{user_id}/pet/{pet_id}/medicalinfo/{medicalinfo_id}",
    status_code=status.HTTP_200_OK,
)
def delete_pet_medicalinfo(
    pet_id: int,
    medicalinfo_id: int,
    user_id: int,
    db: database.SessionLocal = Depends(database.get_db),
):
    pet = get_pet(db, pet_id=pet_id, user_id=user_id)
    medicalinfo = get_medicalinfo(db, medicalinfo_id, pet_id)
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")
    if medicalinfo is None:
        raise HTTPException(status_code=404, detail="Diet not found")
    return delete_medicalinfo(db, medicalinfo_id, pet_id)
