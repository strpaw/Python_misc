"""Encode text to Morse code, display and play encoded text.
Note:  Space between words in encoded text will be represented by '/'
"""
import argparse
from winsound import Beep
from time import sleep
import sys

WORDS_SEP = " "
MORSE_SYMBOLS = {
    "A": "._",   "B": "_...", "C": "_._.", "D": "_..", "E": ".",
    "F": ".._.", "G": "__.",  "H": "....", "I": "..",  "J": ".___",
    "K": "_._",  "L": "._..", "M": "__",   "N": "_.",  "O": "___",
    "P": ".__.", "Q": "__._", "R": "._.",  "S": "...", "T": "_",
    "U": ".._",  "V": "..._", "W": ".__", "X": "_.._", "Y": "_.__",
    "Z": "___..",
    " ": "/"
}


def parse_args() -> argparse.Namespace:
    """Return parsed arguments"""
    parser = argparse.ArgumentParser(
        description="""Encode text to Morse code, display encoded text and play it."""
    )
    parser.add_argument(
        "-m",
        "--message",
        type=str,
        required=True,
        help="Message to encode"
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        required=False,
        help="Output file to save input text and its encoded version")

    return parser.parse_args()


def check_message(message: str) -> bool:
    """Return True if message consists of alphanumeric characters and space, False otherwise

    :param message: message to be encoded
    :return: message check result
    """
    return message.replace(" ", "").isalpha()


def encode_text(message: str) -> str:
    """Encode text to the Morse code.

    :param message: text to be encoded to the Morse code
    :return: Morse code 'character' (dot or dahs)
    """
    if not check_message(message):
        print("Allowed characters: A-Z, space")
        sys.exit()

    encoded_chars = [MORSE_SYMBOLS[char] for char in message.upper()]

    return " ".join(encoded_chars)


def beep_dit() -> None:
    """Make dit sound"""
    Beep(400, 70)


def beep_dah() -> None:
    """Make dah sound"""
    Beep(400, 210)


def play_morse_symbol(symbol: str) -> None:
    """Play single Morse symbol.

    :param symbol: Morse symbol (dits, dahs) to play
    """
    for signal in symbol:
        if signal == '.':
            beep_dit()
        elif signal == "_":
            beep_dah()
        sleep(0.07)  # pause between dits/dahs


def play_morse_code(code: str) -> None:
    """Make Morse sound - dots, dashes beeps and pauses for encoded text.

    :param code: Morse code
    :type code: str
    """
    for word in code.split("  "):  # Two spaces separate Morse codes for single words
        for symbol in word.split():  # One space separates Morse symbols for letters
            play_morse_symbol(symbol)
            sleep(0.24)  # pause between Morse symbols (single encoded letters)
        sleep(0.49)  # pause between words


def save_encoding(
        message: str,
        morse_code: str,
        path: str
) -> None:
    """Save encoding text to Morse code into file.

    :param message: text to be encoded
    :param morse_code: encoded text
    :param path: path to file where save text and its Morse code version
    """
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"Text: {message}\n")
        f.write(f"Morse code: {morse_code}")


def main(args_: argparse.Namespace) -> None:
    """Script loop execution.

    :param args_: parsed arguments passed to the script
    :return:
    """
    encoded_text = encode_text(args_.message)
    print(encoded_text)
    play_morse_code(encoded_text)

    if args_.output:
        save_encoding(
            message=args_.message,
            morse_code=encoded_text,
            path=args_.output
        )


if __name__ == "__main__":
    args = parse_args()
    main(args)
