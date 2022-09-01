from storage.db import Database

db = Database.db


class Metric(db.Model):
    __tablename__ = "metrics"

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.TIMESTAMP, nullable=False)
    metric_name = db.Column(db.Text, nullable=False)
    metric_value = db.Column(db.Float, nullable=False)
