from email import header
from fastapi import FastAPI, status
import models
from database import engine
from fastapi.middleware.cors import CORSMiddleware
from routers import (
    user,
    pet,
    diet,
    medical_info,
    note,
    shopping_list,
    item,
)


# creates the tables in our database
models.Base.metadata.create_all(bind=engine)

# app object
app = FastAPI()

# app.include_router(authenication.router)
app.include_router(user.router)
app.include_router(pet.router)
app.include_router(diet.router)
app.include_router(medical_info.router)
app.include_router(note.router)
app.include_router(shopping_list.router)
app.include_router(item.router)

# Make the connection to our frontend
origins = [
    "https://localhost:3000",
    "http://localhost:3000",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", status_code=status.HTTP_200_OK, tags=["Root"])
def root():
    return {"message": "Soos is the bestest!"}
