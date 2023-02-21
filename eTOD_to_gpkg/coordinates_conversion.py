"""Coordinates conversion.

Common coordinates format in eTOD are:
- degrees, minutes, seconds with hemisphere prefix or suffix (HDMS, DMSH) where degrees, minutes, second, hemisphere
are separated by space example: N 51 43 50.55, 151 43 50.55E
- degrees, minutes, seconds with hemisphere prefix or suffix (HDMS, DMSH) 'compacted' degrees, minutes, second,
hemisphere are not separated example: N514350.55, 1514350.55E
"""
import logging
import re

from shapely.geometry import Point

from errors import CoordinateValueError

LONGITUDE_DELIMITED_PATTERN = re.compile(
    r"""^(?P<hem_prefix>[EW])?
         \s*
         (?P<deg>\d{1,3})
         \s
         (?P<min>\d{1,2})
         \s
         (?P<sec>\d{1,2}|\d{1,2}\.\d+)
         \s*
         (?P<hem_suffix>[EW])?$""",
    re.VERBOSE
)

LONGITUDE_COMPACTED_PATTERN = re.compile(
    r"""^(?P<hem_prefix>[EW])?
         (?P<deg>\d{3})
         (?P<min>\d{2})
         (?P<sec>\d{2}|\d{2}\.\d+)
         (?P<hem_suffix>[EW])?$""",
    re.VERBOSE
)

LATITUDE_DELIMITED_PATTERN = re.compile(
    r"""^(?P<hem_prefix>[NS])?
         \s*
         (?P<deg>\d{1,2})
         \s
         (?P<min>\d{1,2})
         \s
         (?P<sec>\d{1,2}|\d{1,2}\.\d+)
         \s*
         (?P<hem_suffix>[NS])?$""",
    re.VERBOSE
)

LATITUDE_COMPACTED_PATTERN = re.compile(
    r"""^(?P<hem_prefix>[NS])?
         (?P<deg>\d{2})
         (?P<min>\d{2})
         (?P<sec>\d{2}|\d{2}\.\d+)
         (?P<hem_suffix>[NS])?$""",
    re.VERBOSE
)


def longitude_to_dd(lon: str) -> float:
    """Return longitude in decimal degrees (DD) format.
    Raise CoordinateValueError when there is error in coordinate (example minute is out of range <0, 60)
    or coordinate is in not supported format.

    :param lon: longitude in HDMS or DMSH compacted or space delimited format
    :type lon: str
    :return: decimal degrees
    :rtype: float
    """
    match = re.match(LONGITUDE_DELIMITED_PATTERN, lon) or re.match(LONGITUDE_COMPACTED_PATTERN, lon)
    if not match:
        raise CoordinateValueError(lon)

    h = match.group("hem_prefix") or match.group("hem_suffix")
    d = int(match.group("deg"))
    m = int(match.group("min"))
    s = float(match.group("sec"))

    # hemisphere prefix and suffix cannot be both set
    # degrees within range <0, 180>
    # minutes and seconds  within range <0, 60)
    if (
        (match.group("hem_prefix") and match.group("hem_suffix"))
        or not 0 <= d <= 180
        or not 0 <= m < 60
        or not 0 <= s < 60
        or d == 180 and (m != 0 or s != 0)
    ):
        raise CoordinateValueError(lon)

    dd = d + (m + s / 60) / 60
    if h == "W":  # west hemisphere - negative values
        return -dd
    return dd


def latitude_to_dd(lat: str) -> float:
    """Return latitude in decimal degrees (DD) format.
    Raise CoordinateValueError when there is error in coordinate (example minute is out of range <0, 60)
    or coordinate is in not supported format.

    :param lat: latitude in HDMS or DMSH compacted or space delimited format
    :type lat: str
    :return: decimal degrees
    :rtype: float
    """
    match = re.match(LATITUDE_DELIMITED_PATTERN, lat) or re.match(LATITUDE_COMPACTED_PATTERN, lat)
    if not match:
        raise CoordinateValueError(lat)

    h = match.group("hem_prefix") or match.group("hem_suffix")
    d = int(match.group("deg"))
    m = int(match.group("min"))
    s = float(match.group("sec"))

    # hemisphere prefix and suffix cannot be both set
    # degrees within range <0, 90>
    # minutes and seconds  within range <0, 60)
    if (
        (match.group("hem_prefix") and match.group("hem_suffix"))
        or not 0 <= d <= 90
        or not 0 <= m < 60
        or not 0 <= s < 60
        or d == 90 and (m != 0 or s != 0)
    ):
        raise CoordinateValueError(lat)

    dd = d + (m + s / 60) / 60
    if h == "S":  # south hemisphere - negative values
        return -dd
    return dd


def coordinates_to_point_wkt(
    lon_dd: float,
    lat_dd: float
) -> str:
    """Return point as WKT string.

    :param lon_dd: longitude in decimal degrees format
    :type lon_dd: float
    :param lat_dd: latitude in decimal degrees format
    :type lat_dd: float
    :return: WKT representation of pair coordinates as Point
    :rtype: str
    """
    return Point(lon_dd, lat_dd).wkt
