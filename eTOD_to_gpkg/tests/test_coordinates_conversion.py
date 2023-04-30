import pytest

from eTOD_to_gpkg.coordinates_conversion import (
    longitude_to_dd,
    latitude_to_dd
)

VALID_LONGITUDES = [
    ("E 0 0 0", 0.0),
    ("W 10 0 0", -10.0),
    ("E 110 30 0", 110.5),
    ("W 10 30 30", -10.508333333333333),
    ("E 000 00 00", 0.0),
    ("W 010 00 00", -10.0),
    ("E 110 30 00", 110.5),
    ("W 010 30 30", -10.508333333333333),
    ("0 0 0 E", 0.0),
    ("10 0 0 W", -10.0),
    ("110 30 0 E", 110.5),
    ("10 30 30 W", -10.508333333333333),
    ("000 00 00 E", 0.0),
    ("010 00 00 W", -10.0),
    ("110 30 00 E", 110.5),
    ("010 30 30 W", -10.508333333333333),
    ("E0000000", 0.0),
    ("W0100000", -10.0),
    ("E1103000", 110.5),
    ("W0103030", -10.508333333333333),
    ("0000000E", 0.0),
    ("0100000W", -10.0),
    ("1103000E", 110.5),
    ("0103030W", -10.508333333333333)
]

VALID_LATITUDES = [
    ("N 0 0 0", 0.0),
    ("S 10 0 0", -10.0),
    ("N 0 0 0", 0.0),
    ("S 10 0 0", -10.0),
]


@pytest.mark.parametrize("dms, dd", VALID_LONGITUDES)
def test_longitude_to_dd_longitude_valid(dms, dd):
    assert longitude_to_dd(dms) == dd


@pytest.mark.parametrize("lat, lat_dd", VALID_LATITUDES)
def test_latitude_to_dd_valid(lat, lat_dd):
    assert latitude_to_dd(lat) == lat_dd
