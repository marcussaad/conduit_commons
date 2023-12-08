from datetime import datetime
from typing import Optional

from conduit_auth.roles.roles import Roles
from pydantic import BaseModel

from conduit_commons.enums.organization_membership_status_enum import OrganizationMembershipStatusEnum
from conduit_commons.graphql.constants import DEFAULT_ORGLESS_ID


class AuthUser(BaseModel):

    given_name: Optional[str] = None
    family_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    picture: Optional[str] = None
    nickname: Optional[str] = None
    updated_at: Optional[datetime] = None
    email_verified: Optional[bool] = None
    locale: Optional[str] = None
    user_id: Optional[str] = None

    iss: Optional[str] = None
    aud: Optional[str] = None
    iat: Optional[str] = None
    exp: Optional[str] = None
    sid: Optional[str] = None
    sub: Optional[str] = None

    auth_time: Optional[int] = None

    user_metadata: Optional[dict] = {}
    app_metadata: Optional[dict] = {}

    impersonated_by: Optional["AuthUser"] = None

    def id(self):
        return self.user_id or self.sub or None

    def organization(self):
        return self.app_metadata.get("organization", {})

    def organization_status(self):
        return self.organization().get("status", None)

    def organization_name(self):
        org_name = self.organization().get("name", None)
        org_status = self.organization_status()

        if org_status:
            if org_status == OrganizationMembershipStatusEnum.ACCEPTED.value:
                return org_name
        return None

    def organization_id(self):
        org_id = self.organization().get("organization_id", None)
        org_status = self.organization_status()

        if org_status:
            if org_status == OrganizationMembershipStatusEnum.ACCEPTED.value:
                return org_id
        return DEFAULT_ORGLESS_ID

    def role(self):
        user_role = self.app_metadata.get("role", None)
        if user_role not in [role.value for role in Roles]:
            return None
        return Roles.get_by_name(name=user_role)

    def supplier_id(self):
        if self.role() == Roles.SupplierRole:
            return self.organization().get("supplier_id", None)
        return None

    def supplier_access_limited_to(self):
        # Only marketplace users can have their supplier access limited
        if self.role() == Roles.MarketplaceUserRole:
            return self.app_metadata.get("supplier_access_limited_to", [])
        return []

    def to_auth0_update(self):
        user_metadata = dict.copy(self.user_metadata)
        # causes these values to be removed from the metadata
        user_metadata.update(
            {
                "first_name": None,
                "last_name": None,
                "role": None,
            }
        )
        return {
            "family_name": self.family_name,
            "given_name": self.given_name,
            "user_metadata": user_metadata,
            "app_metadata": self.app_metadata,
        }

    def impersonator(self):
        if self.impersonated_by and self.impersonated_by.role() == Roles.SystemAdministratorRole:
            return self.impersonated_by
        return None

    def set_impersonator(self, impersonator: "AuthUser"):
        if self.role() != Roles.SystemAdministratorRole and impersonator.role() == Roles.SystemAdministratorRole:
            self.impersonated_by = impersonator
        else:
            self.impersonated_by = None
