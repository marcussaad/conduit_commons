import boto3
from datetime import datetime
from conduit_commons.aws.errors import MissingRequiredParams


class BaseBotoClient(object):
    """
    This class is a singleton and only supports the creation of a single cliente type at once.
    If you need to have multiple clients in your application at once,
    We'll need to modify this class to support multiple clients.
    """

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(BaseBotoClient, cls).__new__(cls)
        return cls.instance

    def __init__(self, *args, **kwargs):
        self.credentials = None
        self.client = None
        self.aws_access_key_id = kwargs.get("aws_access_key_id")
        self.aws_secret_access_key = kwargs.get("aws_secret_access_key")
        self.aws_role_to_assume = kwargs.get("aws_role_to_assume")
        self.aws_role_session_name = kwargs.get("aws_role_session_name", None)
        self.aws_region_name = kwargs.get("aws_region_name", "us-east-1")
        self.extras = kwargs

        if not all(
            [self.aws_access_key_id, self.aws_secret_access_key, self.aws_role_to_assume, self.aws_role_session_name]
        ):
            raise MissingRequiredParams()

        self.sts_client = boto3.client(
            "sts",
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        )

    def __is_valid_token(self):
        if self.credentials and datetime.astimezone(datetime.now()) < self.credentials["Expiration"]:
            return True
        return False

    def __assume_role(self):
        response = self.sts_client.assume_role(
            RoleArn=self.aws_role_to_assume, RoleSessionName=self.aws_role_session_name
        )

        self.credentials = response["Credentials"]
        return self.credentials

    def get_client_for(self, client_type: str):
        if not self.client or not self.__is_valid_token():
            self.__assume_role()
            self.client = boto3.Session(
                aws_access_key_id=self.credentials["AccessKeyId"],
                aws_secret_access_key=self.credentials["SecretAccessKey"],
                aws_session_token=self.credentials["SessionToken"],
                region_name=self.aws_region_name,
            ).client(client_type)
        else:
            return self.client
