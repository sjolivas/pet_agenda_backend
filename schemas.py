from typing import List, Optional
from pydantic import BaseModel, NonNegativeInt, EmailStr
from datetime import datetime, date

# Note Schema
class NoteBase(BaseModel):
    title: str
    message: str


class NoteCreate(NoteBase):
    created_at: datetime


class Note(NoteBase):
    id: int
    owner_id: int
    updated_at: datetime

    class Config:
        orm_mode = True


# Medical Information Schema
class MedicalInfoBase(BaseModel):
    microchip_number: str
    vaccinations: str
    last_vet_apt: date
    past_injuries: str
    medications: str
    allergies: str


class MedicalInfoCreate(MedicalInfoBase):
    created_at: datetime


class MedicalInfo(MedicalInfoBase):
    id: int
    owner_id: int
    updated_at: datetime

    class Config:
        orm_mode = True


# Diet Schema
class DietBase(BaseModel):
    food_type: str
    amount_per_day: int
    feeding_frequency: int
    treats: str


class DietCreate(DietBase):
    created_at: datetime


class Diet(DietBase):
    id: int
    owner_id: int
    updated_at: datetime

    class Config:
        orm_mode = True


# Pet Schema
class PetBase(BaseModel):
    picture: str
    first_name: str
    last_name: str
    birthday: Optional[date] = None
    adopt_date: Optional[date] = None
    age: NonNegativeInt
    weight: int
    breed: str
    color: Optional[str] = None
    other_characteristics: Optional[str] = None
    fav_person: Optional[str] = None
    fav_activity: Optional[str] = None
    fav_treat: Optional[str] = None
    fav_toy: Optional[str] = None


class PetCreate(PetBase):
    created_at: datetime


class Pet(PetBase):
    id: int
    owner_id: int
    diets: List[Diet] = []
    medicalinfo: List[MedicalInfo] = []
    updated_at: datetime

    class Config:
        orm_mode = True


# User Schema
class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class UserCreate(UserBase):
    hashed_password: str
    created_at: datetime


class User(UserBase):
    id: int
    is_active: bool
    updated_at: datetime
    pets: List[Pet] = []
    note: List[Note] = []

    class Config:
        orm_mode = True


# class UserUpdate(BaseModel):
#     first_name: Optional[str] = None
#     last_name: Optional[str] = None
#     email: Optional[EmailStr] = None
#     hashed_password: Optional[str] = None
