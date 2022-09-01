import datetime
from typing import List, Optional, Union

from pydantic import BaseModel, validator

# This is just an example
ALLOWED_METRICS = ["Voltage", "Current"]


class MetricInput(BaseModel):
    input_str: str

    @validator("*", pre=True)
    def have_invalid_key_qty(cls, v):
        metrics = v.split("\n")
        for metric in metrics:
            if len(metric.split()) != 3:
                raise ValueError(
                    f"Invalid metric string: '{metric}'. "
                    f"The metric should have three components: timestamp, metric_name, metric_value."
                )
        return v

    def extract(self):
        return [metric_str.split() for metric_str in self.input_str.split("\n")]


class Metric(BaseModel):
    timestamp: datetime.datetime
    metric_name: str
    metric_value: float

    @validator("timestamp")
    def timestamp_in_future(cls, v: datetime.datetime) -> Optional[datetime.datetime]:
        # Cast to UTC if value is coming from db
        if v.tzinfo is None:
            v = v.replace(tzinfo=datetime.timezone.utc)
        if datetime.datetime.now(tz=datetime.timezone.utc) < v:
            raise ValueError(f"The date must be from past")
        return v

    @validator("metric_name")
    def metric_not_allowed(cls, v: str) -> Optional[str]:
        if v not in ALLOWED_METRICS:
            raise ValueError(
                f"Metric name should be one of the following {ALLOWED_METRICS}"
            )
        return v

    @validator("metric_value")
    def metric_value_is_negative(cls, v: float) -> Optional[float]:
        if v < 0:
            raise ValueError("Metric value should be positive")
        return v

    class Config:
        orm_mode = True


class MetricBulk(BaseModel):
    objects: List[Metric]


class FilterMetricByDate(BaseModel):
    date_from: Optional[Union[datetime.date, datetime.datetime]]
    date_to: Optional[Union[datetime.date, datetime.datetime]]

    @validator("date_from")
    def date_from_is_none(cls, v: datetime.date) -> Optional[datetime.date]:
        if v is None:
            raise ValueError("Start date is required")
        return v

    @validator("date_to")
    def date_to_is_none(cls, v: datetime.date) -> Optional[datetime.date]:
        if v is None:
            return datetime.datetime.now(tz=datetime.timezone.utc)
        return v


class FilterMetricDateResponse(BaseModel):
    data: List[Metric]
