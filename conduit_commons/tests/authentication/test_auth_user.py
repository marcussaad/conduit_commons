from unittest import TestCase

from conduit_auth.roles.roles import Roles

from conduit_commons.authentication.auth_user import AuthUser
from conduit_commons.enums.organization_membership_status_enum import OrganizationMembershipStatusEnum


class AuthUserTestCase(TestCase):
    def test_id_method_with_user(self):
        user = AuthUser(user_id="auth|3123")
        self.assertEqual(user.id(), "auth|3123")

    def test_id_method_with_sub(self):
        user = AuthUser(sub="auth|1234")
        self.assertEqual(user.id(), "auth|1234")

    def test_id_method_with_empty_user(self):
        user = AuthUser()
        self.assertIsNone(user.id())

    def test_id_method_with_both_id_and_sub(self):
        user = AuthUser(user_id="auth|321", sub="auth|123")
        self.assertEqual(user.id(), "auth|321")

    def test_id_method_with_both_id(self):
        user = AuthUser(user_id=None, sub="auth|123")
        self.assertEqual(user.id(), "auth|123")

    def test_user_organization_with_organization(self):
        user = AuthUser(app_metadata={"organization": "conduit"})
        self.assertEqual(user.organization(), "conduit")

    def test_organization_with_empty_organization(self):
        user = AuthUser(app_metadata={"organization": None})
        self.assertIsNone(user.organization())

    def test_user_organization_without_organization(self):
        user = AuthUser(app_metadata={})
        self.assertEqual(user.organization(), {})

    def test_organization_with_empty_app_metadata(self):
        user = AuthUser()
        self.assertEqual(user.organization(), {})

    def test_organization_id_accepted(self):
        user = AuthUser(
            app_metadata={
                "organization": {
                    "organization_id": "org|123",
                    "status": OrganizationMembershipStatusEnum.ACCEPTED.value,
                }
            }
        )
        self.assertEqual(user.organization_id(), "org|123")

    def test_organization_id_pending(self):
        user = AuthUser(
            app_metadata={
                "organization": {"organization_id": None, "status": OrganizationMembershipStatusEnum.ACCEPTED.value}
            }
        )
        self.assertIsNone(user.organization_id())

    def test_organization_id_no_status(self):
        user = AuthUser(app_metadata={"organization": {"organization_id": "org123", "status": None}})
        self.assertEqual(user.organization_id(), 0)

    def test_organization_status_with_status(self):
        user = AuthUser(app_metadata={"organization": {"status": "ACCEPTED"}})
        self.assertEqual(user.organization_status(), "ACCEPTED")

    def test_organization_status_no_organization_metadata(self):
        user = AuthUser()
        self.assertIsNone(user.organization_status())

    def test_organization_name_with_name(self):
        user = AuthUser(app_metadata={"organization": {"name": "conduit", "status": "ACCEPTED"}})
        self.assertEqual(user.organization_name(), "conduit")

    def test_organization_name_no_organization_metadata(self):
        user = AuthUser()
        self.assertIsNone(user.organization_name())

    def test_role_valid(self):
        user = AuthUser(app_metadata={"role": Roles.SupplierRole.value})
        self.assertEqual(user.role(), Roles.SupplierRole)

    def test_role_invalid(self):
        user = AuthUser(app_metadata={"role": "invalid_role"})
        self.assertIsNone(user.role())

    def test_role_missing(self):
        user = AuthUser()
        self.assertIsNone(user.role())

    def test_supplier_id_with_supplier_role(self):
        user = AuthUser(app_metadata={"role": Roles.SupplierRole.value, "organization": {"supplier_id": "sup|123"}})
        self.assertEqual(user.supplier_id(), "sup|123")

    def test_supplier_id_with_marketplace_role(self):
        user = AuthUser(
            app_metadata={"role": Roles.MarketplaceUserRole.value, "organization": {"supplier_id": "sup|123"}}
        )
        self.assertIsNone(user.supplier_id())

    def test_supplier_id_with_different_role(self):
        user = AuthUser(app_metadata={"role": Roles.SupplierRole.value, "organization": {}})
        self.assertIsNone(user.supplier_id())

    def test_to_auth0_update(self):
        auth_user = AuthUser(
            family_name="Joe",
            given_name="John",
            user_metadata={"age": 30},
            app_metadata={"role": "admin"},
        )

        user = AuthUser(**auth_user.dict())
        user.to_auth0_update()

        self.assertEqual(user.dict(), auth_user.dict())

    def test_to_auth0_update_with_unknown_attr(self):
        auth_user = AuthUser(
            family_name="Joe",
            given_name="John",
            user_metadata={"age": 30},
            app_metadata={"role": "admin"},
        )

        update_with_unknown_attr_result = auth_user.dict()
        update_with_unknown_attr_result["should_be_ignored"] = "some_value"

        user = AuthUser(**update_with_unknown_attr_result)
        user.to_auth0_update()

        self.assertEqual(user.dict(), auth_user.dict())

    def test_to_auth0_update_with_no_properties(self):
        auth_user = AuthUser(
            family_name=None,
            given_name=None,
            user_metadata={},
            app_metadata={},
        )
        user = AuthUser(**auth_user.dict())
        user.to_auth0_update()

        self.assertEqual(user.dict(), auth_user.dict())

    def test_get_user_supplier_access_limited_to(self):
        user = AuthUser(app_metadata={"role": Roles.MarketplaceUserRole.value, "supplier_access_limited_to": [1]})

        self.assertEqual(user.supplier_access_limited_to(), [1])

    def test_get_user_supplier_access_limited_to_as_non_marketplace_user(self):
        user = AuthUser(app_metadata={"role": Roles.SupplierRole.value, "supplier_access_limited_to": [1]})

        self.assertEqual(user.supplier_access_limited_to(), [])

    def test_admin_should_be_able_to_impersonate_non_admin(self):
        admin_user = AuthUser(app_metadata={"role": Roles.SystemAdministratorRole.value})
        marketplace_user = AuthUser(app_metadata={"role": Roles.MarketplaceUserRole.value})
        supplier_user = AuthUser(app_metadata={"role": Roles.SupplierRole.value})

        marketplace_user.set_impersonator(impersonator=admin_user)
        supplier_user.set_impersonator(impersonator=admin_user)
        self.assertEqual(marketplace_user.impersonator(), admin_user)
        self.assertEqual(supplier_user.impersonator(), admin_user)

    def test_admin_should_not_be_able_to_impersonate_admin(self):
        admin_user = AuthUser(app_metadata={"role": Roles.SystemAdministratorRole.value})
        admin_user_2 = AuthUser(app_metadata={"role": Roles.SystemAdministratorRole.value})

        admin_user_2.set_impersonator(impersonator=admin_user)
        self.assertEqual(admin_user_2.impersonator(), None)

    def test_cannot_impersonate_if_not_admin(self):
        marketplace_user = AuthUser(app_metadata={"role": Roles.MarketplaceUserRole.value})
        supplier_user = AuthUser(app_metadata={"role": Roles.SupplierRole.value})

        marketplace_user.set_impersonator(impersonator=supplier_user)
        supplier_user.set_impersonator(impersonator=marketplace_user)
        self.assertEqual(marketplace_user.impersonator(), None)
        self.assertEqual(supplier_user.impersonator(), None)
