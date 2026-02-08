from typing import Annotated

from pydantic import BaseModel, BeforeValidator, Field

PyObjectId = Annotated[str, BeforeValidator(str)]


class UserModel(BaseModel):
    id: PyObjectId | None = Field(alias="_id", default=None)
    username: str = Field(..., min_length=3, max_length=15)
    password: str = Field(...)


class LoginModel(BaseModel):
    username: str = Field(...)
    password: str = Field(...)


class CurrentUserModel(BaseModel):
    id: PyObjectId | None = Field(alias="_id", default=None)
    username: str = Field(..., min_length=3, max_length=15)
