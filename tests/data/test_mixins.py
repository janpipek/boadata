from boadata import wrap
import numpy as np
import pandas as pd


class TestStatisticsMixin:
    @property
    def array(self):
        x = [1, 2, 3, 4, 6]
        native_array = np.array(x)
        return wrap(native_array)

    def test_mean(self):
        assert self.array.mean() == 3.2

    def test_median(self):
        assert self.array.median() == 3

    def test_mode(self):
        array1 = wrap(np.array([1, 1, 2, 3]))
        assert array1.mode() == 1

        array2 = wrap(np.array([1, 1, 2, 2, 3, 4, 5]))
        assert array2.mode() == 1

        array3 = wrap(pd.Series([1, 2, 3, 4, 4, 0, 0]))
        assert array3.mode() == 0

        array4 = wrap(pd.Series([1, 2, 3, 4, 4, 0, 0, -2, -2]))
        assert array4.mode() == -2


if __name__ == "__main__":
    import pytest
    pytest.main(__file__)