import strawberry
import typing

from conduit_commons.graphql.errors import ErrorInterface


@strawberry.type
class OutputInterface:
    id: typing.Optional[int]
    record: typing.Optional[strawberry.scalars.JSON]
    status: int
    errors: typing.Optional[typing.List[ErrorInterface]]
