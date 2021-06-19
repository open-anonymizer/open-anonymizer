import pytest

from open_anonymizer.model_utils import *
from open_anonymizer.utils import *


@pytest.fixture
def init_large_model():
    nlp = init_pipeline("xlm-roberta-large-finetuned-conll03-german")
    return nlp


def test_clean_entities_person(init_large_model):
    assert "Hallo ich bin PERSON_1" == clean_entities(
        "Hallo ich bin Markus", init_large_model, entities=["PER"]
    )


def test_clean_entities_location(init_large_model):
    assert "ich lebe in LOCATION_1" == clean_entities(
        "ich lebe in Köln", init_large_model, entities=["LOC"]
    )
    assert "ich lebe in LOCATION_1" == clean_entities(
        "ich lebe in 78250 Tengen", init_large_model, entities=["LOC"]
    )


def test_clean_entities_org(init_large_model):
    assert "ich arbeite bei ORG_1" == clean_entities(
        "ich arbeite bei Facebook", init_large_model, entities=["ORG"]
    )
