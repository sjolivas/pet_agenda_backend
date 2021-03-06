from sqlalchemy.orm import Session
import models, schemas


# Note Create Utility Function
def create_user_note(db: Session, note: schemas.NoteCreate, user_id: int):
    db_note = models.Note(**note.dict(), owner_id=user_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


# Note READ utility functions
def get_all_notes(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Note)
        .filter(models.Note.owner_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_note(db: Session, note_id: int, user_id: int):
    return (
        db.query(models.Note)
        .filter(models.Note.owner_id == user_id)
        .filter(models.Note.id == note_id)
        .first()
    )


# Note DELETE utility functions
def destroy_note(db: Session, note_id: int, user_id: int):
    (
        db.query(models.Note)
        .filter(models.Note.owner_id == user_id)
        .filter(models.Note.id == note_id)
        .delete(synchronize_session=False)
    )
    db.commit()

    return {"message": "Successfully Deleted"}
