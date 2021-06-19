from open_anonymizer.regex_rules import *


def test_regex_clean_email():
    assert "EMAIL_1" == regex_clean_email("markus.nutz@gmx.de")


def test_regex_clean_phone():
    assert "PHONE_1" == regex_clean_phone("0175-234578623")
    assert "PHONE_1" == regex_clean_phone("07736 951604")


def test_regex_clean_date():
    assert "DATE_1" == regex_clean_date("20.12.2021")
    # assert "DATE_1" == regex_clean_date("20-12-2012")
    # assert "DATE_1" == regex_clean_date("2021-12-02")


def test_regex_clean_number():
    assert "NUMBER_1" == regex_clean_number("1234567890")
    assert "NUMBER_1_10" == regex_clean_number("1234567890", True)
