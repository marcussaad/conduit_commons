import datetime
import auth0
from auth0.management import Auth0

from conduit_commons.authentication.errors import (
    MissingDomain,
    MissingClientId,
    MissingClientSecret,
    InvalidAuth0M2MConfiguration,
    RateLimitedAuth0M2M,
)
from auth0.authentication import GetToken


class Auth0M2MAuthentication(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(Auth0M2MAuthentication, cls).__new__(cls)
        return cls.instance

    def __init__(self, *args, **kwargs):
        self.management_api_token = None
        self.domain = kwargs.get("domain")
        self.client_id = kwargs.get("client_id")
        self.client_secret = kwargs.get("client_secret")

        if not self.domain:
            raise MissingDomain()

        if not self.client_id:
            raise MissingClientId()

        if not self.client_secret:
            raise MissingClientSecret()

        self.get_token = GetToken(self.domain, self.client_id, self.client_secret)

    def get_management_api_token(self):
        if self.management_api_token is None or (
            self.management_api_token and datetime.datetime.now() > self.management_api_token["expires_on"]
        ):
            try:
                token = self.get_token.client_credentials("https://{}/api/v2/".format(self.domain))
                self.management_api_token = {
                    "token": token["access_token"],
                    "expires_on": datetime.datetime.now() + datetime.timedelta(seconds=token["expires_in"]),
                }
                return self.management_api_token
            except auth0.Auth0Error as e:
                self.management_api_token = None
                raise InvalidAuth0M2MConfiguration(msg=e.message)
            except auth0.RateLimitError as e:
                self.management_api_token = None
                raise RateLimitedAuth0M2M(msg=e.message)
            finally:
                return self.management_api_token
        return self.management_api_token

    def get_management_client(self):
        token = self.get_management_api_token()
        if token and token["token"]:
            return Auth0(domain=self.domain, token=token["token"])
        return None
