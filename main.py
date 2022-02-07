from email.generator import Generator
from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware

# creates the tables in our database
models.Base.metadata.create_all(bind=engine)

# app object
app = FastAPI()

# Make the connection to our frontend
origins = ["https://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Dependency
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", status_code=status.HTTP_200_OK, tags=["root"])
def root():
    return {"message": "Soos is the bestest!"}


@app.post("/users/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=409, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", status_code=status.HTTP_200_OK, response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get(
    "/users/{user_id}", status_code=status.HTTP_200_OK, response_model=schemas.User
)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post(
    "/users/{user_id}/pets/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.PetCreate,
)
def create_pet_for_user(
    user_id: int, pet: schemas.PetCreate, db: Session = Depends(get_db)
):
    return crud.create_user_pet(db=db, pet=pet, user_id=user_id)


@app.get(
    "/users/{user_id}/pets/",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.Pet],
)
def read_pets(
    user_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    pets = crud.get_pets(db, user_id, skip=skip, limit=limit)
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return pets


@app.get(
    "/users/{user_id}/pets/{pet_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.Pet,
)
def read_pet(pet_id: int, user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    pet = crud.get_pet(db, pet_id=pet_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet

# Update USER
@app.put("/user/{user_id}", status_code=200)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    crud.update_user(db, user_id, user)
    return {"message": "Successfully Updated"}

# Update PET
@app.put("/user/{user_id}/pets/{pet_id}", status_code=200)
def update_pet(pet_id: int, pet: schemas.PetCreate, db: Session = Depends(get_db)):
    db_pet = crud.get_pet(db, pet_id=pet_id)
    if db_pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")
    crud.update_pet(db, pet_id, pet)
    return {"message": "Successfully Updated"}


@app.delete("/user/{user_id}", status_code=200)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.delete_user(db, user_id)


@app.delete("/user/{user_id}/pets/{pet_id}", status_code=200)
def delete_pet(pet_id: int, user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    pet = crud.get_pet(db, pet_id=pet_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")
    return crud.delete_pet(db, pet_id)
