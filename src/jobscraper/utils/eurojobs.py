import re


def mark_eurojobs(value):
    return "eurojobs-" + value


def clean_data(value: str):
    cleaned_value = re.sub(r"(<br>|</p>|\n|<p\s*[^>]*?>)", " ", value)
    return " ".join(cleaned_value.split())


def clean_title(value: str):
    return value.strip()


def clean_location(value: str):
    return (
        value.replace("\xa0", " ")
        .replace("\t", "")
        .replace("\r", "")
        .replace("\n", "")
        .strip()
    )
