import pytest

from eTOD_to_gpkg.errors import CoordinateValueError


def test_coordinate_value_error():
    incorrect_coordinate = "E 0 0 0 W"
    with pytest.raises(CoordinateValueError, match=f"Coordinate error/not supported format: {incorrect_coordinate}."):
        raise CoordinateValueError(incorrect_coordinate)
