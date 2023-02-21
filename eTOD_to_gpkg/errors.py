"""Custom errors"""


class CoordinateValueError(Exception):
    """Risen when cannot convert coordinate to decimal degrees if there is error in coordinate or coordinate is in
    not supported format"""

    def __init__(self, coordinate: str):
        self.coordinate = coordinate
        """Invalid/nor supported format coordinate to convert to decimal degrees format"""
        super().__init__(f"Coordinate error/not supported format: {self.coordinate}.")
