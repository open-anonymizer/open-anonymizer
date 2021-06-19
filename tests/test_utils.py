from open_anonymizer.utils import *


def test_remove_context():
    assert "XXX" == remove_context("PERSON_1")
    assert "XXX" == remove_context("LOCATION_12")
    assert "XXX" == remove_context("ORG_3")
    assert "XXX" == remove_context("EMAIL_1")
    assert "XXX" == remove_context("PHONE_2")
    assert "XXX" == remove_context("DATE_5")
    assert "XXX" == remove_context("NUMBER_10")
    assert "XXX" == remove_context("NUMBER_1_12")
    assert "mein Name ist XXX, ich wohne in XXX" == remove_context(
        "mein Name ist PERSON_12, ich wohne in LOCATION_1"
    )
