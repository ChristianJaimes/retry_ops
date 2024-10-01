from time import sleep
from functools import wraps


def retry(retries=3, retry_delay=2, exceptions=(Exception,), error_message="Max retries exceeded"):
    """
    Un decorador que reintenta una función si se levantan excepciones específicas durante su ejecución.

    Args:
        retries (int): Número máximo de intentos. Por defecto es 3.
        retry_delay (int): Tiempo en segundos entre intentos. Por defecto es 2.
        exceptions (tuple): Excepciones que desencadenan un reintento. Por defecto es (Exception,).
        error_message (str): Mensaje de error si se exceden los reintentos.

    Raises:
        Exception: Si se excede el número de reintentos.

    Returns:
        any: El resultado de la función decorada.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    print(f"Error: {e}. Intento {attempt + 1} de {retries}")
                    print(f"Reintentando en {retry_delay} segundos...")
                    sleep(retry_delay)
            raise Exception(error_message)
        return wrapper
    return decorator


def silent_retry_with_default(retries=3, retry_delay=2, default_return_value=None,
                              exceptions=(Exception,), error_message="Max retries exceeded"):
    """
    Un decorador que reintenta silenciosamente una función y devuelve un valor por defecto si falla.

    Args:
        retries (int): Número máximo de intentos. Por defecto es 3.
        retry_delay (int): Tiempo en segundos entre intentos. Por defecto es 2.
        default_return_value (any): Valor a devolver si se exceden los reintentos.
        exceptions (tuple): Excepciones que desencadenan un reintento.
        error_message (str): Mensaje de error si se exceden los reintentos.

    Returns:
        any: El resultado de la función decorada o el valor por defecto.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    print(f"Error: {e}. Intento {attempt + 1} de {retries}")
                    sleep(retry_delay)
            print(error_message)
            return default_return_value
        return wrapper
    return decorator
