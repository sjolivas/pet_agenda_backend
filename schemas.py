from typing import List, Optional
from pydantic import BaseModel, NonNegativeInt, EmailStr
from datetime import datetime, date

# Event Schema
class EventBase(BaseModel):
    title: str
    start_date_time_utc: date
    end_date_time_utc: date
    is_all_day: bool
    is_reocurring: bool


class EventCreate(EventBase):
    created_at: datetime


class Event(EventBase):
    id: int
    owner_id: int
    updated_at: datetime


    class Config:
        orm_mode = True

# Medical Information Schema
class MedicalInfoBase(BaseModel):
    microchip_number: str
    vaccinations: List[str]
    last_vet_apt: date
    past_injuries: List[str] = []
    medications: List[str] = []
    allergies: List[str] = []


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
    food_type:str
    amount_per_day: int
    feeding_frequency: int
    treats: List[str] = []
    allergies: Optional[str] = None


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
    updated_at: datetime

    class Config:
        orm_mode = True


# User Schema
class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    updated_at: datetime


class UserCreate(UserBase):
    hashed_password: str
    created_at: datetime


class User(UserBase):
    id: int
    is_active: bool
    pets: List[Pet] = []


    class Config:
        orm_mode = True

# class UserUpdate(BaseModel):
#     first_name: Optional[str] = None
#     last_name: Optional[str] = None
#     email: Optional[EmailStr] = None
#     hashed_password: Optional[str] = None

# Pydantic Models/Schemas
# need to create a PetBase and UserBase

# need a PetCreate and UserCreate
# - inherit from the Pydantic SChema
# - have same attrs plus any additional data needed for creation
#       - the user will also have a password when creating it
#       - the password won't be in other pydantic models - won't be sent from API when reading a user

# Pydantic's orm_mode will tell the Pydantic model to read the data even if it's not a dict, but an ORM model
#   (or any other arbitrary object with attrs)
#   makes Pydantic model compatible with ORMs, and can be declared in the response_model argument in path operations
#   will be able to return a bd model and it will read the data from it
