import pytest
from retryer import retry, silent_retry_with_default

# Función auxiliar que puede fallar para las pruebas
def may_fail(counter, max_attempts):
    """
    Simula una función que falla varias veces antes de tener éxito.
    """
    if counter['attempt'] < max_attempts:
        counter['attempt'] += 1
        raise ValueError("Error simulado")
    return "Success"

# Pruebas para el decorador @retry
def test_retry_success():
    """
    Verifica que la función se reintenta correctamente y tiene éxito antes de agotar los reintentos.
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
    Verifica que se lanza una excepción cuando se exceden los intentos máximos.
    """
    counter = {'attempt': 0}
    max_attempts = 4  # Más de los reintentos disponibles

    @retry(retries=3, retry_delay=0.1, exceptions=(ValueError,))
    def my_function():
        return may_fail(counter, max_attempts)

    with pytest.raises(Exception, match="Max retries exceeded"):
        my_function()
    assert counter['attempt'] == 3  # Debería haberse reintentado el número máximo de veces


def test_retry_handles_different_exception():
    """
    Verifica que no se reintenta si se lanza una excepción que no está en el conjunto de excepciones.
    """
    counter = {'attempt': 0}

    @retry(retries=3, retry_delay=0.1, exceptions=(TypeError,))
    def my_function():
        return may_fail(counter, 2)

    with pytest.raises(ValueError):
        my_function()
    assert counter['attempt'] == 1  # Solo se debe ejecutar una vez ya que la excepción no coincide


# Pruebas para el decorador @silent_retry_with_default
def test_silent_retry_with_default_success():
    """
    Verifica que la función se reintenta correctamente y tiene éxito antes de agotar los reintentos.
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
    Verifica que se devuelve el valor por defecto cuando se exceden los intentos máximos.
    """
    counter = {'attempt': 0}
    max_attempts = 4  # Más de los reintentos disponibles

    @silent_retry_with_default(retries=3, retry_delay=0.1, default_return_value="Fallback", exceptions=(ValueError,))
    def my_function():
        return may_fail(counter, max_attempts)

    result = my_function()
    assert result == "Fallback"
    assert counter['attempt'] == 3  # Debería haberse reintentado el número máximo de veces
