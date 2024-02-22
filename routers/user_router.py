from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import crud
from typing import Annotated
import schemas
from database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("", response_model=schemas.UserCreate)
def create_user(user: Annotated[schemas.UserCreate, Depends()], db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


@router.get("", response_model=list[schemas.User])
def get_users(db: Session = Depends(get_db)):
    return crud.get_users(db=db)


@router.get("/{user_id}", response_model=schemas.User)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user_by_id(db=db, user_id=user_id)