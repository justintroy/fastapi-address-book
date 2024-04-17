from typing import Any

from sqlalchemy import (
    CursorResult,
    Insert,
    MetaData,
    Select,
    Update,
)
from sqlalchemy.ext.asyncio import create_async_engine

from src.config import config

engine = create_async_engine(config.DATABASE_URL, pool_pre_ping=True)
metadata = MetaData()

# DB operations helper async functions


async def fetch_one(query: Select | Insert | Update) -> dict[str, Any] | None:
    """Asynchronously fetch one record, returns None if no result.

    :param query: The SQL query to execute.
    """
    async with engine.begin() as conn:
        cursor: CursorResult = await conn.execute(query)
        result = cursor.first()
        return (
            result._asdict()
            if result
            else None
        )


async def fetch_all(query: Select | Insert | Update) -> list[dict[str, Any]]:
    """Asynchronously Fetch all record, returns empty list if no result.

    :param query: The SQL query to execute.
    """
    async with engine.begin() as conn:
        cursor: CursorResult = await conn.execute(query)
        return [r._asdict() for r in cursor.all()]


async def execute(query: Insert | Update) -> None:
    """Execute the provided SQL query asynchronously.

    :param query: The INSERT or UPDATE statement to execute.
    """
    async with engine.begin() as conn:
        await conn.execute(query)
