import pytest

from retry_ops.decorators import retry_with_condition, retry, silent_retry_with_default

# Auxiliary function that can fail for testing purposes
def may_fail(counter, max_attempts):
    """
    Simulates a function that fails several times before succeeding.
    """
    if counter['attempt'] < max_attempts:
        counter['attempt'] += 1
        raise ValueError("Simulated error")
    return "Success"


# Tests for the @silent_retry_with_default decorator
def test_silent_retry_with_default_success():
    """
    Verifies that the function is retried correctly and succeeds before exhausting retries.
    """
    counter = {'attempt': 0}
    max_attempts = 2

    @silent_retry_with_default(retries=3, retry_delay=0.1, default_return_value="Fallback", exceptions=(ValueError,))
    def my_function():
        return may_fail(counter, max_attempts)

    result = my_function()
    assert result == "Success"
    assert counter['attempt'] == max_attempts


def test_silent_retry_with_default_fallback():
    """
    Verifies that the default value is returned when the maximum retry attempts are exceeded.
    """
    counter = {'attempt': 0}
    max_attempts = 4  # More than the available retries

    @silent_retry_with_default(retries=3, retry_delay=0.1, default_return_value="Fallback", exceptions=(ValueError,))
    def my_function():
        return may_fail(counter, max_attempts)

    result = my_function()
    assert result == "Fallback"
    assert counter['attempt'] == 3  # Should have been retried the maximum number of times


def test_retry_success_on_first_attempt():
    """
    Prueba que la función tenga éxito en el primer intento sin reintentos.
    """
    @retry_with_condition(retries=3, retry_delay=1)
    def success_func():
        return "Success"

    assert success_func() == "Success"

