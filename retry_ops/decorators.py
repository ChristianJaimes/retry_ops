from time import sleep
from functools import wraps


def retry(retries=3, retry_delay=2, exceptions=(Exception,), error_message="Max retries exceeded"):
    """
    A decorator that retries a function if specific exceptions are raised during its execution.

    Args:
        retries (int): Maximum number of attempts. Default is 3.
        retry_delay (int): Time in seconds between attempts. Default is 2.
        exceptions (tuple): Exceptions that trigger a retry. Default is (Exception,).
        error_message (str): Error message if the maximum retries are exceeded.

    Raises:
        Exception: If the number of retries is exceeded.

    Returns:
        any: The result of the decorated function.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    print(f"Error: {e}. Attempt {attempt + 1} of {retries}")
                    print(f"Retrying in {retry_delay} seconds...")
                    sleep(retry_delay)
            raise Exception(error_message)
        return wrapper
    return decorator


def silent_retry_with_default(retries=3, retry_delay=2, default_return_value=None,
                              exceptions=(Exception,), error_message="Max retries exceeded"):
    """
    A decorator that silently retries a function and returns a default value if it fails.

    Args:
        retries (int): Maximum number of attempts. Default is 3.
        retry_delay (int): Time in seconds between attempts. Default is 2.
        default_return_value (any): Value to return if the maximum retries are exceeded.
        exceptions (tuple): Exceptions that trigger a retry.
        error_message (str): Error message if the maximum retries are exceeded.

    Returns:
        any: The result of the decorated function or the default value.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    print(f"Error: {e}. Attempt {attempt + 1} of {retries}")
                    sleep(retry_delay)
            print(error_message)
            return default_return_value
        return wrapper
    return decorator
