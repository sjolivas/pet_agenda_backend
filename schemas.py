from re import T
from typing import List
from pydantic import BaseModel, validator
from datetime import datetime, date


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

# Pet Schema
class PetBase(BaseModel):
    first_name: str
    last_name: str
    birthday: date 
    adopt_date: str

class PetCreate(PetBase):
    pass

class Pet(PetBase):
    id: int
    owner_id: int
    date_created: datetime
    date_last_updated: datetime

    class Config:
        orm_mode = True


# User Schema
class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    is_active: bool
    pets: List[Pet] = []
    date_created: datetime

    class Config:
        orm_mode = True
