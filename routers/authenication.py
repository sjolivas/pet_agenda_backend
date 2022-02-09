from fastapi import APIRouter, Depends, HTTPException, status
from database import SessionLocal, get_db
import schemas, models

router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(request: schemas.Login, db: SessionLocal = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )
    if not user.verify_password(request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )
    return user
