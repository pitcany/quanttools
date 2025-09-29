import pytest

from ykp.execution import ExecutionHandler


def test_execution_handler_abstract():
    eh = ExecutionHandler()
    with pytest.raises(NotImplementedError):
        eh.send_order("SYM", 10)
