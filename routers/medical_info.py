from fastapi import APIRouter, Depends, HTTPException, status
from crud.medical_info import get_medicalinfo, create_pet_medinfo, delete_medicalinfo
from crud.pet import get_pet
from crud.user import get_user
import database
from routers import user
import schemas


router = APIRouter(prefix="/users", tags=["Medical Information"])

# Create - post operation
@router.post(
    "/{user_id}/pets/{pet_id}/medicalinfo",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.MedicalInfo,
)
def create_medinfo(
    user_id: int,
    pet_id: int,
    medical_info: schemas.MedicalInfoCreate,
    db: database.SessionLocal = Depends(database.get_db),
):
    db_user = get_user(db, user_id=user_id)
    pet = get_pet(db, pet_id=pet_id, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")
    return create_pet_medinfo(db=db, medical_info=medical_info, pet_id=pet_id)


# Read - get operation
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
    db_user = get_user(db, user_id=user_id)
    pet = get_pet(db, pet_id=pet_id, user_id=user_id)
    medicalinfo = get_medicalinfo(db, medicalinfo_id, pet_id, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")
    if medicalinfo is None:
        raise HTTPException(status_code=404, detail="No medical information found")
    return medicalinfo


# Update - patch operation
@router.patch(
    "/{user_id}/pet/{pet_id}/medicalinfo/{medicalinfo_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.MedicalInfo,
)
def patch_medical_info(
    medicalinfo_id: int,
    pet_id: int,
    user_id: int,
    medicalinfo: schemas.MedicalInfoUpdate,
    db: database.SessionLocal = Depends(database.get_db),
):
    db_user = get_user(db, user_id=user_id)
    db_pet = get_pet(db, pet_id=pet_id, user_id=user_id)
    db_medicalinfo = get_medicalinfo(db, medicalinfo_id, pet_id, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")
    if db_medicalinfo is None:
        raise HTTPException(status_code=404, detail="MedicalInfo not found")
    medicalinfo_data = medicalinfo.dict(exclude_unset=True)
    for key, value in medicalinfo_data.items():
        setattr(db_medicalinfo, key, value)
    db.add(db_medicalinfo)
    db.commit()
    db.refresh(db_medicalinfo)
    return db_medicalinfo


# Delete - delete operation
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
    db_user = get_user(db, user_id=user_id)
    pet = get_pet(db, pet_id=pet_id, user_id=user_id)
    medicalinfo = get_medicalinfo(db, medicalinfo_id, pet_id, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")
    if medicalinfo is None:
        raise HTTPException(status_code=404, detail="Diet not found")
    return delete_medicalinfo(db, medicalinfo_id, pet_id)
