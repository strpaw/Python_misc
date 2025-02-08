"""
Script to convert monthly climate data (temperature, precipitation) between Celsius degrees, millimetres and
Fahrenheit degrees and inches.

Note:
    if target unit is C_MM (Celsius, millimeters) - input data should be in Fahrenheit and inches
    if target unit is F_INCH (Fahrenheit, inches) - input data should be in Celsius and millimeters

Example input file - Celsius degrees, millimetres
Station;Element;Jan;Feb;Mar;Apr;May;Jun;Jul;Aug;Sep;Oct;Nov;Dec
Sydney;Temp;23.5;23.4;22.1;19.5;16.6;14.2;13.4;14.5;17;18.9;20.4;22.1
Sydney;Precipitation;91.1;131.5;117.5;114.1;100.8;142;80.3;75.1;63.4;67.7;90.6;73

Output file - Fahrenheit degrees, inches
"""
import argparse
from typing import Callable

import pandas as pd

INCH_MM = 25.4


def parse_args() -> argparse.Namespace:
    """Return parsed arguments"""
    parser = argparse.ArgumentParser(
        description="""Convert climate data Celsius degrees, mm to Fahrenheit degrees, inches,
                        and Fahrenheit degrees, inches to Celsius degrees, mm"""
    )
    parser.add_argument("-i", "--input", type=str, required=True, help="Path to input data file")
    parser.add_argument("-o", "--output", type=str, required=True, help="Path to output data")
    parser.add_argument("-t", "--target-unit", type=str, required=True, choices=["C_mm", "F_inch"],
                        help="Target unit, C_mm for Celsius, millimeters, F_inch - Fahrenheit, inches")

    return parser.parse_args()


def celsius_to_fahrenheit(value: float) -> float:
    """Return Fahrenheit degrees.

    :param value: Celsius degrees
    :return: Fahrenheit degrees
    """
    return round(value * 9 / 5 + 32, 1)


def fahrenheit_to_celsius(value: float) -> float:
    """Return Celsius degrees.

    :param value: Fahrenheit degrees
    :return: Celsius degrees
    """
    return round((value - 32) * 5 / 9, 1)


def mm_to_inch(value: float) -> float:
    """Convert millimeters into inches

    :param value: value in millimeters
    :return: value in inches
    """
    return round(value / INCH_MM, 2)


def inch_to_mm(value: float) -> float:
    """Convert inches into millimeters

    :param value: value in inches
    :return: value in millimeters
    """
    return round(value * INCH_MM, 1)


def convert_to_c_mm(t: pd.DataFrame, p: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return tuple (temperature, precipitation) dataframes with values in Celsius degrees and millimeters.

    :param t: data frame with temperature from input data
    :param p: data frame with precipitation from input data
    :return: tuple (data frame temperature, data frame precipitation) with converted values
    """
    return t.apply(fahrenheit_to_celsius), p.apply(inch_to_mm)


def convert_to_f_inch(t: pd.DataFrame, p: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return tuple (temperature, precipitation) dataframes with values in Fahrenheit degrees and inches.

    :param t: data frame with temperature from input
    :param p: data frame with precipitation from input
    :return: tuple (data frame temperature, data frame precipitation) with converted values
    """
    return t.apply(celsius_to_fahrenheit), p.apply(mm_to_inch)


def get_conversion_function(target_unit: str) -> Callable:
    """Return conversion function specific to target unit.
    In case target_unit is not supported raise ValueError.

    :param target_unit: unit to which convert data
    :return: conversion function used for conversion
    """
    match target_unit:
        case "C_mm": return convert_to_c_mm
        case "F_inch": return convert_to_f_inch
        case _: raise ValueError(f"Not supported target unit: {target_unit}")


def main(
        input_path: str,
        output_path: str,
        target_unit: str
):
    """Convert climate data to target units.

    :param input_path: path to the input data file
    :param output_path: path to the output data file
    :param target_unit: unit to which input data will be converted
    :return:
    """
    src_data = pd.read_csv(input_path, sep=';', index_col=['Station', 'Element'])
    src_temp = src_data[src_data.index.get_level_values('Element') == 'Temp']
    src_precip = src_data[src_data.index.get_level_values('Element') == 'Precipitation']

    convert_func = get_conversion_function(target_unit)
    target_temp, target_precip = convert_func(src_temp, src_precip)

    output_data = pd.concat([target_temp, target_precip])
    output_data.sort_index(inplace=True)
    output_data.to_csv(output_path)


if __name__ == "__main__":
    args = parse_args()
    main(args.input, args.output, args.target_unit)
