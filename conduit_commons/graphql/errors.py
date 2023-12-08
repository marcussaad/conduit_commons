import typing

import strawberry


class RecordNotFoundError(Exception):
    def __init__(self, msg=None, *args, **kwargs):
        self.msg = msg or "Record does not exist"
        super().__init__(*args, **kwargs)


class DuplicateRecordError(Exception):
    def __init__(self, msg=None, *args, **kwargs):
        self.msg = msg or "Record already exists"
        super().__init__(*args, **kwargs)


class IntegrityConstraintError(Exception):
    def __init__(self, msg=None, *args, **kwargs):
        self.msg = msg or "Operation violates referential integrity constraint"
        super().__init__(*args, **kwargs)


class DatabaseError(Exception):
    def __init__(self, msg=None, *args, **kwargs):
        self.msg = msg or "Database Error"
        super().__init__(*args, **kwargs)


class InputValidationError(Exception):
    def __init__(self, errors=[], *args, **kwargs):
        self.msg = kwargs.get("msg") or "The input is invalid. See attached errors"
        self.errors = errors
        super().__init__()


class ErrorInterface:
    message: str

    def __init__(self, values: typing.Optional[typing.List[str]] = []):
        if values:
            self.message = self.message.format(*values)


@strawberry.federation.type(shareable=True)
class AccessDeniedError(ErrorInterface):
    message: str = "You do not have permission to perform this action"


@strawberry.federation.type(shareable=True)
class InvalidStateError(ErrorInterface):
    message: str = "State {} is not a valid option"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


@strawberry.federation.type(shareable=True)
class InvalidZipCodeError(ErrorInterface):
    message: str = "Zip Code is {} invalid"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


@strawberry.federation.type(shareable=True)
class FieldTooShortError(ErrorInterface):
    message: str = "{} is too short"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


@strawberry.federation.type(shareable=True)
class FieldTooLongError(ErrorInterface):
    message: str = "{} is too long"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


@strawberry.federation.type(shareable=True)
class MissingRequiredField(ErrorInterface):
    message: str = "Required field {} are missing"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


@strawberry.federation.type(shareable=True)
class InvalidPhoneNumber(ErrorInterface):
    message: str = "Phone number {} is invalid."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


@strawberry.federation.type(shareable=True)
class InvalidEmail(ErrorInterface):
    message: str = "{} is an invalid email"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


@strawberry.federation.type(shareable=True)
class InsufficientPermission(ErrorInterface):
    message: str = "You do not have sufficient permissions to execute this"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


@strawberry.federation.type(shareable=True)
class FileSizeTooLongError(ErrorInterface):
    message: str = "file {} size is too long"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


@strawberry.federation.type(shareable=True)
class WrongFileExtensionError(ErrorInterface):
    message: str = "file {} have a bad extension"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


@strawberry.federation.type(shareable=True)
class FileNameError(ErrorInterface):
    message: str = "{} is invalid"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
