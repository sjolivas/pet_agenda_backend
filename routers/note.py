from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from crud.note import get_note, get_all_notes, destroy_note, create_user_note
from crud.user import get_user
import database
import schemas


router = APIRouter(prefix="/users", tags=["notes"])

# Create - post operation
@router.post(
    "/{user_id}/notes",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Note,
)
def create_note(
    user_id: int,
    note: schemas.NoteCreate,
    db: database.SessionLocal = Depends(database.get_db),
):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return create_user_note(db=db, note=note, user_id=user_id)


# Read - get operation
@router.get(
    "/{user_id}/notes",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.Note],
)
def read_notes(
    user_id: int,
    skip: int = 0,
    limit: int = 10,
    db: database.SessionLocal = Depends(database.get_db),
):
    notes = get_all_notes(db, user_id, skip=skip, limit=limit)
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return notes


@router.get(
    "/{user_id}/notes/{note_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.Note,
)
def read_note(
    note_id: int, user_id: int, db: database.SessionLocal = Depends(database.get_db)
):
    db_user = get_user(db, user_id=user_id)
    note = get_note(db, note_id=note_id, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    return note


# Update - patch operation
@router.patch(
    "/{user_id}/notes/{note_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.Note,
)
def patch_note_info(
    note_id: int,
    user_id: int,
    note: schemas.NoteUpdate,
    db: database.SessionLocal = Depends(database.get_db),
):
    db_user = get_user(db, user_id)
    db_note = get_note(db, note_id=note_id, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    note_data = note.dict(exclude_unset=True)
    for key, value in note_data.items():
        setattr(db_note, key, value)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


# Delete - delete operation
@router.delete(
    "/{user_id}/notes/{note_id}",
    status_code=status.HTTP_200_OK,
)
def delete_note(
    note_id: int, user_id: int, db: database.SessionLocal = Depends(database.get_db)
):
    db_user = get_user(db, user_id=user_id)
    note = get_note(db, note_id=note_id, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return destroy_note(db, note_id, user_id)
