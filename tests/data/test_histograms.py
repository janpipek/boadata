from boadata.data.numpy_types import NumpyArray
from boadata.data.plotting_types import HistogramData
import numpy as np


class TestEmpty:
    def test_empty_is_empty(self):
        empty = HistogramData(bins = np.linspace(0, 10, 11))
        assert np.allclose(empty.values, np.zeros(10))
        assert empty.total == 0
        assert empty.overflow == 0
        assert empty.underflow == 0
        assert empty.total_weight == 0


class TestFill:
    def test_fill_empty(self):
        empty = HistogramData(bins = np.linspace(0, 10, 11))
        empty.fill(5)
        assert empty.total == 1
        empty.fill(5, 0.4)
        assert np.isclose(empty.total_weight, 1.4)
        assert np.isclose(empty.total, 2)


if __name__ == "__main__":
    import pytest
    pytest.main(__file__)