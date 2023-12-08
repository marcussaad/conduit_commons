import typing
import strawberry


@strawberry.type
class Numeric:
    key: strawberry.ID
    type: str = "numeric"
    display_text: str
    required: bool
    depends_on: typing.Optional[str] = None
    validation_type: typing.Optional[str] = None
    condition: typing.Optional[typing.Union[typing.List[int], None]] = None

    def __init__(self, *args, **kwargs):
        self.key = kwargs.get("key")
        self.display_text = kwargs.get("display_text")
        self.depends_on = kwargs.get("depends_on")
        self.required = kwargs.get("required")
        self.validation_type = kwargs.get("validation_type")
        self.condition = None

        if kwargs.get("condition", None):
            self.condition = list(map(int, kwargs.get("condition")))
