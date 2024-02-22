from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import crud
from typing import Annotated
import schemas
from database import get_db

router = APIRouter(
    prefix="/devices",
    tags=["Devices"]
)


@router.post("", response_model=schemas.Device)
def create_device(device: Annotated[schemas.DeviceCreate, Depends()], db: Session = Depends(get_db)):
    return crud.create_device(db=db, device=device)


@router.get("", response_model=list[schemas.Device])
def get_devices(db: Session = Depends(get_db)):
    return crud.get_devices(db=db)


@router.get("/{device_id}", response_model=schemas.Device)
def get_device_by_id(device_id: int, db: Session = Depends(get_db)):
    return crud.get_device_by_id(db=db, device_id=device_id)


@router.post("/add_user/{device_id}")
def add_user_to_device_by_id(device_id: int, user_id: int, db: Session = Depends(get_db)):
    return crud.add_user_to_device_by_id(db=db, device_id=device_id, user_id=user_id)
