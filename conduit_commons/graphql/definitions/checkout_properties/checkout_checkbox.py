import typing
import strawberry


@strawberry.type
class CheckoutCheckbox:
    key: strawberry.ID
    type: str = "checkbox"
    display_text: str
    required: bool
    depends_on: typing.Optional[str] = None
    validation_type: typing.Optional[str] = None
    insurance: typing.Optional[str] = None
    state: typing.Optional[str] = None
    category: typing.Optional[str] = None
    subcategory: typing.Optional[str] = None
    condition: typing.Optional[typing.List[int]] = None

    def __init__(self, *args, **kwargs):
        self.key = kwargs.get("key")
        self.display_text = kwargs.get("display_text")
        self.depends_on = kwargs.get("depends_on")
        self.required = kwargs.get("required")
        self.validation_type = kwargs.get("validation_type")
        self.insurance = kwargs.get("insurance")
        self.state = kwargs.get("state")
        self.category = kwargs.get("category")
        self.subcategory = kwargs.get("subcategory")
        self.type = self.type
        self.condition = None

        if kwargs.get("condition", None):
            self.condition = list(map(int, kwargs.get("condition")))
