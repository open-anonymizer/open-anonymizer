import re

from transformers import pipeline


def load_model():
    pass


def init_pipeline(model_name):
    """
    Load model and return pipeline
    """
    nlp = pipeline("ner", model=model_name, grouped_entities=True)
    return nlp


def fix_strlist_value(value):
    """
    Fix prompt output
    """
    if " " in value or "," in value or all(len(i) == 1 for i in value):
        return [k for k in "".join(value).replace(",", " ").split(" ") if k]
    return value


def remove_context(text):
    """
    remove entities
    """

    re1 = "PERSON_[0-9]{1,2}"
    re2 = "LOCATION_[0-9]{1,2}"
    re3 = "ORG_[0-9]{1,2}"
    re4 = "EMAIL_[0-9]{1,2}"
    re5 = "PHONE_[0-9]{1,2}"
    re6 = "DATE_[0-9]{1,2}"
    re7 = "NUMBER_[0-9]{1,2}"
    re8 = "XXX_[0-9]{1,2}"

    re_list = [re1, re2, re3, re4, re5, re6, re7]
    generic_re = re.compile("|".join(re_list))

    matches = re.findall(generic_re, text)
    for m in matches:
        text = text.replace(m, "XXX")

    # number check again
    matches = re.findall(re8, text)
    for m in matches:
        text = text.replace(m, "XXX")

    return text
