from io import StringIO

from numpy import ndarray, isclose
import pandas as pd

from climate_data_unit_converter import (
    celsius_to_fahrenheit,
    fahrenheit_to_celsius,
    get_conversion_function,
    convert_to_c_mm,
    convert_to_f_inch
)


def test_celsius_to_fahrenheit():
    assert 30.2 == celsius_to_fahrenheit(-1.0)
    assert 32.0 == celsius_to_fahrenheit(0.0)
    assert 33.8 == celsius_to_fahrenheit(1.0)
    assert isinstance(celsius_to_fahrenheit(1), float)


def test_fahrenheit_to_celsius():
    assert -1.0 == fahrenheit_to_celsius(30.2)
    assert 0.0 == fahrenheit_to_celsius(32.0)
    assert 1.0 == fahrenheit_to_celsius(33.8)
    assert isinstance(fahrenheit_to_celsius(32), float)


def test_get_conversion_function():
    assert get_conversion_function("C_mm") == convert_to_c_mm
    assert get_conversion_function("F_inch") == convert_to_f_inch


def test_convert_to_f_inch():
    data_c_mm = StringIO("""Station;Element;Jan;Feb;Mar;Apr;May;Jun;Jul;Aug;Sep;Oct;Nov;Dec
    Warsaw;Temp;-1.5;-0.4;3.2;9.2;14.3;17.7;19.7;19.1;14.0;8.7;3.8;-0.1
    Warsaw;Precipitation;31.0;29.8;29.0;35.1;55.5;52.4;40.1;46.0;50.4;40.2;36.0;36.1""")

    data_f_inch = StringIO("""Station;Element;Jan;Feb;Mar;Apr;May;Jun;Jul;Aug;Sep;Oct;Nov;Dec
    Warsaw;Temp;29.3;31.3;37.8;48.6;57.7;63.9;67.5;66.4;57.2;47.7;38.8;31.8
    Warsaw;Precipitation;1.22;1.17;1.14;1.38;2.19;2.06;1.58;1.81;1.98;1.58;1.42;1.42""")

    df_c_mm = pd.read_table(data_c_mm, delimiter=';', index_col=['Station', 'Element'])
    t_c = df_c_mm[df_c_mm.index.get_level_values('Element') == 'Temp']
    p_mm = df_c_mm[df_c_mm.index.get_level_values('Element') == 'Precipitation']

    df_f_inch = pd.read_table(data_f_inch, delimiter=';', index_col=['Station', 'Element'])
    t_f = df_f_inch[df_f_inch.index.get_level_values('Element') == 'Temp']
    p_inch = df_f_inch[df_f_inch.index.get_level_values('Element') == 'Precipitation']

    t_f_calc, p_inch_calc = convert_to_f_inch(t_c, p_mm)

    # Take into account rounding errors
    arr_t_f = t_f.to_numpy()
    arr_t_f_calc = t_f_calc.to_numpy()
    assert ndarray.all(isclose(arr_t_f, arr_t_f_calc, atol=0.1))

    arr_p_inch = p_inch.to_numpy()
    arr_p_inch_calc = p_inch_calc.to_numpy()
    assert ndarray.all(isclose(arr_p_inch, arr_p_inch_calc, atol=0.01))


def test_convert_to_c_mm():
    data_c_mm = StringIO("""Station;Element;Jan;Feb;Mar;Apr;May;Jun;Jul;Aug;Sep;Oct;Nov;Dec
    Warsaw;Temp;-1.5;-0.4;3.2;9.2;14.3;17.7;19.7;19.1;14.0;8.7;3.8;-0.1
    Warsaw;Precipitation;31.0;29.8;29.0;35.1;55.5;52.4;40.1;46.0;50.4;40.2;36.0;36.1""")

    data_f_inch = StringIO("""Station;Element;Jan;Feb;Mar;Apr;May;Jun;Jul;Aug;Sep;Oct;Nov;Dec
    Warsaw;Temp;29.3;31.3;37.8;48.6;57.7;63.9;67.5;66.4;57.2;47.7;38.8;31.8
    Warsaw;Precipitation;1.22;1.17;1.14;1.38;2.19;2.06;1.58;1.81;1.98;1.58;1.42;1.42""")

    df_c_mm = pd.read_table(data_c_mm, delimiter=';', index_col=['Station', 'Element'])
    t_c = df_c_mm[df_c_mm.index.get_level_values('Element') == 'Temp']
    p_mm = df_c_mm[df_c_mm.index.get_level_values('Element') == 'Precipitation']

    df_f_inch = pd.read_table(data_f_inch, delimiter=';', index_col=['Station', 'Element'])
    t_f = df_f_inch[df_f_inch.index.get_level_values('Element') == 'Temp']
    p_inch = df_f_inch[df_f_inch.index.get_level_values('Element') == 'Precipitation']

    t_c_calc, p_mm_calc = convert_to_c_mm(t_f, p_inch)

    # Take into account rounding errors
    arr_t_c = t_c.to_numpy()
    arr_t_c_calc = t_c_calc.to_numpy()
    assert ndarray.all(isclose(arr_t_c, arr_t_c_calc, atol=0.1))

    arr_p_mm = p_mm.to_numpy()
    arr_p_mm_calc = p_mm_calc.to_numpy()
    assert ndarray.all(isclose(arr_p_mm, arr_p_mm_calc, atol=0.1))
