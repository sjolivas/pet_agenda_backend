from sqlalchemy.orm import Session
import models, schemas
from datetime import datetime

# MedicalInfo Create Utility Function
def create_pet_medinfo(
    db: Session, medical_info: schemas.MedicalInfoCreate, pet_id: int
):
    db_medical_info = models.MedicalInfo(**medical_info.dict(), owner_id=pet_id)
    db.add(db_medical_info)
    db.commit()
    db.refresh(db_medical_info)
    return db_medical_info


# MedicalInfo READ utility functions
def get_medicalinfo(db: Session, medicalinfo_id: int, pet_id: int, user_id: int):
    return (
        db.query(models.MedicalInfo)
        .filter(models.MedicalInfo.owner_id == pet_id)
        .filter(models.MedicalInfo.id == medicalinfo_id)
        .first()
    )


# Medical Info DELETE utility functions
def delete_medicalinfo(db: Session, medicalinfo_id: int, pet_id: int):
    (
        db.query(models.MedicalInfo)
        .filter(models.MedicalInfo.owner_id == pet_id)
        .filter(models.MedicalInfo.id == medicalinfo_id)
        .delete(synchronize_session=False)
    )
    db.commit()

    return "Successfully Deleted"
