from datetime import datetime
from pydantic import BaseModel


class StatisticsBase(BaseModel):
    x: float
    y: float
    z: float
    device_id: int


class StatisticsAdd(StatisticsBase):
    pass


class Statistics(StatisticsBase):
    id: int
    date: datetime

    class Config:
        orm_mode = True


class DeviceBase(BaseModel):
    name: str


class DeviceCreate(DeviceBase):
    pass


class UserBase(BaseModel):
    name: str


class Device(DeviceBase):
    id: int
    statistics: list[Statistics] = []
    users: list[UserBase] = []

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    devices: list[Device] = []

    class Config:
        orm_mode = True
