"""Read configuration file."""
from yaml import safe_load


class Configuration:

    def __init__(self, path: str = "config.yml") -> None:
        """Configuration to read/parse eTOD file into gpkg file.

        :param path: path to the configuration file
        :type path: str
        """
        with open(path, "r") as f:
            config = safe_load(f)
            self.file_settings: dict = config["file_settings"]
            """File settings: column separator, encoding, skip first rows containing some additional information"""
            self.col_lon: str = config["coordinates"]["columns"]["longitude"]
            """Column that keeps longitude"""
            self.col_lat: str = config["coordinates"]["columns"]["latitude"]
            """Column that keeps latitude"""
            self.column_map: dict = config["column_map"]
            """Mapping between column names in source data CSV file and colum names in output file"""
