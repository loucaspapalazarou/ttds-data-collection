import requests
import json
from w3lib.html import remove_tags
import pycountry
from concurrent.futures import ThreadPoolExecutor, as_completed
import datetime
import random
from constants import LOCATION_CODES
from db import db

RESULTS_PER_PAGE = 50
MAX_PAGES = 200


def init_session() -> requests.Session:
    """
    Initialize a session with Europa website.

    Returns:
        requests.Session: A session object.
    """
    session = requests.Session()
    # get an unprotected route in order to get the cookies
    session.get(
        "https://europa.eu/eures/eures-apps/searchengine/page/common/security/profile?lang=en"
    )
    return session


def fetch_jobs(page_num: int, locationCodes: list[str] = []) -> dict:
    """
    Fetch job vacancies from Europa website.

    Args:
        page_num (int): Page number to fetch.
        locationCodes (list): List of location codes to filter job vacancies.

    Returns:
        dict: Job vacancies data.
    """
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
    response = session.post(url, headers=headers, data=payload, timeout=10)
    data = json.loads(response.text)
    if "jvs" in data and data["jvs"] and len(data["jvs"]) > 0:
        return data["jvs"]
    else:
        return None


def job_to_tuple(job: dict):
    """
    Convert job data to a tuple.

    Args:
        job (dict): Job data dictionary.

    Returns:
        tuple: Tuple containing job data.
    """
    # Extracting company name
    company = job.get("employer", {}).get("name", "")

    # Extracting date posted
    try:
        timestamp = job.get("creationDate", 0) / 1000
        date_posted = datetime.datetime.utcfromtimestamp(timestamp).strftime("%d %b %Y")
    except Exception as e:
        date_posted = ""

    # Extracting location
    location = ""
    try:
        location_code = next(iter(job.get("locationMap", {})))
        location_name = pycountry.countries.get(alpha_2=location_code).name
        location = location_name
    except Exception as e:
        pass

    return (
        "europa-" + job.get("id", ""),
        f"https://europa.eu/eures/portal/jv-se/jv-details/{job.get('id', '')}?lang=en",
        remove_tags(job.get("title", "")),
        company,
        date_posted,
        location,
        remove_tags(job.get("description", "")),
    )


def store_jobs(jobs: dict):
    """
    Store jobs in the database.

    Args:
        jobs (dict): Job vacancies data dictionary.
    """
    if not jobs:
        return

    for job in jobs:
        data_tuple = job_to_tuple(job)
        db.insert(data_tuple)
        print(data_tuple)


def run():
    """
    Run the Europascraper module to fetch and store job vacancies.
    """
    try:
        with ThreadPoolExecutor() as executor:
            futures = []
            random.shuffle(LOCATION_CODES)
            for location_code in LOCATION_CODES:
                for page_num in range(1, MAX_PAGES):
                    futures.append(
                        executor.submit(
                            fetch_jobs, page_num, locationCodes=[location_code]
                        )
                    )
            for future in as_completed(futures):
                jobs = future.result()
                store_jobs(jobs)
    except KeyboardInterrupt:
        exit()
