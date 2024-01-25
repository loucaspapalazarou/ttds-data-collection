import re
from urllib.parse import urlparse


def url_to_id(url: str):
    parsed_url = urlparse(url)
    sld = parsed_url.netloc.split(".")[1]
    job_id = parsed_url.path.split("-")[-1]
    return f"{sld}-{job_id}"


def clean_data(value: str):
    cleaned_value = re.sub(r"(<br>|</p>|\n|<p\s*[^>]*?>)", " ", value)
    return " ".join(cleaned_value.split())


def string_to_date(s: str):
    return " ".join(s[s.find(",") + 1 :].split()[:2])
