from unittest import IsolatedAsyncioTestCase
import pytest


@pytest.mark.usefixtures("monkeypatch")
class BaseAsyncTestCase(IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.monkeypatch = pytest.MonkeyPatch()

    def get_async_result(self, coroutine):
        """Run a coroutine synchronously."""
        return self.event_loop.run_until_complete(coroutine)

    async def asyncSetUp(self, *args, **kwargs) -> None:
        print(f" {self.shortDescription()}")
        if kwargs.get("db_path"):
            self.monkeypatch.setattr(kwargs.get("db_path"), lambda: kwargs.get("db_fixture"))
