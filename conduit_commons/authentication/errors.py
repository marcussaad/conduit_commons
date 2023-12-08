from strawberry.exceptions import StrawberryGraphQLError


class MissingJWKSUrl(Exception):
    def __init__(self, msg=None, *args, **kwargs):
        self.msg = msg or "Missing URL for JWKS"
        super().__init__(msg, *args, **kwargs)


class MissingAudience(Exception):
    def __init__(self, msg=None, *args, **kwargs):
        self.msg = msg or "Missing audience argument"
        super().__init__(msg, *args, **kwargs)


class MissingIssuer(Exception):
    def __init__(self, msg=None, *args, **kwargs):
        self.msg = msg or "Missing issuer argument"
        super().__init__(msg, *args, **kwargs)


class JWKSInvalidJSON(Exception):
    def __init__(self, msg=None, *args, **kwargs):
        self.msg = msg or "The url provided for JWKS does not return a valid json"
        super().__init__(msg, *args, **kwargs)


class NoKeysFoundInJWKS(Exception):
    def __init__(self, msg=None, *args, **kwargs):
        self.msg = msg or "The url provided for JWKS does not return a valid json"
        super().__init__(msg, *args, **kwargs)


class NoKeyMatch(Exception):
    def __init__(self, msg=None, *args, **kwargs):
        self.msg = msg or "The kid does not match a valid jwk"
        super().__init__(msg, *args, **kwargs)


class MissingValidJWT(Exception):
    def __init__(self, msg=None, *args, **kwargs):
        self.msg = msg or "Missing valid JWT"
        super().__init__(msg, *args, **kwargs)


class InvalidJWTToken(Exception):
    def __init__(self, msg=None, *args, **kwargs):
        self.msg = msg or "Could not parse JWT token"
        super().__init__(msg, *args, **kwargs)


class InvalidJWTAlgorithm(Exception):
    def __init__(self, msg=None, *args, **kwargs):
        self.msg = msg or "The algorithm used to encrypt the JWT token is not supported"
        super().__init__(msg, *args, **kwargs)


class ExpiredToken(Exception):
    def __init__(self, msg=None, *args, **kwargs):
        self.msg = msg or "The token is expired"
        super().__init__(msg, *args, **kwargs)


class InvalidClaims(Exception):
    def __init__(self, msg=None, *args, **kwargs):
        self.msg = msg or "The claims are invalid. Please check the audience and issuer"
        super().__init__(msg, *args, **kwargs)


class InvalidToken(Exception):
    def __init__(self, msg=None, *args, **kwargs):
        self.msg = msg or "Token could not be validated"
        super().__init__(msg, *args, **kwargs)


class UnauthorizedRequest(StrawberryGraphQLError):
    def __init__(self, msg=None, *args, **kwargs):
        self.msg = msg or "No authentication headers found"
        super().__init__(msg, *args, **kwargs)


class MissingDomain(Exception):
    def __init__(self, msg=None, *args, **kwargs):
        self.msg = msg or "Missing Domain"
        super().__init__(msg, *args, **kwargs)


class MissingClientId(Exception):
    def __init__(self, msg=None, *args, **kwargs):
        self.msg = msg or "Missing Client ID"
        super().__init__(msg, *args, **kwargs)


class MissingClientSecret(Exception):
    def __init__(self, msg=None, *args, **kwargs):
        self.msg = msg or "Missing Client Secret"
        super().__init__(msg, *args, **kwargs)


class InvalidAuth0M2MConfiguration(Exception):
    def __init__(self, msg=None, *args, **kwargs):
        self.msg = msg or f"Could not retrieve machine to machine token. Error: #{msg}"
        super().__init__(msg, *args, **kwargs)


class RateLimitedAuth0M2M(Exception):
    def __init__(self, msg=None, *args, **kwargs):
        self.msg = msg or f"Too many requests. Error: #{msg}"
        super().__init__(msg, *args, **kwargs)
