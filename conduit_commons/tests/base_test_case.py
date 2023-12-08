import pytest
from unittest import TestCase


@pytest.mark.usefixtures("monkeypatch")
class BaseTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.monkeypatch = pytest.MonkeyPatch()

    def setUp(self, *args, **kwargs) -> None:
        print(f" {self.shortDescription()}")
        if kwargs.get("db_path"):
            self.monkeypatch.setattr(kwargs.get("db_path"), lambda: kwargs.get("db_fixture"))
