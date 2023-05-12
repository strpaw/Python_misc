"""Sunrise/sunset times calculation and plot generation."""
import argparse


def parse_args() -> argparse.Namespace:
    """Return parsed arguments"""
    parser = argparse.ArgumentParser(
        description='''Calculate sunrise/sunset for the whole year and create sunrise/sunset plot'''
    )

    subparsers = parser.add_subparsers()
    subparsers.required = True

    place_parser = subparsers.add_parser(
        'place',
        help='Calculation/plotting for single place')
    place_parser.add_argument(
        '-n',
        '--name',
        type=str,
        required=True,
        help='Place name'
    )
    place_parser.add_argument(
        '--lat',
        type=float,
        required=True,
        help='Latitude'
    )
    place_parser.add_argument(
        '--lon',
        type=float,
        required=True,
        help='Longitude'
    )
    place_parser.add_argument(
        '-t',
        '--table',
        action='store_true',
        help='Write sunrise/sunset to CSV file'
    )

    file_parser = subparsers.add_parser(
        'file',
        help='Calculation/plotting for multiple places provided in CSV file'
    )
    file_parser.add_argument('filename')
    file_parser.add_argument(
        '-t',
        '--table',
        action='store_true',
        help='Write sunrise/sunset to CSV file'
    )

    return parser.parse_args()


def main() -> None:
    """Main script loop"""
    args = parse_args()


if __name__ == '__main__':
    main()
