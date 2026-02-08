from typing import Annotated, List

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, field_validator

PyObjectId = Annotated[str, BeforeValidator(str)]


class CarModel(BaseModel):
    """
    Container for a single car document in the database
    """

    id: PyObjectId | None = Field(alias="_id", default=None)
    brand: str = Field(...)
    make: str = Field(...)
    year: int = Field(..., gt=1970, lt=2025)
    cm3: int = Field(..., gt=0, lt=5000)
    km: int = Field(..., gt=0, lt=500 * 1000)
    price: int = Field(..., gt=0, lt=100000)
    user_id: str = Field(...)

    # add the picture file
    picture_url: str | None = Field(None)

    @field_validator("brand")
    @classmethod
    def check_brand_case(cls, v: str) -> str:
        return v.title()

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
                "picture_url": "https://images.pexels.com/photos/2086676/pexels-photo-2086676.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260",
            }
        },
    )


class UpdateCarModel(BaseModel):
    """
    Optional updates
    """

    brand: str | None = None
    make: str | None = None
    year: int | None = Field(gt=1970, lt=2025, default=None)
    cm3: int | None = Field(gt=0, lt=5000, default=None)
    km: int | None = Field(gt=0, lt=500 * 1000, default=None)
    price: int | None = Field(gt=0, lt=100 * 1000, default=None)

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


class CarCollection(BaseModel):
    """
    A container holding a list of cars
    """

    cars: List[CarModel]


class CarCollectionPagination(CarCollection):
    page: int = Field(ge=1, default=1)
    has_more: bool
