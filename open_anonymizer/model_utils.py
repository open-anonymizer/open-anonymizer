import re


def concat_elements(tag, spacer, text, counter):
    searchpattern = tag + "_([0-9]{1,2})(" + spacer + ")" + tag + "_([0-9]{1,2})"
    check_wrong = re.search(searchpattern, text)
    if check_wrong:
        old_first = f"{tag}_{check_wrong[1]}"
        old_second = f"{tag}_{check_wrong[3]}"

        text = text.replace(check_wrong[0], old_first)

        check_wrong = re.search(old_second, text)
        if not check_wrong:
            counter -= 1

    return text, counter


def clean_entities(text: str, pipeline, entities: list, replace_address: bool = True):

    found = [
        e for e in pipeline(text) if e.get("entity_group") in entities and len(e.get("word")) > 1
    ]

    if not found:
        return text

    count_per = 0
    count_loc = 0
    count_org = 0

    mapping = {}

    for each in found:

        word = each.get("word")
        if not word in mapping.values():

            if each.get("entity_group") == "PER":
                count_per += 1
                name = f"PERSON_{count_per}"

                if replace_address:
                    matches = re.findall(
                        rf"(?:^|\s)(((?:Herrn|Herr|Frau|Doktor|Familie|Hr\.|Fr\.|Dr\.|[A-Z]\.)[\s]*)?{word}[\w]*)",
                        text,
                    )

                    for person_match in matches:
                        text = text.replace(person_match[0], name)

                else:
                    matches = re.findall(rf"({word}[\w]*)", text)

                    for person_match in matches:
                        text = text.replace(person_match, name)

                # Concat multi word names: PERSON_1 PERSON_2 -> PERSON_1
                text, count_per = concat_elements("PERSON", "\s+|[a-z]+", text, count_per)

            elif each.get("entity_group") == "LOC":

                count_loc += 1
                name = f"LOCATION_{count_loc}"
                matches = re.findall(
                    rf"(?:^|\s)(((?:[0-9][0-9][0-9][0-9][0-9]|[0-9][0-9][0-9][0-9])[\s\,\.][\.]*)?{word}[\w]*)",
                    text,
                )

                for location_match in matches:
                    text = text.replace(location_match[0], name)

                # correcting some locations
                text, count_loc = concat_elements("LOCATION", "[a-z]+", text, count_loc)

            elif each.get("entity_group") == "ORG":
                count_org += 1
                name = f"ORG_{count_org}"

                matches = re.findall(rf"({word}[\w]*)", text)
                for org_match in matches:
                    text = text.replace(org_match, name)

                text, count_org = concat_elements("ORG", "[a-z]+", text, count_org)

    return text
