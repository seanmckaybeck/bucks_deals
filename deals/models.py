import typing

import pydantic


class UnapprovedItem(pydantic.BaseModel):
    key: typing.Optional[str] = None
    ebay_id: int


class Item(pydantic.BaseModel):
    key: typing.Optional[str] = None
    ebay_id: int
    name: str
    price: float
    weight: float
    metal: str
    picture_url: str
    reported = False
    available = True
    quantity = 0
    seller: str


class Spot(pydantic.BaseModel):
    key: typing.Optional[str] = None
    name: str
    value: float
