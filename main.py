from fastapi import FastAPI, status
import models
from database import engine
from fastapi.middleware.cors import CORSMiddleware
from routers import user, pet, diet, medical_info, note


# creates the tables in our database
models.Base.metadata.create_all(bind=engine)

# app object
app = FastAPI()

app.include_router(user.router)
app.include_router(pet.router)
app.include_router(diet.router)
app.include_router(medical_info.router)
app.include_router(note.router)

# Make the connection to our frontend
origins = ["https://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", status_code=status.HTTP_200_OK, tags=["root"])
def root():
    return {"message": "Soos is the bestest!"}
