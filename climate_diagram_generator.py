"""
Script to generate climate diagrams (charts) with average monthly temperature and precipitation.
Input data:
    - CSV file with separator semicolon ';'
    - first line is header line
    - precipitation in mm
    - temperature in Celsius degrees

Example input file:
Station;Element;Jan;Feb;Mar;Apr;May;Jun;Jul;Aug;Sep;Oct;Nov;Dec
Sydney;Temp;23.5;23.4;22.1;19.5;16.6;14.2;13.4;14.5;17;18.9;20.4;22.1
Sydney;Precipitation;91.1;131.5;117.5;114.1;100.8;142;80.3;75.1;63.4;67.7;90.6;73
"""
from math import (
    ceil,
    floor
)
from typing import NamedTuple
import sys

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


TempMin = float
TempMax = float
TempRange = tuple[TempMin, TempMax]


class YAxisLimits(NamedTuple):
    """Keep Y axis limits fr temperature, precipitation"""
    tmin: int
    tmax: int
    pmax: int


def round_down(num: float, multiple: int) -> int:
    """Rounds down a number to the nearest multiple of given value such as 1, 5, 10 etc.

    :param num: number to be rounded
    :param multiple: multiple of number to be round to
    :return: rounded value
    """
    return floor(num / multiple) * multiple


def round_up(num: float, multiple: int) -> int:
    """Rounds up a number the nearest multiple of given value such as 1, 5, 10 etc.

    :param num: value to be rounded
    :param multiple: multiplies of value round to
    :return: rounded value
    """
    return ceil(num / multiple) * multiple


def get_temp_range(df: pd.DataFrame) -> TempRange:
    """Returns minimum and maximum monthly temperature for the whole dataset.

    :param df: the whole dataset
    :return: min, max average monthly temperatures
    """
    temp_df = df[df.index.get_level_values('Element') == 'Temp']
    temp_arr = temp_df.to_numpy()
    return temp_arr.min(), temp_arr.max()


def get_max_precip(df: pd.DataFrame) -> float:
    """Returns maximum monthly precipitation for the whole dataset

    :param df: the whole data set
    :return: maximum monthly precipitation
    """
    precip_df = df[df.index.get_level_values('Element') == 'Precipitation']
    return precip_df.to_numpy().max()


def get_yaxis_limits(df: pd.DataFrame) -> YAxisLimits:
    """Returns limits (min, max values) of precipitation, temperature y axes.
    Notes:
        precipitation:
            min - always 0
            max - max monthly precipitation round up to 100th
        temperature:
            min:
                0 if min monthly temperature is > 0)
                min monthly temperature round down to 5th if min monthly temperature is < 0
            max:
                0 if max monthly temperature is < 0)
                max monthly temperature round yp to 5th if max monthly temperature is > 0
    :param df: whole data set
    :return: named tuple YAxisLimits (y axis values for temperature and precipitation)
    """
    tmin, tmax = get_temp_range(df)

    if tmin > 0:
        tmin = 0
    else:
        tmin = round_down(tmin, 5)

    if tmax < 0:
        tmax = 0
    else:
        tmax = round_up(tmax, 5)

    pmax = get_max_precip(df)
    pmax = round_up(pmax, 100)

    return YAxisLimits(tmin=tmin, tmax=tmax, pmax=pmax)


def create_diagram(
        y_axis_limits: YAxisLimits,
        station_data: pd.DataFrame,
        station: str
) -> None:
    """Create climate diagram for single station.

    :param y_axis_limits: limits (min and max temperature, max precipitation) for Y axis
    :param station_data: data (temperature, precipitation) for single station
    :param station: station name
    """
    climate_diagram = plt.figure(dpi=600)

    precip_ax = climate_diagram.add_axes((0.1, 0.1, 0.4, 0.8))
    precip_ax.yaxis.tick_left()
    precip_ax.set_ylim(0, y_axis_limits.pmax)
    precip_ax.yaxis.set_label_position('left')
    precip_ax.set_ylabel('mm')

    temp_ax = precip_ax.twinx()
    temp_ax.set_ylim(y_axis_limits.tmin, y_axis_limits.tmax)
    temp_ax.yaxis.tick_right()
    temp_ax.yaxis.set_label_position('right')
    temp_ax.set_ylabel('°C')

    temp_data = station_data.loc['Temp']
    precip_data = station_data.loc['Precipitation']
    precip_ax.bar(np.arange(1, 13).astype(str), precip_data, color='b', zorder=1)
    temp_ax.plot(np.arange(1, 13).astype(str), temp_data, color='r', zorder=2)

    mean_temp = round(temp_data.mean(), 1)
    sum_precip = round(precip_data.sum(), 1)
    precip_ax.set_title(f'Mean {mean_temp} °C, Sum  {sum_precip} mm')

    plt.savefig(f'{station}.jpg', bbox_inches='tight')


def main(data_path: str) -> None:
    """ Create chart diagrams for data in CSV file
    :param data_path: path to data file
    :type data_path: str
    """
    climate_data = pd.read_csv(data_path, sep=';', index_col=['Station', 'Element'])
    stations = set(climate_data.index.get_level_values(0))
    y_axis_limits = get_yaxis_limits(climate_data)

    num_stations = len(stations)
    print(f'{num_stations} station(s) found in {data_path}')
    for i, station in enumerate(stations, start=1):
        print(f'Creating diagram for {station} [{i}/{num_stations}] ...')
        station_data = climate_data.loc[station]
        create_diagram(y_axis_limits, station_data, station)


def usage() -> None:
    """Print help how to use script."""
    print('Usage:\nclimate_diagram_generator.py <climate_data.csv>')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
        sys.exit(0)

    main(sys.argv[1])
