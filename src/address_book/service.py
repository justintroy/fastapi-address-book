import uuid
from datetime import datetime, timezone
from typing import Any

from pydantic import UUID4
from sqlalchemy import insert, select, func, update, delete
from sqlalchemy.exc import SQLAlchemyError, OperationalError

from src.database import fetch_all, fetch_one
from src.address_book.models import addresses
from src.address_book.schemas import Address


async def create_address(addr: Address) -> dict[str, Any] | None:
    """Asynchronously creates Address entry to database.
    Returns the created Address on success
    Returns None on failure

    :param addr: The Address object to create.
    """
    try:
        insert_query = (
            insert(addresses)
            .values(
                {
                    **addr.dict(),
                    "created_at": datetime.utcnow(),
                }
            )
            .returning(addresses)
        )

        return await fetch_one(insert_query)

    except (SQLAlchemyError, OperationalError) as e:
        return None


async def get_address_by_id(id: int) -> dict[str, Any] | None:
    """Asynchronously fetches Address to db with id.
    Returns the Address
    Returns None if not found

    :param id: Address id
    """
    try:
        query = (
            select(addresses)
            .where(addresses.c.id == id)
        )

        return await fetch_one(query)

    except (SQLAlchemyError, OperationalError) as e:
        return None


async def get_address_by_distance(
    distance_km: float, longitude: float, latitude: float
) -> list[dict[str, Any]] | None:
    """Asynchronously fetches addresses that are within a given
    distance (in kilometers) from a specified location
    Returns: List of addresses within the specified distance from the location.

    :param id: Address id
    """
    try:
        # Haversine formula for calculating distances
        haversine_formula = (
            6371 * func.acos(
                func.cos(func.radians(latitude)) *
                func.cos(func.radians(addresses.c.latitude)) *
                func.cos(func.radians(addresses.c.longitude) - func.radians(longitude)) +
                func.sin(func.radians(latitude)) *
                func.sin(func.radians(addresses.c.latitude))
            )
        )

        # Query to get addresses within the specified distance
        query = (
            select(addresses)
            .where(haversine_formula <= distance_km)
        )

        return await fetch_all(query)

    except (SQLAlchemyError, OperationalError) as e:
        return None


async def update_address(id: int, addr: Address) -> dict[str, Any] | None:
    """Asynchronously updates Address entry to database.
    Returns the updated Address on success
    Returns None on failure

    :param addr: The Address object to create.
    """
    try:
        update_query = (
            update(addresses)
            .where(addresses.c.id == id)
            .values(addr.dict())
            .returning(addresses)
        )

        return await fetch_one(update_query)

    except (SQLAlchemyError, OperationalError) as e:
        return None


async def delete_address(id: int) -> dict[str, Any] | None:
    """Asynchronously deletes Address entry to database.
    Returns the deleted Address on success
    Returns None on failure

    :param addr: The Address object to create.
    """
    try:
        update_query = (
            delete(addresses)
            .where(addresses.c.id == id)
            .returning(addresses)
        )

        return await fetch_one(update_query)

    except (SQLAlchemyError, OperationalError) as e:
        return None
