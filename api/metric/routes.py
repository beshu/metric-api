import json

from flask import Blueprint, request, jsonify
from pydantic import ValidationError

import api.metric.schemas as schemas
import api.metric.actions as db

metric_api = Blueprint("metric", __name__)


@metric_api.route("/data", methods=["GET", "POST"])
def data():
    try:
        if request.method == "POST":
            user_input = request.data.decode(encoding="UTF-8")
            valid_metric_input = schemas.MetricInput(input_str=user_input)
            bulk_container = schemas.MetricBulk(
                objects=[
                    schemas.Metric(
                        timestamp=metric[0],
                        metric_name=metric[1],
                        metric_value=metric[2],
                    )
                    for metric in valid_metric_input.extract()
                ]
            )
            db.bulk_create_metric(bulk_container)
            return jsonify(success=True)

        elif request.method == "GET":
            date_from, date_to = request.args.get("from"), request.args.get("to")
            valid_filter = schemas.FilterMetricByDate(
                date_from=date_from, date_to=date_to
            )
            filtered = db.filter_metric_by_date(valid_filter)
            metrics = [schemas.Metric.from_orm(metric) for metric in filtered]
            return schemas.FilterMetricDateResponse(data=metrics).json()

    except ValidationError as e:
        return e.json()
