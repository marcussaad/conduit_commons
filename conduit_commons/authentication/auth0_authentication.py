import json
from json import JSONDecodeError
from urllib.request import urlopen

from jose import jwt

from conduit_commons.authentication.errors import (
    MissingJWKSUrl,
    JWKSInvalidJSON,
    NoKeysFoundInJWKS,
    NoKeyMatch,
    MissingIssuer,
    MissingAudience,
    MissingValidJWT,
    InvalidJWTToken,
    InvalidJWTAlgorithm,
    ExpiredToken,
    InvalidClaims,
    InvalidToken,
)


class Auth0Authentication(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(Auth0Authentication, cls).__new__(cls)
        return cls.instance

    def __init__(self, *args, **kwargs):
        if not hasattr(self, "keys"):
            self.jwks_url = kwargs.get("jwks_url")
            self.issuer = kwargs.get("issuer")
            self.audience = kwargs.get("audience")
            self.algorithms = ["RS256"]
            self.keys = None

            if not self.jwks_url:
                raise MissingJWKSUrl()

            if not self.issuer:
                raise MissingIssuer()

            if not self.audience:
                raise MissingAudience()

            try:
                self.keys = json.load(urlopen(self.jwks_url)).get("keys")
                self.jwks = {entry["kid"]: entry for entry in self.keys}
            except JSONDecodeError:
                raise JWKSInvalidJSON()
            except ValueError:
                raise NoKeysFoundInJWKS()

    def get_key_by_kid(self, kid):
        return self.jwks.get(kid, None)

    def validate_token(self, token):
        if not token:
            raise MissingValidJWT()

        try:
            unverified_header = jwt.get_unverified_header(token)
            if unverified_header["alg"] not in self.algorithms:
                raise InvalidJWTAlgorithm()

            rsa_key = self.get_key_by_kid(unverified_header["kid"])

            if not rsa_key:
                raise NoKeyMatch()

            return jwt.decode(
                token,
                rsa_key,
                algorithms=self.algorithms,
                issuer=self.issuer,
                audience=self.audience,
                options={"verify_aud": False},
            )

        except jwt.JWTError:
            raise InvalidJWTToken()
        except jwt.ExpiredSignatureError:
            raise ExpiredToken()
        except jwt.JWTClaimsError:
            raise InvalidClaims()
        except Exception:
            raise InvalidToken()
