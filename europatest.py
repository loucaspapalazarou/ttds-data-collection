import requests
import json
from concurrent.futures import ThreadPoolExecutor

def fetch_jobs(page_num):
    # create session
    session = requests.Session()
    # get an unprotected route in order to get the cookies
    response = session.get("https://europa.eu/eures/eures-apps/searchengine/page/common/security/profile?lang=en")

    url = "https://europa.eu/eures/eures-apps/searchengine/page/jv-search/search"

    cookies = session.cookies.get_dict()
    headers = {
        'Cookie':f'EURES_JVSE_SESSIONID={cookies["EURES_JVSE_SESSIONID"]}; XSRF-TOKEN={cookies["XSRF-TOKEN"]};',
        'X-XSRF-TOKEN': f'{cookies["XSRF-TOKEN"]}',
        'Content-Type': 'application/json'
    }
    payload = json.dumps({
        "keywords": [],
        "publicationPeriod": None,
        "occupationUris": [],
        "skillUris": [],
        "requiredExperienceCodes": [],
        "positionScheduleCodes": [],
        "sectorCodes": [],
        "educationLevelCodes": [],
        "positionOfferingCodes": [],
        "locationCodes": [],
        "euresFlagCodes": [],
        "otherBenefitsCodes": [],
        "requiredLanguages": [],
        "resultsPerPage": 50,
        "sortSearch": "BEST_MATCH",
        "page": page_num,  # Set the current page number
        "minNumberPost": None
    })

    response = session.post(url, headers=headers, data=payload)
    data = json.loads(response.text)
    if "jvs" in data and data["jvs"]:
        print(f"Page {page_num}: {data['jvs'][0]['id']}. Total jobs {page_num*50}")
    else:
        print(f"Error {page_num}. {response}. {response.text}")

# Define the range of pages to scrape
pages_range = range(1, 10001)  # Adjust the range as needed

# Define the number of threads to use
num_threads = 10

# # Create a ThreadPoolExecutor with the defined number of threads
# with ThreadPoolExecutor(max_workers=num_threads) as executor:
#     # Map the fetch_jobs function to each page number in the range using multiple threads
#     executor.map(fetch_jobs, pages_range)

fetch_jobs(201)