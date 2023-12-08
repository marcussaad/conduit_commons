from typing import Optional, List, Set, Union
from auth0 import Auth0Error
from cryptography.fernet import Fernet, MultiFernet

from conduit_commons.authentication.auth_user import AuthUser
from pydantic import parse_raw_as, parse_obj_as

from conduit_commons.enums.organization_membership_status_enum import OrganizationMembershipStatusEnum


class UserVault:

    REDIS_KEY = "authorization:user:"

    def __init__(self, *args, **kwargs):
        self.redis_connection = kwargs.get("redis_connection")
        self.auth0_m2m_connection = kwargs.get("auth0_m2m_connection")
        self.cryptography_keys = kwargs.get("cryptography_keys")
        self.encryption = None

        if not all([self.redis_connection, self.auth0_m2m_connection, self.cryptography_keys]):
            raise Exception("Missing redis or auth0 connection")
        self.init_cyphers()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(UserVault, cls).__new__(cls)
        return cls.instance

    def init_cyphers(self):
        if len(self.cryptography_keys) == 2:
            self.encryption = MultiFernet([Fernet(self.cryptography_keys[0]), Fernet(self.cryptography_keys[1])])
        else:
            self.encryption = Fernet(self.cryptography_keys[0])

    def __get_auth0_m2m_client(self):
        return self.auth0_m2m_connection.get_management_client()

    def get_user(self, user_id: str) -> Optional[AuthUser]:
        user = self.redis_connection.get(self.REDIS_KEY + user_id)
        user = parse_raw_as(AuthUser, self.encryption.decrypt(user)) if user else None
        if user and user.app_metadata:
            return user
        else:
            try:
                user_response = self.__get_auth0_m2m_client().users.get(user_id)
                if user_response:
                    user = parse_obj_as(AuthUser, user_response)
                    self.set_user(user)
                    return user
                return None
            except Auth0Error:
                return None

    # This method may return None for users that were not found
    def get_users(self, user_ids: Set[str]) -> Optional[List[AuthUser]]:
        users_from_cache = self.redis_connection.mget(keys=user_ids)
        user_id_to_auth_user_map = dict((user_id, auth_user) for user_id, auth_user in zip(user_ids, users_from_cache))
        if all(user_id_to_auth_user_map.values()):
            return user_id_to_auth_user_map
        else:
            try:
                # Query auth0 for the missing ids
                missing_ids = set(
                    user_id for user_id, auth_user in user_id_to_auth_user_map.items() if auth_user is None
                )
                search_response = self.__get_auth0_m2m_client().users.list(
                    per_page=50, q=f'user_id:({" ".join(missing_ids)})'
                )
                if search_response["users"]:
                    for user in search_response["users"]:
                        # parse the object
                        parsed_user = parse_obj_as(AuthUser, user)
                        # add to the mapping of users we'll return
                        user_id_to_auth_user_map[user["user_id"]] = parsed_user
                        # update the missing ids set so that we know which ones were found
                        missing_ids.remove(parsed_user.id())
                        # set it in the cache
                        self.set_user(parsed_user)

                    # Mark which users were not found
                    for id_not_found in missing_ids:
                        user_id_to_auth_user_map[id_not_found] = None
            except Auth0Error:
                pass
            finally:
                return user_id_to_auth_user_map

    def set_user(self, user: AuthUser):
        if user.exp:
            self.redis_connection.set(
                self.REDIS_KEY + user.id(), self.encryption.encrypt(bytes(user.json(), "utf-8"), ex=int(user.exp))
            )
        else:
            self.redis_connection.set(self.REDIS_KEY + user.id(), self.encryption.encrypt(bytes(user.json(), "utf-8")))

    def update_user(self, user: AuthUser):
        try:
            self.__get_auth0_m2m_client().users.update(user.id(), user.to_auth0_update())
            self.set_user(user)
        except Auth0Error:
            pass

    def remove_user(self, user: AuthUser):
        return self.redis_connection.delete(self.REDIS_KEY + user.id())

    def get_organization_users(self, organization_id: int, status: Union[OrganizationMembershipStatusEnum]):
        users, page, per_page, found_all = [], 0, 50, False

        while not found_all:
            search_response = self.__get_auth0_m2m_client().users.list(
                page=page,
                per_page=per_page,
                q=f"app_metadata.organization.organization_id: {organization_id} AND "
                f"app_metadata.organization.status: {status.value}",
            )

            if search_response["users"]:
                for user in search_response["users"]:
                    users.append(parse_obj_as(AuthUser, user))

            if search_response["total"] <= page * per_page:
                found_all = True

            page += 1
        return users
