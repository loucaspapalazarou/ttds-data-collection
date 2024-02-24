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


def link_to_location(url: str):
    domain_to_location = {
        "s1jobs.com": "Scotland",
        "y1jobs.com": "Yorkshire",
        "ne1jobs.com": "Northeast England",
        "l1jobs.com": "Liverpool",
        "se1jobs.com": "Southeast England",
        "sw1jobs.com": "Southwest England",
        "wm1jobs.com": "West Midlands",
        "w1jobs.com": "Wales",
        "em1jobs.com": "East Midlands",
        "ea1jobs.com": "East Anglia",
        "ox1jobs.com": "Oxfordshire",
        "jobs24.co.uk": "England & Wales",
    }
    domain = url.split("//")[-1].split("/")[0].removeprefix("www.")
    if domain in domain_to_location:
        return domain_to_location[domain]
    else:
        return ""
