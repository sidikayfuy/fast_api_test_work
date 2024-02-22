from sqlalchemy.orm import Session
import models
import schemas


def get_device_by_id(db: Session, device_id: int):
    return db.query(models.Device).filter(models.Device.id == device_id).first()


def get_devices(db: Session):
    return db.query(models.Device).all()


def create_device(db: Session, device: schemas.DeviceCreate):
    db_device = models.Device(**device.dict())
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device


def create_statistics(db: Session, statistics: schemas.StatisticsAdd):
    db_statistics = models.Statistics(**statistics.dict())
    db.add(db_statistics)
    db.commit()
    db.refresh(db_statistics)
    return db_statistics


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session):
    return db.query(models.User).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def add_user_to_device_by_id(db: Session, user_id: int, device_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    device = db.query(models.Device).filter(models.Device.id == device_id).first()

    if user is None or device is None:
        return {"error": "User or Device not found"}

    if user in device.users:
        return {"message": "User is already associated with the device"}

    device.users.append(user)
    db.commit()

    return {'status': 'success'}
