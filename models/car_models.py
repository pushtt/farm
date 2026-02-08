from typing import Annotated

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, field_validator

PyObjectId = Annotated[str, BeforeValidator(str)]


class CarModel(BaseModel):
    id: PyObjectId | None = Field(alias="_id", default=None)
    brand: str = Field(...)
    make: str = Field(...)
    year: int = Field(..., gt=1970, lt=2027)
    cm3: int = Field(..., gt=0, lt=5000)
    km: int = Field(..., gt=0, lt=500000)
    price: int = Field(..., gt=0, lt=100000)

    @field_validator("make")
    @classmethod
    def check_make_case(cls, v: str) -> str:
        return v.title()

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "brand": "Ford",
                "make": "Fiesta",
                "year": 2019,
                "cm3": 1500,
                "km": 120000,
                "price": 10000,
            }
        },
    )


class UpdateCarModel(BaseModel):
    brand: str | None = Field(...)
    make: str | None = Field(...)
    year: int | None = Field(..., gt=1970, lt=2025)
    cm3: int | None = Field(..., gt=0, lt=5000)
    km: int | None = Field(..., gt=0, lt=500 * 1000)
    price: int | None = Field(..., gt=0, lt=100 * 1000)


class CarCollection(BaseModel):
    cars: list[CarModel]
