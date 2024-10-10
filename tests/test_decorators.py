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

def test_retry_success_on_first_attempt():
    """
    Prueba que la función tenga éxito en el primer intento sin reintentos.
    """
    @retry_with_condition(retries=3, retry_delay=1)
    def success_func():
        return "Success"

    assert success_func() == "Success"


def test_retry_with_exception():
    """
    Prueba que la función reintente si se lanza una excepción y tenga éxito en un reintento.
    """
    attempt = 0

    @retry_with_condition(retries=3, retry_delay=1, exceptions=(ValueError,))
    def exception_func():
        nonlocal attempt
        attempt += 1
        if attempt < 2:
            raise ValueError("Simulated error")
        return "Success on retry"

    assert exception_func() == "Success on retry"
    assert attempt == 2  # Se debe haber intentado dos veces


def test_retry_exceeding_attempts():
    """
    Prueba que la función retorne el valor por defecto cuando se exceden los reintentos.
    """
    attempt = 0

    @retry_with_condition(retries=3, retry_delay=1, default_return_value="Failed")
    def fail_func():
        nonlocal attempt
        attempt += 1
        raise ValueError("Simulated error")

    assert fail_func() == "Failed"
    assert attempt == 3  # Se deben haber agotado los 3 intentos


def test_retry_with_condition():
    """
    Prueba que la función reintente cuando la condición se cumple.
    """
    attempt = 0

    @retry_with_condition(retries=3, retry_delay=1, conditional=lambda result: result == "Retry")
    def conditional_func():
        nonlocal attempt
        attempt += 1
        if attempt < 2:
            return "Retry"
        return "Success"

    assert conditional_func() == "Success"
    assert attempt == 2  # Se debe haber intentado dos veces


def test_no_retry_when_condition_not_met():
    """
    Prueba que no se realicen reintentos si la condición no se cumple.
    """
    attempt = 0

    @retry_with_condition(retries=3, retry_delay=1, conditional=lambda result: result == "No Retry")
    def no_retry_func():
        nonlocal attempt
        attempt += 1
        return "Success"

    assert no_retry_func() == "Success"
    assert attempt == 1  # Solo un intento, no se debe haber reintentado


def test_retry_on_condition_and_exception():
    """
    Prueba que se realicen reintentos tanto por condición como por excepción.
    """
    attempt = 0

    @retry_with_condition(retries=4, retry_delay=1, conditional=lambda result: result == "Retry", exceptions=(ValueError,))
    def combined_func():
        nonlocal attempt
        attempt += 1
        if attempt == 1:
            return "Retry"  # Esto debería desencadenar un reintento
        elif attempt == 2:
            raise ValueError("Simulated error")  # Esto también desencadena un reintento
        return "Success"

    assert combined_func() == "Success"
    assert attempt == 3  # 1 reintento por la condición, 1 por la excepción    
