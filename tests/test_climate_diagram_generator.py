from io import StringIO
import pandas as pd
from pytest import mark

from climate_diagram_generator import (
    round_down,
    round_up,
    get_temp_range,
    get_max_precip,
    get_yaxis_limits,
    YAxisLimits
)


@mark.parametrize("num, multiple, expected",
                  [
                      (41.1, 1, 41),
                      (41.1, 10, 40),
                      (41.1, 100, 0),
                      (371.1, 100, 300),
                      (-2.1, 1, -3),
                      (-2.1, 5, -5),
                      (-2.1, 10, -10)
                  ])
def test_round_down(num, multiple, expected):
    assert round_down(num, multiple) == expected


@mark.parametrize("num, multiple, expected",
                  [
                      (41.1, 1, 42),
                      (41.1, 10, 50),
                      (41.1, 100, 100),
                      (-2.1, 1, -2),
                      (-2.1, 10, 0),
                      (-21, 10, -20)
                  ])
def test_round_up(num, multiple, expected):
    assert round_up(num, multiple) == expected


def test_get_temp_range():
    data = StringIO('''Station;Element;Jan;Feb;Mar;Apr;May;Jun;Jul;Aug;Sep;Oct;Nov;Dec
    Warsaw;Temp;-1.5;-0.4;3.2;9.2;14.3;17.7;19.7;19.1;14.0;8.7;3.8;-0.1
    Warsaw;Precipitation;31.0;29.8;29.0;35.1;55.5;52.4;40.1;46.0;50.4;40.2;36.0;36.1''')
    df = pd.read_table(data, delimiter=';', index_col=['Station', 'Element'])
    assert get_temp_range(df) == (-1.5, 19.7)


def test_get_max_precip():
    data = StringIO('''Station;Element;Jan;Feb;Mar;Apr;May;Jun;Jul;Aug;Sep;Oct;Nov;Dec
    Warsaw;Temp;-1.5;-0.4;3.2;9.2;14.3;17.7;19.7;19.1;14.0;8.7;3.8;-0.1
    Warsaw;Precipitation;31.0;29.8;29.0;35.1;55.5;52.4;40.1;46.0;50.4;40.2;36.0;36.1''')
    df = pd.read_table(data, delimiter=';', index_col=['Station', 'Element'])
    assert get_max_precip(df) == 55.5


def test_get_yaxis_limits():
    data = StringIO('''Station;Element;Jan;Feb;Mar;Apr;May;Jun;Jul;Aug;Sep;Oct;Nov;Dec
    Vostok;Temp;-31.7;-44.2;-58.2;-64.5;-65.7;-66.0;-65.9;-67.4;-66.1;-56.5;-41.6;-31.1
    Vostok;Precipitation;1.7;1.1;1.9;2.7;2.8;2.4;1.9;1.8;1.9;2.5;1.6;1.6''')
    df = pd.read_table(data, delimiter=';', index_col=['Station', 'Element'])
    assert get_yaxis_limits(df) == YAxisLimits(tmin=-70, tmax=0, pmax=100)

    data = StringIO('''Station;Element;Jan;Feb;Mar;Apr;May;Jun;Jul;Aug;Sep;Oct;Nov;Dec
    Warsaw;Temp;-1.5;-0.4;3.2;9.2;14.3;17.7;19.7;19.1;14.0;8.7;3.8;-0.1
    Warsaw;Precipitation;31.0;29.8;29.0;35.1;55.5;52.4;40.1;46.0;50.4;40.2;36.0;36.1''')
    df = pd.read_table(data, delimiter=';', index_col=['Station', 'Element'])
    assert get_yaxis_limits(df) == YAxisLimits(tmin=-5, tmax=20, pmax=100)

    data = StringIO('''Station;Element;Jan;Feb;Mar;Apr;May;Jun;Jul;Aug;Sep;Oct;Nov;Dec
    Sydney;Temp;23.5;23.4;22.1;19.5;16.6;14.2;13.4;14.5;17;18.9;20.4;22.1
    Sydney;Precipitation;91.1;131.5;117.5;114.1;100.8;142;80.3;75.1;63.4;67.7;90.6;73''')
    df = pd.read_table(data, delimiter=';', index_col=['Station', 'Element'])
    assert get_yaxis_limits(df) == YAxisLimits(tmin=0, tmax=25, pmax=200)
