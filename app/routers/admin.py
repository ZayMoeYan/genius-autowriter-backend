from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.deps import get_db

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/users", response_model=schemas.UserOut, status_code=201)
def create_user_admin(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = crud.create_user(db, user_in, is_admin=False)
    return user
