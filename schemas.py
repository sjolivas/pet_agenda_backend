from typing import List, Optional
from pydantic import BaseModel, NonNegativeInt, EmailStr
from datetime import datetime, date


# Medical Information Schema
class MedicalInfoBase(BaseModel):
    microchip_number: str
    vaccinations: list
    last_vet_apt: date
    past_injuries: Optional[list] = None
    medications: Optional[list] = None
    allergies: Optional[list] = None


class MedicalInfoCreate(MedicalInfoBase):
    pass


class MedicalInfo(MedicalInfoBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Diet Schema
class DietBase(BaseModel):
    food_type:str
    amount_per_day: int
    feeding_frequency: int
    treats: List
    allergies: Optional[str] = None


class DietCreate(DietBase):
    pass


class Diet(DietBase):
    id: int
    owner_id: int
    created_at: datetime
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
    pass


class Pet(PetBase):
    id: int
    owner_id: int
    created_at: datetime
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


class User(UserBase):
    id: int
    is_active: bool
    pets: List[Pet] = []
    created_at: datetime

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    hashed_password: Optional[str] = None

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
