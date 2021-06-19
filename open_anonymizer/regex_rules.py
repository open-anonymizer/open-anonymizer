import re


def clean_regex_helper(text, pattern, placeholder, show_length=False):

    matches = re.findall(pattern, text)
    matches = [m if isinstance(m, str) else m[0] for m in matches]

    if placeholder == "DATE":
        matches = [m for m in matches if 5 < len(m) < 11]

    if not matches:
        return text

    mapping = {}
    count_no = 0

    for match in matches:

        if not match in mapping.values():
            count_no += 1
            placeholder_num = placeholder + "_"

            placeholder_num += str(count_no)
            if show_length:
                placeholder_num += "_" + str(len(match))

            text = text.replace(match, placeholder_num)
            mapping[placeholder_num] = match

    return text


def regex_clean_email(text):
    return clean_regex_helper(
        text, r"([a-zA-Z0-9._%+-]+@[a-zA-Z0-9._%+-]+(\.[a-zA-Z]{2,})?)", "EMAIL"
    )


def regex_clean_phone(text):
    return clean_regex_helper(
        text,
        r"(?:^|[^\d])((?:\+|0)[0-9]{2,6}(\-|\s|\/|\_|\:)?[0-9]{2,9}(\-|\s|\/|\_|\:)?[0-9]{2,14})",
        "PHONE",
    )


def regex_clean_date(text):
    return clean_regex_helper(
        text, r"([0-3]?[0-9]{1,4}[._%+-/][0-3]?[0-9]{1,4}([._%+-/])[0-3]?[0-9]{1,4})", "DATE"
    )


def regex_clean_number(text, count: bool = False):
    return clean_regex_helper(text, r"([0-9]{2}[0-9-\.\s\/\-\/\_\:]{3,}[0-9]{2})", "NUMBER", count)
