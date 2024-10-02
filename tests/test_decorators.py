import pytest
from sure_retry import retry, silent_retry_with_default

# Auxiliary function that can fail for testing purposes
def may_fail(counter, max_attempts):
    """
    Simulates a function that fails several times before succeeding.
    """
    if counter['attempt'] < max_attempts:
        counter['attempt'] += 1
        raise ValueError("Simulated error")
    return "Success"

# Tests for the @retry decorator
def test_retry_success():
    """
    Verifies that the function is retried correctly and succeeds before exhausting retries.
    """
    counter = {'attempt': 0}
    max_attempts = 2

    @retry(retries=3, retry_delay=0.1, exceptions=(ValueError,))
    def my_function():
        return may_fail(counter, max_attempts)

    result = my_function()
    assert result == "Success"
    assert counter['attempt'] == max_attempts


def test_retry_exceeds_attempts():
    """
    Verifies that an exception is raised when the maximum retry attempts are exceeded.
    """
    counter = {'attempt': 0}
    max_attempts = 4  # More than the available retries

    @retry(retries=3, retry_delay=0.1, exceptions=(ValueError,))
    def my_function():
        return may_fail(counter, max_attempts)

    with pytest.raises(Exception, match="Max retries exceeded"):
        my_function()
    assert counter['attempt'] == 3  # Should have been retried the maximum number of times


def test_retry_handles_different_exception():
    """
    Verifies that no retries occur if an exception is raised that is not in the exception set.
    """
    counter = {'attempt': 0}

    @retry(retries=3, retry_delay=0.1, exceptions=(TypeError,))
    def my_function():
        return may_fail(counter, 2)

    with pytest.raises(ValueError):
        my_function()
    assert counter['attempt'] == 1  # Should only run once as the exception does not match


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
