from pytest import mark

from morse_encoder import check_message, encode_text


@mark.parametrize("msg, expected",
                  [
                      ("TEST", True),
                      ("TEST TEST", True),
                      ("test", True),
                      ("1test", False)
                  ])
def test_check_message(msg, expected):
    assert check_message(msg) == expected


def test_encode_text():
    assert encode_text("TEST") == "_ . ... _"
    assert encode_text("test") == "_ . ... _"
    assert encode_text("TEST abc") == "_ . ... _ / ._ _... _._."
