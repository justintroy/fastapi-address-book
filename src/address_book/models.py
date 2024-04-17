from sqlalchemy import (
    Column,
    Float,
    DateTime,
    Integer,
    String,
    Table,
    func,
)
from src.database import metadata

addresses = Table(
    "addresses",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("street", String, index=True),
    Column("city", String, index=True),
    Column("state", String, index=True),
    Column("country", String, index=True),
    Column("postal_code", String, index=True),
    Column("latitude", Float, nullable=False),
    Column("longitude", Float, nullable=False),
    Column("created_at", DateTime, server_default=func.now(), nullable=False),
)
