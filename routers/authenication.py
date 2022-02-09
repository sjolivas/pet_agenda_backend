from fastapi import APIRouter, Depends, HTTPException, status
from database import SessionLocal, get_db
import schemas
from crud.user import get_user_by_email
from datetime import timedelta
from auth_token import create_access_token
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(request: schemas.Login, db: SessionLocal = Depends(get_db)):
    user = get_user_by_email(db, request.username)
    if not user or not user.verify_password(request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
