import requests
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import psycopg2
import os
import datetime
from dotenv import load_dotenv
from w3lib.html import remove_tags
from datetime import datetime
import pycountry

load_dotenv()

RESULTS_PER_PAGE = 50
MAX_PAGES = 200
LOCATION_CODES = [
    "at",
    "be",
    "bg",
    "ch",
    "cy",
    "cz",
    "de",
    "dk",
    "ee",
    "el",
    "es",
    "fi",
    "fr",
    "hr",
    "hu",
    "ie",
    "is",
    "it",
    "li",
    "lt",
    "lu",
    "lv",
    "mt",
    "nl",
    "no",
    "pl",
    "pt",
    "ro",
    "se",
    "si",
    "sk",
]


def init_session() -> requests.Session:
    session = requests.Session()
    # get an unprotected route in order to get the cookies
    session.get(
        "https://europa.eu/eures/eures-apps/searchengine/page/common/security/profile?lang=en"
    )
    return session


def fetch_jobs(page_num: int, locationCodes: list[str] = []) -> dict:
    session = init_session()
    url = "https://europa.eu/eures/eures-apps/searchengine/page/jv-search/search"

    cookies = session.cookies.get_dict()
    headers = {
        "Cookie": f'EURES_JVSE_SESSIONID={cookies["EURES_JVSE_SESSIONID"]}; XSRF-TOKEN={cookies["XSRF-TOKEN"]};',
        "X-XSRF-TOKEN": f'{cookies["XSRF-TOKEN"]}',
        "Content-Type": "application/json",
    }
    payload = json.dumps(
        {
            "keywords": [],
            "publicationPeriod": None,
            "occupationUris": [],
            "skillUris": [],
            "requiredExperienceCodes": [],
            "positionScheduleCodes": [],
            "sectorCodes": [],
            "educationLevelCodes": [],
            "positionOfferingCodes": [],
            "locationCodes": locationCodes,
            "euresFlagCodes": [],
            "otherBenefitsCodes": [],
            "requiredLanguages": [],
            "resultsPerPage": RESULTS_PER_PAGE,
            "sortSearch": "BEST_MATCH",
            "page": page_num,  # Set the current page number
            "minNumberPost": None,
        }
    )

    response = session.post(url, headers=headers, data=payload)
    data = json.loads(response.text)
    if "jvs" in data and data["jvs"] and len(data["jvs"]) > 0:
        return data["jvs"]
    else:
        return None


def job_to_tuple(job: dict):
    try:
        company = job.get("employer", {}).get("name", "")  # company
    except Exception:
        company = ""

    try:
        timestamp = job["creationDate"] / 1000
        date_posted = datetime.utcfromtimestamp(timestamp)
        date_posted = date_posted.strftime("%d %b %Y")
    except Exception:
        date_posted = ""

    return (
        "europa-" + job.get("id", ""),  # id
        f"https://europa.eu/eures/portal/jv-se/jv-details/{job.get('id', '')}?lang=en",  # link
        job.get("title", ""),  # title
        company,
        date_posted,  # date
        pycountry.countries.get(
            alpha_2=next(iter(job["locationMap"]))
        ).name,  # location
        remove_tags(job.get("description", "")),  # desc
    )


def store_jobs(jobs: dict):
    if not jobs:
        return

    connection = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        dbname=os.getenv("POSTGRES_DB"),
    )
    cur = connection.cursor()

    insert_statement = """
        INSERT INTO jobs (id, link, title, company, date_posted, location, description)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
    """

    for job in jobs:
        try:
            data_tuple = job_to_tuple(job)
            cur.execute(insert_statement, data_tuple)
            connection.commit()
            print(data_tuple)
        except Exception as e:
            print(f"Error: {e}")
            connection.rollback()


def run():
    with ThreadPoolExecutor() as executor:
        futures = []
        for location_code in LOCATION_CODES:
            for page_num in range(1, MAX_PAGES):
                futures.append(
                    executor.submit(fetch_jobs, page_num, locationCodes=[location_code])
                )
        for future in as_completed(futures):
            jobs = future.result()
            store_jobs(jobs)


if __name__ == "__main__":
    run()
