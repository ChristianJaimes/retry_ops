# Retryer

Retryer is a Python library designed to simplify the creation of retry decorators. With Retryer, you can effortlessly add retry logic to your functions, helping them handle transient errors more gracefully.

## Features

- **Easy to use**: Apply retry logic with minimal code changes.
- **Configurable**: Customize the number of retries, delay between retries, and more.
- **Flexible**: Use with any Python function.
```sh
pip install retryer
```
## Usage

To use Retryer, you simply need to import it and apply the retry decorator to the function you want to wrap. Here is an example:

```python
from retryer import retry

# Simple usage with default settings
@retry
def my_function():
    # Function logic that may fail
    print("Attempting the operation...")
    raise ValueError("An error occurred!")
```

## Parameters

The `@retry` decorator accepts the following parameters:

- **attempts** (int): The number of retry attempts. Default is `3`.
- **delay** (int or float): The delay (in seconds) between retry attempts. Default is `1`.

## Contributing

We welcome contributions! Please submit a pull request or open an issue to help improve Retryer.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements

This library was inspired by the need for simple and configurable retry logic in Python functions.
