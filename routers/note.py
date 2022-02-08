from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
import crud
import database
import schemas


router = APIRouter(tags=["notes"])

# Create
@router.post(
    "/users/{user_id}/notes",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Note,
)
def create_note(
    user_id: int,
    note: schemas.NoteCreate,
    db: database.SessionLocal = Depends(database.get_db),
):
    return crud.create_note(db=db, note=note, user_id=user_id)


# Read
@router.get(
    "/users/{user_id}/notes",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.Note],
)
def read_notes(
    user_id: int,
    skip: int = 0,
    limit: int = 10,
    db: database.SessionLocal = Depends(database.get_db),
):
    notes = crud.get_all_notes(db, user_id, skip=skip, limit=limit)
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return notes


@router.get(
    "/users/{user_id}/notes/{note_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.Note,
)
def read_note(
    note_id: int, user_id: int, db: database.SessionLocal = Depends(database.get_db)
):
    db_user = crud.get_user(db, user_id=user_id)
    note = crud.get_note(db, note_id=note_id, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    return note


# Delete
@router.delete(
    "/users/{user_id}/notes/{note_id}",
    status_code=status.HTTP_200_OK,
)
def delete_note(
    note_id: int, user_id: int, db: database.SessionLocal = Depends(database.get_db)
):
    db_user = crud.get_user(db, user_id=user_id)
    note = crud.get_note(db, note_id=note_id, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return crud.delete_note(db, note_id, user_id)
