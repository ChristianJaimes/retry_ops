[![🐍 Unit Tests 🚦](https://github.com/ChristianJaimes/retry_ops/actions/workflows/main.yml/badge.svg)](https://github.com/ChristianJaimes/retry_ops/actions/workflows/main.yml) ![PyPI - License](https://img.shields.io/pypi/l/retry-ops)
 [![Downloads](https://static.pepy.tech/badge/retry-ops)](https://pepy.tech/project/retry-ops)
# retry-ops

retry_ops is a Python library designed to simplify the creation of retry decorators. With retry_ops, you can effortlessly add retry logic to your functions, helping them handle transient errors more gracefully.

## Features

- **Easy to use**: Apply retry logic with minimal code changes.
- **Configurable**: Customize the number of retries, delay between retries, and more.
- **Flexible**: Use with synchronous Python functions.
```sh
pip install retry-ops
```
## Usage

To use retry_ops, you simply need to import it and apply the retry decorator to the function you want to wrap. Here is an example:

```python
from retry_ops import retry, silent_retry_with_default

# Simple usage with default settings
@retry()
def my_function():
    # Function logic that may fail
    print("Attempting the operation...")
    raise ValueError("An error occurred!")

# Customizing the retry logic
@retry(retries=5, retry_delay=2, exceptions=(IOError, ), error_message="Custom error message")
def my_other_function():
    # Function logic that may fail
    print("Attempting another operation...")
    raise IOError("Another error occurred!")

# Using the silent retry decorator
@silent_retry_with_default(default_return_value=-1, retries=5, retry_delay=3, exceptions=(RuntimeError,), error_message="Operation failed after retries")
def my_silent_function():
    # Function logic that may fail
    print("Attempting the silent operation...")
    raise RuntimeError("A runtime error occurred!")
```
## Parameters

The `@retry` decorator accepts the following parameters:

- **retries** (int): The maximum number of total attempts, including the first call. Default is `3`.
- **retry_delay** (int or float): The delay (in seconds) between retry attempts. Default is `2`.
- **exceptions** (tuple): A tuple of exception classes that will trigger a retry. Default is `(Exception,)`.
- **error_message** (str): The error message to be raised when the retry attempts are exceeded. Default is `"Max retries exceeded"`.

The `@silent_retry_with_default` decorator accepts the following parameters:

- **default_return_value** (any): The value to return if the retries are exceeded. Default is `None`.
- **retries** (int): The maximum number of total attempts, including the first call. Default is `3`.
- **retry_delay** (int or float): The delay (in seconds) between retry attempts. Default is `2`.
- **exceptions** (tuple): A tuple of exception classes that will trigger a retry. Default is `(Exception,)`.
- **error_message** (str): The error message to be logged when the retry attempts are exceeded. Default is `"Max retries exceeded"`.

## Contributing

We welcome contributions! Please submit a pull request or open an issue to help improve retry_ops.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements

This library was inspired by the need for simple and configurable retry logic in Python functions.

## Retry behavior

All decorators require `retries` to be a positive integer and `retry_delay` to
be a finite, non-negative number. `exceptions` must be a tuple of `Exception`
subclasses; an empty tuple disables exception retries. Invalid configuration
raises `TypeError` or `ValueError` when the decorator is created.

There are at most `retries - 1` pauses. `retry` raises `RetryError` on exhaustion,
with the original exception in `error.__cause__`. It remains an `Exception`
subclass. Exceptions outside the configured tuple propagate immediately.

```python
from retry_ops import retry_with_condition

@retry_with_condition(retries=3, retry_delay=0.5,
                      conditional=lambda response: response["status"] == 503,
                      default_return_value={"status": 503})
def fetch_status():
    return {"status": 200}
```

A true condition triggers another attempt; exhaustion returns the fallback.
Errors raised by the condition itself propagate immediately without repeating
an already completed operation. Conditions must be callable or `None`.

These decorators support synchronous functions only, not `async def` functions
or deferred generator execution. Use them for operations that are safe to repeat.
They do not print to stdout. Enable DEBUG logging on `retry_ops.decorators` to
see retry diagnostics; exception details may appear in those logs.

## Development

Install `pip install -e ".[test]"` and run `python -m pytest`.
Tests replace sleep with a mock and check calls and delays without real waiting.
CI also builds an sdist and wheel and tests the installed wheel outside the source tree.
