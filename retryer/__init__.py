from time import sleep

def retry(retries=3, retry_delay=2, exceptions=(Exception,), error_message="Max retries exceeded"):
    """
    A decorator that retries a function if specified exceptions are raised during its execution.

    The decorated function will be retried up to 'retries' times with a 'delay' in seconds between each attempt.
    Only the exceptions specified in the 'exceptions' tuple will trigger a retry. If the function raises an
    exception not included in 'exceptions', it will not be retried and the exception will be propagated immediately.

    Args:
        retries (int): The maximum number of retry attempts. Default is 3.
        retry_delay (int): The delay in seconds between retry attempts. Default is 2.
        exceptions (tuple): A tuple of exception classes that will trigger a retry. Default is (Exception,).
        error_message (str): The error message to be raised when the retry attempts are exceeded. Default is
                             "Max retries exceeded".

    Raises:
        Exception: If the number of retries is exceeded, an Exception with the provided 'error_message' is raised.

    Usage:
        @retry(retries=5, retry_delay=10, exceptions=(MyCustomError,), error_message="Custom error message")
        def my_function():
            # Function implementation that may raise MyCustomError.
            pass
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            nonlocal retries, retry_delay, exceptions, error_message
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    print(f"Error: {e}. Retry {attempt + 1} of {retries}")
                    print(f"Retrying in {retry_delay} seconds...")
                    sleep(retry_delay)
            raise Exception(error_message)
        return wrapper
    return decorator

def silent_retry_with_default( retries=3, retry_delay=2,default_return_value=None, exceptions=(Exception,), error_message="Max retries exceeded"):
    """
    A decorator that silently retries a function if specified exceptions are raised during its execution.
    If the retries are exceeded, it logs an error message and returns a default value instead of raising an exception.

    Args:
        default_return_value (any): The value to return if the retries are exceeded. Default is None.
        retries (int): The maximum number of retry attempts. Default is 3.
        retry_delay (int): The delay in seconds between retry attempts. Default is 2.
        exceptions (tuple): A tuple of exception classes that will trigger a retry. Default is (Exception,).
        error_message (str): The error message to be logged when the retry attempts are exceeded. Default is
                             "Max retries exceeded".

    Returns:
        A wrapper function that includes the retry logic and returns the default value if retries are exceeded.

    Usage:
        @silent_retry_with_default(default_return_value=-1, retries=5, retry_delay=10, exceptions=(MyCustomError,), error_message="Custom error message")
        def my_function():
            # Function implementation that may raise MyCustomError.
            pass
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    print(f"Error: {e}. Retry {attempt + 1} of {retries}")
                    sleep(retry_delay)
            print(error_message)
            return default_return_value
        return wrapper
    return decorator
