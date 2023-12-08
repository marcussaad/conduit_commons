import itertools
import logging

import redis
import sqlalchemy
from mysql.connector import errorcode
from pymongo.errors import BulkWriteError
from strawberry.field import StrawberryField

from conduit_commons.authentication.auth0_m2m_authentication import Auth0M2MAuthentication
from conduit_commons.authentication.organization_vault import OrganizationVault
from conduit_commons.authentication.user_vault import UserVault
from conduit_commons.graphql.errors import (
    DuplicateRecordError,
    IntegrityConstraintError,
    DatabaseError,
)

REQUESTS_LOGGER = logging.getLogger("Commons - Do Mutation")


async def do_mutation(fn, *args, **kwargs):
    if not callable(fn):
        raise TypeError("fn is not callable")
    try:
        return await fn(*args, **kwargs)
    except sqlalchemy.exc.IntegrityError as integrity_error:
        REQUESTS_LOGGER.error(integrity_error.orig.msg)
        if integrity_error.orig.args[0] == errorcode.ER_DUP_ENTRY:
            raise DuplicateRecordError(msg=integrity_error.orig.msg)
        elif integrity_error.orig.args[0] in [
            errorcode.ER_ROW_IS_REFERENCED_2,
            errorcode.ER_NO_REFERENCED_ROW_2,
        ]:
            raise IntegrityConstraintError(msg=integrity_error.orig.msg)
    except sqlalchemy.exc.DatabaseError as database_error:
        REQUESTS_LOGGER.error(database_error.orig.msg)
        raise DatabaseError(msg=database_error.orig.msg)
    except sqlalchemy.exc.SQLAlchemyError as generic_sqlalchemy_exc:
        REQUESTS_LOGGER.error(generic_sqlalchemy_exc.args[0])
        raise Exception
    except BulkWriteError as mongo_bulk_error:
        REQUESTS_LOGGER.error(mongo_bulk_error.args[0])
        raise DuplicateRecordError(msg=mongo_bulk_error.details["writeErrors"][0]["errmsg"])


class ValidatedInput(StrawberryField):
    def get_result(self, source, info, args, kwargs):
        validators = []

        def validate_input_recursively(input_val, validations=[]):
            validations.append(input_val)
            for field in input_val.__dict__.values():
                if getattr(field, "_type_definition", False) and field._type_definition.is_input:
                    validate_input_recursively(field, validations)
            return validations

        for _, value in kwargs.items():
            if hasattr(value, "_type_definition") and value._type_definition.is_input:
                validators.append(validate_input_recursively(value))

        validators = list(itertools.chain.from_iterable(validators))
        try:
            info.context["errors"] = list(
                itertools.chain.from_iterable(map(lambda input_object: input_object.validate(), validators))
            )
        except NotImplementedError:
            raise NotImplementedError("Your Input does not implement a validate function")

        return super().get_result(source, info, args, kwargs)


def get_user_vault(
    auth0_m2m_client_id, auth0_m2m_client_secret, auth0_domain, redis_address, redis_port, cryptography_keys
):
    auth0_m2m_conn = None

    if auth0_m2m_client_id and auth0_m2m_client_secret:
        auth0_m2m_conn = Auth0M2MAuthentication(
            domain=auth0_domain,
            client_id=auth0_m2m_client_id,
            client_secret=auth0_m2m_client_secret,
        )

    redis_conn = redis.Redis.from_url(f"redis://{redis_address}:{redis_port}", encoding="utf-8")

    if all([auth0_m2m_conn, redis_conn.ping()]):
        return UserVault(
            redis_connection=redis_conn, auth0_m2m_connection=auth0_m2m_conn, cryptography_keys=cryptography_keys
        )
    else:
        return None


def get_organization_vault(redis_address, redis_port, cryptography_keys):
    redis_conn = redis.Redis.from_url(f"redis://{redis_address}:{redis_port}", encoding="utf-8")
    return OrganizationVault(redis_connection=redis_conn, cryptography_keys=cryptography_keys)
