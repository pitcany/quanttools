import pytest

from ykp.data import DataLoader


def test_data_loader_abstract():
    dl = DataLoader()
    with pytest.raises(NotImplementedError):
        dl.get_data("SYM", "2020-01-01", "2020-01-10")
