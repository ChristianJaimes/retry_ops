from unittest.mock import Mock
import pytest


@pytest.fixture(autouse=True)
def mock_sleep(monkeypatch):
    sleeper = Mock()
    monkeypatch.setattr('retry_ops.decorators.sleep', sleeper)
    return sleeper
