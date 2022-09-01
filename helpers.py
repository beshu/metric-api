from importlib import import_module

from flask import Flask

from storage.db import Database


def run_database(app: Flask):
    Database.init()
    Database.bind(app)
    Database.create_session()


def register_metric_api(app):
    from api.metric.routes import metric_api

    app.register_blueprint(metric_api)
    Database.create_tables(app)
