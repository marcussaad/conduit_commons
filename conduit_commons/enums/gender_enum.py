from enum import Enum

import strawberry


@strawberry.enum
class GenderEnum(Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"

    @staticmethod
    def as_dict():
        return {gender.name: gender.value for gender in GenderEnum}
