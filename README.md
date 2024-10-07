[![🐍 Unit Tests 🚦](https://github.com/ChristianJaimes/retry_ops/actions/workflows/main.yml/badge.svg)](https://github.com/ChristianJaimes/retry_ops/actions/workflows/main.yml) ![PyPI - License](https://img.shields.io/pypi/l/retry-ops)
 [![Downloads](https://static.pepy.tech/badge/retry-ops)](https://pepy.tech/project/retry-ops)
# retry-ops

retry_ops is a Python library designed to simplify the creation of retry decorators. With retry_ops, you can effortlessly add retry logic to your functions, helping them handle transient errors more gracefully.

## Features

- **Easy to use**: Apply retry logic with minimal code changes.
- **Configurable**: Customize the number of retries, delay between retries, and more.
- **Flexible**: Use with any Python function.
```sh
pip install retry-ops
```
## Usage

To use retry_ops, you simply need to import it and apply the retry decorator to the function you want to wrap. Here is an example:

```python
from retry_ops import retry, silent_retry_with_default

# Simple usage with default settings
@retry
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

- **retries** (int): The maximum number of retry attempts. Default is `3`.
- **retry_delay** (int or float): The delay (in seconds) between retry attempts. Default is `2`.
- **exceptions** (tuple): A tuple of exception classes that will trigger a retry. Default is `(Exception,)`.
- **error_message** (str): The error message to be raised when the retry attempts are exceeded. Default is `"Max retries exceeded"`.

The `@silent_retry_with_default` decorator accepts the following parameters:

- **default_return_value** (any): The value to return if the retries are exceeded. Default is `None`.
- **retries** (int): The maximum number of retry attempts. Default is `3`.
- **retry_delay** (int or float): The delay (in seconds) between retry attempts. Default is `2`.
- **exceptions** (tuple): A tuple of exception classes that will trigger a retry. Default is `(Exception,)`.
- **error_message** (str): The error message to be logged when the retry attempts are exceeded. Default is `"Max retries exceeded"`.

## Contributing

We welcome contributions! Please submit a pull request or open an issue to help improve retry_ops.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements

This library was inspired by the need for simple and configurable retry logic in Python functions.
