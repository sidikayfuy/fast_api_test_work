from datetime import datetime
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
import crud
from tasks import get_in_period_statistics_by_device_id, get_all_devices_statistics_by_user_id, get_all_statistics_by_device_id, get_all_devices_statistics_by_user_id_with_grouping
import schemas
from database import get_db

router = APIRouter(
    prefix="/statistics",
    tags=["Statistics"]
)


@router.post("", response_model=schemas.StatisticsAdd)
def create_statistics(statistics: Annotated[schemas.StatisticsAdd, Depends()], db: Session = Depends(get_db)):
    return crud.create_statistics(db=db, statistics=statistics)


@router.get("/device/all_stat/{device_id}")
async def get_all_device_statistics_by_id(device_id: int):
    task_result = get_all_statistics_by_device_id.apply_async((device_id,))
    result = task_result.get()
    return result


@router.get("/device/period_stat/{device_id}")
async def get_period_device_statistics_by_id(device_id: int,
                                       from_date: Optional[datetime] = Query(None, description="Start date for statistics"),
                                       to_date: Optional[datetime] = Query(None, description="End date for statistics")):
    task_result = get_in_period_statistics_by_device_id.apply_async((device_id, from_date, to_date))
    result = task_result.get()
    return result


@router.get("/users/all_device_stat/{user_id}")
async def all_devices_statistics_by_user_id(user_id: int):
    task_result = get_all_devices_statistics_by_user_id.apply_async((user_id,))
    result = task_result.get()
    return result


@router.get("/users/stat_group_by_device/{user_id}")
async def all_devices_statistics_by_user_id_with_grouping(user_id: int):
    task_result = get_all_devices_statistics_by_user_id_with_grouping.apply_async((user_id,))
    result = task_result.get()
    return result
