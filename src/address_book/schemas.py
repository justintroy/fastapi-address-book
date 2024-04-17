from datetime import datetime
from pydantic import field_validator, BaseModel


class Address(BaseModel):
    street: str
    city: str
    state: str
    country: str
    postal_code: int
    latitude: float
    longitude: float

    @field_validator("postal_code", mode="after")
    @classmethod
    def valid_postal(cls, code: int) -> int:
        if code > 9999 or code < 1000:
            raise ValueError("Postal code must be 4 digits.")

        return code


class AddressReturn(Address):
    id: int
    created_at: datetime


class AddressResponse(BaseModel):
    status: str
    data: AddressReturn


class AddressListResponse(BaseModel):
    status: str
    data: list[AddressReturn]
