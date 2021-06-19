from copy import deepcopy

from open_anonymizer.model_utils import clean_entities
from open_anonymizer.regex_rules import (regex_clean_date, regex_clean_email,
                                         regex_clean_number, regex_clean_phone)


def anonymize(text, pipeline, entities, flag_replace_address):

    if not isinstance(text, str):
        return text

    else:
        cleaned_text = deepcopy(text)
        nlp = pipeline

        try:
            if "DATE" in entities:
                cleaned_text = regex_clean_date(cleaned_text)
            if "PHONE" in entities:
                cleaned_text = regex_clean_phone(cleaned_text)
            if "NUMBER" in entities:
                cleaned_text = regex_clean_number(cleaned_text, True)
            if "EMAIL" in entities:
                cleaned_text = regex_clean_email(cleaned_text)

            if any([e in ["PER", "LOC", "ORG"] for e in entities]):

                cleaned_text = clean_entities(
                    text=cleaned_text,
                    pipeline=nlp,
                    entities=entities,
                    replace_address=flag_replace_address,
                )

            return cleaned_text

        except Exception as e:
            print("=======================================")
            print(e)
            print("=======================================")
            print(cleaned_text)
            print("=======================================")
            print("returning None, but continuing")
            return None
