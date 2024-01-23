import re


def mark_cvlibrary(value):
    return "cvlibrary-" + value


def clean_data(value: str):
    cleaned_value = re.sub(r"(<br>|</p>|\n|<p\s*[^>]*?>)", " ", value)
    return " ".join(cleaned_value.split())
