import dataclasses
from typing import Optional

# This is not used, however I think it would be nice to have these guys
# especially when creating config for db


@dataclasses.dataclass
class BaseProvider:
    protocol: str
    echo: Optional[bool]
    max_overflow: Optional[int]
    pool_size: Optional[int]
    pool_timeout: Optional[int]
    native_unicode: Optional[bool]


@dataclasses.dataclass
class SQLProvider(BaseProvider):
    db_name: str


@dataclasses.dataclass
class SQLiteProvider(SQLProvider):
    path: str


@dataclasses.dataclass
class PostgreSQLProvider(SQLProvider):
    host: Optional[str]
    port: Optional[int]
    username: Optional[str]
    password: Optional[str]
