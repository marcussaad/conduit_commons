import strawberry

from typing import NewType


JSONValue = strawberry.scalar(
    NewType("JSONValue", object),
    serialize=lambda v: v,
    parse_value=lambda v: v,
)
