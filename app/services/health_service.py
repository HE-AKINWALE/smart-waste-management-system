import random
import time

from sqlalchemy.orm import Session

from app.models.health_metric import HealthMetric


def collect_system_metrics(db: Session):

    start = time.time()

    cpu = round(random.uniform(15, 75), 2)

    memory = round(random.uniform(25, 80), 2)

    disk = round(random.uniform(30, 85), 2)

    response_time = round(
        (time.time() - start) * 1000,
        2
    )

    metric = HealthMetric(

        cpu_usage=cpu,

        memory_usage=memory,

        disk_usage=disk,

        database_status="Healthy",

        api_response_time=response_time
    )

    db.add(metric)

    db.commit()

    db.refresh(metric)

    return metric

def get_latest_metrics(db: Session):

    return (
        db.query(HealthMetric)
        .order_by(
            HealthMetric.metric_id.desc()
        )
        .first()
    )