from typing import Any

from fastapi import APIRouter, HTTPException, Depends, Body, status

from src.security import validate_token

from src.address_book import service
from src.address_book.schemas import (
    Address,
    AddressResponse,
    AddressListResponse,
)

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=AddressResponse,
)
async def create_address(
    *,
    token: str = Depends(validate_token),
    auth_data: Address = Body(...),
) -> dict[str, str]:
    addr = await service.create_address(auth_data)

    if not addr:
        raise HTTPException(400, "Unable to create address")

    return {"status": "sucess", "data": addr}


@router.get(
    "/{addr_id}",
    response_model=AddressResponse,
    status_code=status.HTTP_200_OK,
)
async def get_address_by_id(
    *,
    token: str = Depends(validate_token),
    addr_id: int,
) -> dict[str, str]:
    addr = await service.get_address_by_id(addr_id)

    if not addr:
        raise HTTPException(404, "Address not found.")

    return {"status": "sucess", "data": addr}


@router.get(
    "/",
    response_model=AddressListResponse,
)
async def get_address_by_distance(
    distance_km: float,
    long: float,
    lat: float,
) -> dict[str, Any]:
    addrs = await service.get_address_by_distance(distance_km, long, lat)

    if not addrs:
        raise HTTPException(
            404, "No address found within the given parameters."
        )

    return {"status": "sucess", "data": addrs}


@router.put(
    "/{addr_id}",
    status_code=status.HTTP_200_OK,
    response_model=AddressResponse,
)
async def update_address(
    addr_id: int,
    auth_data: Address,
) -> dict[str, str]:

    addr = await service.get_address_by_id(addr_id)

    if not addr:
        raise HTTPException(404, "Address not found.")

    updated_addr = await service.update_address(addr_id, auth_data)

    if not updated_addr:
        raise HTTPException(400, "Unable to update address")

    return {"status": "sucess", "data": updated_addr}


@router.delete(
    "/{addr_id}",
    status_code=status.HTTP_200_OK,
    response_model=AddressResponse,
)
async def delete_address(
    addr_id: int,
) -> dict[str, str]:

    addr = await service.get_address_by_id(addr_id)

    if not addr:
        raise HTTPException(404, "Address not found.")

    updated_addr = await service.delete_address(addr_id)

    if not updated_addr:
        raise HTTPException(400, "Unable to delete address")

    return {"status": "sucess", "data": updated_addr}
