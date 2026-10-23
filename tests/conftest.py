"""Shared fixtures that make retry tests deterministic and fast."""

from unittest.mock import Mock
import pytest


@pytest.fixture(autouse=True)
def mock_sleep(monkeypatch):
    """Replace retry sleeps with a mock and return it for delay assertions."""
    sleeper = Mock()
    monkeypatch.setattr('retry_ops.decorators.sleep', sleeper)
    return sleeper
