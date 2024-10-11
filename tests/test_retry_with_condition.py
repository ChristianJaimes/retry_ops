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
