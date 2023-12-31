from enum import Enum
import strawberry


@strawberry.enum
class OrganizationMembershipStatusEnum(Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
