from enum import Enum

import strawberry


@strawberry.enum
class InsuranceEligibilityStatusEnum(Enum):
    VALID = "VALID"
    INVALID = "INVALID"
    UNCHECKED = "UNCHECKED"
