from unittest.mock import Mock, call
import pytest
import retry_ops
from retry_ops import RetryError, retry, retry_with_condition, silent_retry_with_default

DECORATORS = [retry, silent_retry_with_default, retry_with_condition]


def test_public_exports():
    namespace = {}
    exec('from retry_ops import *', namespace)
    for name in retry_ops.__all__:
        assert callable(namespace[name])


@pytest.mark.parametrize('decorator', DECORATORS)
@pytest.mark.parametrize('attempts', [1, 3])
def test_exhaustion_and_delays(decorator, attempts, mock_sleep):
    original = ValueError('original')
    operation = Mock(side_effect=original)
    wrapped = decorator(retries=attempts, retry_delay=0.25)(operation)
    if decorator is retry:
        with pytest.raises(RetryError) as caught:
            wrapped()
        assert caught.value.__cause__ is original
    else:
        assert wrapped() is None
    assert operation.call_count == attempts
    assert mock_sleep.call_args_list == [call(0.25)] * (attempts - 1)


@pytest.mark.parametrize('decorator', DECORATORS)
def test_success_and_metadata(decorator, mock_sleep):
    @decorator()
    def operation(value, *, extra=0):
        """Original documentation."""
        return value + extra
    assert operation(2, extra=3) == 5
    assert operation.__name__ == 'operation'
    assert operation.__doc__ == 'Original documentation.'
    assert operation.__wrapped__(2) == 2
    mock_sleep.assert_not_called()


@pytest.mark.parametrize('decorator', DECORATORS)
def test_unmatched_exception(decorator, mock_sleep):
    operation = Mock(side_effect=TypeError('not retriable'))
    with pytest.raises(TypeError):
        decorator(exceptions=(ValueError,))(operation)()
    operation.assert_called_once_with()
    mock_sleep.assert_not_called()


@pytest.mark.parametrize('decorator', DECORATORS)
@pytest.mark.parametrize('options,error', [
    ({'retries': 0}, ValueError), ({'retries': -1}, ValueError),
    ({'retries': True}, TypeError), ({'retries': 1.5}, TypeError),
    ({'retry_delay': -1}, ValueError), ({'retry_delay': float('nan')}, ValueError),
    ({'retry_delay': float('inf')}, ValueError), ({'retry_delay': '1'}, TypeError),
    ({'exceptions': [ValueError]}, TypeError), ({'exceptions': (object,)}, TypeError),
    ({'exceptions': (KeyboardInterrupt,)}, TypeError),
])
def test_invalid_configuration(decorator, options, error):
    with pytest.raises(error):
        decorator(**options)


def test_condition_exhaustion(mock_sleep):
    operation = Mock(return_value='retry')
    assert retry_with_condition(retries=3, retry_delay=0,
        conditional=lambda result: result == 'retry',
        default_return_value='fallback')(operation)() == 'fallback'
    assert operation.call_count == 3
    assert mock_sleep.call_args_list == [call(0), call(0)]


def test_predicate_error_propagates(mock_sleep):
    operation = Mock(return_value='success')
    condition = Mock(side_effect=ValueError('bad predicate'))
    with pytest.raises(ValueError, match='bad predicate'):
        retry_with_condition(conditional=condition)(operation)()
    operation.assert_called_once_with()
    mock_sleep.assert_not_called()


def test_invalid_condition():
    with pytest.raises(TypeError):
        retry_with_condition(conditional=False)


@pytest.mark.parametrize('decorator', DECORATORS)
def test_empty_exceptions(decorator, mock_sleep):
    with pytest.raises(ValueError):
        decorator(exceptions=())(Mock(side_effect=ValueError))()
    mock_sleep.assert_not_called()


def test_logging_and_custom_message(caplog, capsys):
    with caplog.at_level('DEBUG', logger='retry_ops.decorators'):
        assert silent_retry_with_default(retries=1, error_message='exhausted')(
            Mock(side_effect=ValueError('failure')))() is None
    assert 'exhausted' in caplog.text
    assert capsys.readouterr().out == ''


def test_custom_retry_error():
    with pytest.raises(RetryError, match='custom'):
        retry(retries=1, error_message='custom')(Mock(side_effect=ValueError))()
