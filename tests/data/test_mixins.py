from boadata import wrap
import numpy as np


class TestStatisticsMixin:
    def __init__(self):
        x = [1, 2, 3, 4, 6]
        native_array = np.array(x)
        self.array = wrap(native_array)

    def test_mean(self):
        assert self.array.mean() == 3.2

    def test_median(self):
        assert self.array.median() == 3.5


if __name__ == "__main__":
    import pytest
    pytest.main(__file__)