from typing import List, Optional

import api.metric.model as model
import api.metric.schemas as schemas
from storage.db import Database

session = Database.session


# def create_metric(metric: schemas.Metric):
#     db_metric = model.Metric(**metric.dict())
#     session.add(db_metric)
#     session.commit()
#     session.refresh(db_metric)

def bulk_create_metric(bulk: schemas.MetricBulk):
    metrics = [model.Metric(**valid_metric.dict()) for valid_metric in bulk.objects]
    session.bulk_save_objects(metrics)


def filter_metric_by_date(filter: schemas.FilterMetricByDate,) -> Optional[List[model.Metric]]:
    q = session.query(model.Metric)
    q.filter(
        model.Metric.timestamp > filter.date_from,
        model.Metric.timestamp < filter.date_to,
    )
    return q.all()
