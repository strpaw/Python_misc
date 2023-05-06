"""Encode text to Morse code, display and play encoded text"""
import argparse
from winsound import Beep
from time import sleep
import sys

PAUSE = " "
MORSE_SYMBOLS = {
    "A": "._",   "B": "_...", "C": "_._.", "D": "_..", "E": ".",
    "F": ".._.", "G": "__.",  "H": "....", "I": "..",  "J": ".___",
    "K": "_._",  "L": "._..", "M": "__",   "N": "_.",  "O": "___",
    "P": ".__.", "Q": "__._", "R": "._.",  "S": "...", "T": "_",
    "U": ".._",  "V": "..._", "W": ".__", "X": "_.._", "Y": "_.__",
    "Z": "___.."
}


def parse_args() -> argparse.Namespace:
    """Return parsed arguments"""
    parser = argparse.ArgumentParser(
        description="""Encode text to Morse code, display encoded text and play it."""
    )
    parser.add_argument("-m", "--message", type=str, required=True, help="Message to encode")
    parser.add_argument("-o", "--output", type=str, required=False, help="Output file to save input text and its "
                                                                         "encoded version")

    return parser.parse_args()


def check_message(message: str) -> bool:
    """Return True if message consists of alphanumeric characters and space, False otherwise

    :param message: message to be encoded
    :type message: str
    :return: message check result
    :rtype: bool
    """
    return message.replace(" ", "").isalpha()


def encode_text(message: str) -> str:
    """Encode text to Morse code.

    :param message: text to be encoded to Morse code
    :type message: str
    :return: Morse code
    :rtype: str
    """
    if not check_message(message):
        print("Allowed characters: A-Z, space")
        sys.exit()

    encoded = ""
    for char in message.upper():
        if char == PAUSE:
            encoded += PAUSE  # Two spaces separates words in encoded message
        else:
            encoded += MORSE_SYMBOLS[char] + PAUSE
    return encoded


def beep_dot() -> None:
    """Make 'dot' sound"""
    Beep(400, 70)


def beep_dash() -> None:
    """Make 'dash' sound"""
    Beep(400, 210)


def play_morse_symbol(symbol: str) -> None:
    """Play single Morse symbol.

    :param symbol: Morse symbol (dot(s), dash(es)) to play
    :type symbol: str
    """
    for signal in symbol:
        if signal == '.':
            beep_dot()
        elif signal == "_":
            beep_dash()
        sleep(0.07)  # pause between dots/dashes


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
    :type message: str
    :param morse_code: encoded text
    :type morse_code: str
    :param path: path to file where save text and its Morse code version
    :type path: str
    """
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"Text: {message}\n")
        f.write(f"Morse code: {morse_code}")


def main(args_: argparse.Namespace) -> None:
    """Script loop execution

    :param args_: parsed arguments passed to the script
    :type args_: argparse.Namespace
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
