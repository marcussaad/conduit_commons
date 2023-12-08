from cryptography.fernet import Fernet, MultiFernet


class OrganizationVault:

    REDIS_KEY = "authorization:organization:"

    def __init__(self, *args, **kwargs):
        self.redis_connection = kwargs.get("redis_connection")
        self.cryptography_keys = kwargs.get("cryptography_keys")
        self.encryption = None

        if not all([self.redis_connection, self.cryptography_keys]):
            raise Exception("Missing redis connection")
        self.init_cyphers()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(OrganizationVault, cls).__new__(cls)
        return cls.instance

    def init_cyphers(self):
        if len(self.cryptography_keys) == 2:
            self.encryption = MultiFernet([Fernet(self.cryptography_keys[0]), Fernet(self.cryptography_keys[1])])
        else:
            self.encryption = Fernet(self.cryptography_keys[0])

    def get_organization_by_id(self, org_id: int):
        org = self.redis_connection.get(self.REDIS_KEY + str(org_id))
        if org:
            return self.encryption.decrypt(org).decode("utf-8")
        return None

    def set_organization(self, org_id: int, org):
        self.redis_connection.set(self.REDIS_KEY + str(org_id), self.encryption.encrypt(bytes(org, "UTF-8")))

    def remove_organization_by_id(self, org_id: int):
        return self.redis_connection.delete(self.REDIS_KEY + str(org_id))
