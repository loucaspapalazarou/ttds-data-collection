import re


def clean_data(value: str):
    cleaned_value = re.sub(r"(<br>|</p>|\n|<p\s*[^>]*?>)", " ", value)
    return " ".join(cleaned_value.split())


def mark_jobs24(value):
    return "jobs24-" + value


def mark_s1jobs(value):
    return "s1jobs-" + value


def string_to_date(s: str):
    return " ".join(s[s.find(",") + 1 :].split()[:2])
