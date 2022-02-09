from typing import List, Optional
from pydantic import BaseModel, NonNegativeInt, EmailStr
from datetime import datetime, date


# Item Schema
class ItemBase(BaseModel):
    name: str
    count: int


class ItemCreate(ItemBase):
    created_at: datetime


class Item(ItemBase):
    id: int
    owner_id: int
    updated_at: datetime

    class Config:
        orm_mode = True


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    count: Optional[int] = None


# Shopping List Schema
class ShoppingListBase(BaseModel):
    title: str


class ShoppingListCreate(ShoppingListBase):
    created_at: datetime


class ShoppingList(ShoppingListBase):
    id: int
    items: List[Item] = []
    owner_id: int
    updated_at: datetime

    class Config:
        orm_mode = True


class ShoppingListUpdate(BaseModel):
    title: Optional[str] = None


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


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    message: Optional[str] = None


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


class MedicalInfoUpdate(BaseModel):
    microchip_number: Optional[str] = None
    vaccinations: Optional[str] = None
    last_vet_apt: Optional[date] = None
    past_injuries: Optional[str] = None
    medications: Optional[str] = None
    allergies: Optional[str] = None


# Diet Schema
class DietBase(BaseModel):
    food_type: str
    amount_per_day: float
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


class DietUpdate(BaseModel):
    food_type: Optional[str] = None
    amount_per_day: Optional[float] = None
    feeding_frequency: Optional[int] = None
    treats: Optional[str] = None


# Pet Schema
class PetBase(BaseModel):
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


class PetUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birthday: Optional[date] = None
    adopt_date: Optional[date] = None
    age: Optional[NonNegativeInt] = None
    weight: Optional[int] = None
    breed: Optional[str] = None
    color: Optional[str] = None
    other_characteristics: Optional[str] = None
    fav_person: Optional[str] = None
    fav_activity: Optional[str] = None
    fav_treat: Optional[str] = None
    fav_toy: Optional[str] = None


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
    shoppinglist: List[ShoppingList] = []

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
