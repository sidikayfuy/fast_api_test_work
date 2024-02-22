import os
from datetime import date
from celery import Celery
from sqlalchemy import func
import models
from helpers import calculate_median
from database import get_db_celery


redis_host = os.getenv('REDIS_HOST', 'localhost')

celery = Celery('hello', backend=f'redis://{redis_host}:6379/1', broker=f'redis://{redis_host}:6379/')


@celery.task
def get_all_statistics_by_device_id(device_id: int):
    with get_db_celery() as db:
        query_result = (
            statistic_query(db)
            .filter(models.Statistics.device_id == device_id)
            .first()
        )

        result = statistic_result(query_result)

        return result


@celery.task
def get_in_period_statistics_by_device_id(device_id: int, from_date: date = None, to_date: date = None):
    with get_db_celery() as db:
        query = (
            statistic_query(db)
            .filter(models.Statistics.device_id == device_id)
        )

        if from_date is not None:
            query = query.filter(models.Statistics.date >= from_date)

        if to_date is not None:
            query = query.filter(models.Statistics.date <= to_date)

        query_result = query.first()

        result = statistic_result(query_result)

        return result


def statistic_query(db):
    return db.query(
            func.min(models.Statistics.x).label("min_x"),
            func.max(models.Statistics.x).label("max_x"),
            func.avg(models.Statistics.x).label("avg_x"),
            func.count(models.Statistics.x).label("count_x"),
            func.group_concat(models.Statistics.x, ',').label("list_x"),
            func.min(models.Statistics.y).label("min_y"),
            func.max(models.Statistics.y).label("max_y"),
            func.avg(models.Statistics.y).label("avg_y"),
            func.count(models.Statistics.y).label("count_y"),
            func.group_concat(models.Statistics.y, ',').label("list_y"),
            func.min(models.Statistics.z).label("min_z"),
            func.max(models.Statistics.z).label("max_z"),
            func.avg(models.Statistics.z).label("avg_z"),
            func.count(models.Statistics.z).label("count_z"),
            func.group_concat(models.Statistics.z, ',').label("list_z"),
        )


def statistic_result(query_result):
    return {
        "x": {
            "min": query_result.min_x,
            "max": query_result.max_x,
            "avg": query_result.avg_x,
            "count": query_result.count_x,
            "median": calculate_median(query_result.list_x) if query_result.list_x else None,
        },
        "y": {
            "min": query_result.min_y,
            "max": query_result.max_y,
            "avg": query_result.avg_y,
            "count": query_result.count_y,
            "median": calculate_median(query_result.list_y) if query_result.list_y else None,
        },
        "z": {
            "min": query_result.min_z,
            "max": query_result.max_z,
            "avg": query_result.avg_z,
            "count": query_result.count_z,
            "median": calculate_median(query_result.list_z) if query_result.list_z else None,
        },
    }


@celery.task
def get_all_devices_statistics_by_user_id(user_id: int):
    with get_db_celery() as db:
        result = (
            statistic_query(db)
            .join(models.Statistics.device)
            .join(models.Device.users)
            .filter(models.User.id == user_id)
            .first()
        )
        query_result = result

        result = statistic_result(query_result)

        return result


@celery.task
def get_all_devices_statistics_by_user_id_with_grouping(user_id: int):
    with get_db_celery() as db:
        results = (
            db.query(
                models.Statistics.device_id,
                func.min(models.Statistics.x).label("min_x"),
                func.max(models.Statistics.x).label("max_x"),
                func.avg(models.Statistics.x).label("avg_x"),
                func.count(models.Statistics.x).label("count_x"),
                func.group_concat(models.Statistics.x, ',').label("list_x"),
                func.min(models.Statistics.y).label("min_y"),
                func.max(models.Statistics.y).label("max_y"),
                func.avg(models.Statistics.y).label("avg_y"),
                func.count(models.Statistics.y).label("count_y"),
                func.group_concat(models.Statistics.y, ',').label("list_y"),
                func.min(models.Statistics.z).label("min_z"),
                func.max(models.Statistics.z).label("max_z"),
                func.avg(models.Statistics.z).label("avg_z"),
                func.count(models.Statistics.z).label("count_z"),
                func.group_concat(models.Statistics.z, ',').label("list_z"),
            ).group_by(models.Statistics.device_id)
            .join(models.Device, models.Statistics.device_id == models.Device.id)
            .join(models.Device.users)
            .filter(models.User.id == user_id)
            .all()
        )

        result_dict = {}
        for query_result in results:
            device_id = query_result.device_id
            result_dict[device_id] = statistic_result(query_result)

        return result_dict
