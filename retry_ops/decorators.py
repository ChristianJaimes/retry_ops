"""Retry decorators for synchronous functions."""
import logging
import math
from functools import wraps
from numbers import Real
from time import sleep

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class RetryError(Exception):
    """All attempts failed; the last exception is available as __cause__."""


def _validate(retries, retry_delay, exceptions, conditional=None):
    """Validate retry options before wrapping a function.
    
    Raises:
        TypeError: An option has an unsupported type.
        ValueError: Attempts or delay are outside their valid range."""
    if isinstance(retries, bool) or not isinstance(retries, int):
        raise TypeError("retries must be an integer")
    if retries < 1:
        raise ValueError("retries must be at least 1")
    if isinstance(retry_delay, bool) or not isinstance(retry_delay, Real):
        raise TypeError("retry_delay must be a real number")
    if not math.isfinite(retry_delay) or retry_delay < 0:
        raise ValueError("retry_delay must be finite and non-negative")
    if not isinstance(exceptions, tuple) or any(
        not isinstance(exc, type) or not issubclass(exc, Exception)
        for exc in exceptions
    ):
        raise TypeError("exceptions must be a tuple of Exception subclasses")
    if conditional is not None and not callable(conditional):
        raise TypeError("conditional must be callable or None")


def _decorate(retries, retry_delay, exceptions, error_message,
              default_return_value=None, conditional=None, raise_on_failure=False):
    """Build a decorator with shared retry, fallback, and error handling.
    
    The supplied configuration is validated immediately. Predicate failures
    propagate without retrying. When raise_on_failure is true, exhaustion
    raises RetryError chained to the final matching exception; otherwise it
    returns default_return_value.
    
    Returns:
        callable: A decorator that preserves the wrapped function metadata."""
    _validate(retries, retry_delay, exceptions, conditional)

    def decorator(func):
        """Wrap func with the validated retry policy and preserve its metadata."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            """Forward arguments, retry matching failures, and return or raise on exhaustion."""
            last_exception = None
            for attempt in range(retries):
                try:
                    result = func(*args, **kwargs)
                except exceptions as exc:
                    last_exception = exc
                    logger.debug("Attempt %s of %s failed", attempt + 1, retries,
                                 exc_info=True)
                else:
                    # Predicate errors must propagate without repeating the operation.
                    if conditional is None or not conditional(result):
                        return result
                if attempt + 1 < retries:
                    logger.debug("Retrying in %s seconds", retry_delay)
                    sleep(retry_delay)
            if raise_on_failure:
                raise RetryError(error_message) from last_exception
            logger.debug("%s", error_message)
            return default_return_value
        return wrapper
    return decorator


def retry(retries=3, retry_delay=2, exceptions=(Exception,),
          error_message="Max retries exceeded"):
    """Try a synchronous function up to retries times, then raise RetryError.
    
    retry_delay is the non-negative delay between attempts. Only exceptions
    matching the supplied tuple are retried. Use @retry() with parentheses.
    
    Args:
        retries (int): Maximum total attempts, including the first call.
        retry_delay (float): Finite, non-negative seconds between attempts.
        exceptions (tuple): Exception classes that trigger another attempt.
        error_message (str): Message used when all attempts are exhausted.
    
    Returns:
        callable: A decorator for synchronous functions.
    
    Raises:
        TypeError: Configuration has an unsupported type.
        ValueError: Attempts or delay are outside their valid range.
        RetryError: The wrapped function exhausts all attempts. The last
            matching exception is retained as __cause__.
    """
    return _decorate(retries, retry_delay, exceptions, error_message,
                     raise_on_failure=True)


def silent_retry_with_default(retries=3, retry_delay=2, default_return_value=None,
                              exceptions=(Exception,), error_message="Max retries exceeded"):
    """Try up to retries times, returning the fallback on matching failures.
    
    Args:
        retries (int): Maximum total attempts, including the first call.
        retry_delay (float): Finite, non-negative seconds between attempts.
        exceptions (tuple): Exception classes that trigger another attempt.
        error_message (str): Message used when all attempts are exhausted.
        default_return_value: Value returned after all attempts fail.
    
    Returns:
        callable: A decorator for synchronous functions.
    
    Raises:
        TypeError: Configuration has an unsupported type.
        ValueError: Attempts or delay are outside their valid range.
    """
    return _decorate(retries, retry_delay, exceptions, error_message,
                     default_return_value=default_return_value)


def retry_with_condition(retries=3, retry_delay=2, conditional=None,
                         default_return_value=None, exceptions=(Exception,),
                         error_message="Max retries exceeded"):
    """Retry matching exceptions or results for which conditional returns true.
    
    Return default_return_value after exhaustion. Errors in conditional propagate
    immediately. retries counts total attempts, including the first execution.
    
    Args:
        retries (int): Maximum total attempts, including the first call.
        retry_delay (float): Finite, non-negative seconds between attempts.
        exceptions (tuple): Exception classes that trigger another attempt.
        error_message (str): Message used when all attempts are exhausted.
        default_return_value: Value returned after all attempts fail.
        conditional (callable): Result predicate; true requests a retry.
            None disables result-based retries. Predicate errors propagate.
    
    Returns:
        callable: A decorator for synchronous functions.
    
    Raises:
        TypeError: Configuration has an unsupported type.
        ValueError: Attempts or delay are outside their valid range.
    """
    return _decorate(retries, retry_delay, exceptions, error_message,
                     default_return_value=default_return_value, conditional=conditional)
