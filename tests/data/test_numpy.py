from boadata.data.numpy_types import NumpyArray
import numpy as np


class TestNumpyWhere:
    @property
    def array(self):
        return NumpyArray(np.array([[0.5, 1.0], [1.5, 2.0]]))

    def test_lambda(self):
        assert np.allclose(self.array.where(lambda x: x > 1.0).inner_data, np.array([1.5, 2.0]))

    def test_function(self):
        pass


if __name__ == "__main__":
    import pytest
    pytest.main(__file__)