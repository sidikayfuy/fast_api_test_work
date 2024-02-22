from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func, Table
from sqlalchemy.orm import relationship

from database import Base

device_users = Table('device_users', Base.metadata,
                     Column('device_id', ForeignKey('device.id'), primary_key=True),
                     Column('user_id', ForeignKey('users.id'), primary_key=True)
                     )


class Device(Base):
    __tablename__ = 'device'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    statistics = relationship("Statistics", back_populates="device")
    users = relationship("User", secondary=device_users, back_populates="devices")


class Statistics(Base):
    __tablename__ = 'statistics'

    id = Column(Integer, primary_key=True, index=True)
    x = Column(Float)
    y = Column(Float)
    z = Column(Float)
    device_id = Column(Integer, ForeignKey("device.id"))
    date = Column(DateTime, default=func.now())
    device = relationship("Device", back_populates="statistics")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    devices = relationship("Device", secondary=device_users, back_populates="users")
