from typing import Optional

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Session


class Singleton:
    __initialized = False

    def __new__(cls, *args, **kwargs):
        if not cls.__initialized:
            cls.__init__(*args, **kwargs)
            cls.__initialized = True
        return cls


class Database(Singleton):
    db: Optional[SQLAlchemy] = None
    session: Optional[Session] = None

    @classmethod
    def __init__(cls):
        super(Database, cls).__init__()

    @classmethod
    def init(cls):
        if cls.db is None:
            cls.db = SQLAlchemy()

    @classmethod
    def create_tables(cls, app):
        cls.db.create_all(app=app)

    @classmethod
    def create_session(cls):
        if cls.session is None:
            cls.session = cls.db.create_scoped_session()

    @classmethod
    def bind(cls, app: Flask):
        cls.db.init_app(app)

    @classmethod
    def get_db(cls) -> SQLAlchemy:
        return cls.db

    @classmethod
    def get_session(cls) -> Session:
        return cls.session
