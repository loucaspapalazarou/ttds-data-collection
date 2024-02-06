# import requests module
import requests

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"

# create a session object
session = requests.Session()

session.get(url="https://european-union.europa.eu/index_en")

session.get(
    "https://europa.eu/eures/eures-apps/searchengine/page/common/security/profile?lang=en"
)

headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-GB,en;q=0.9,el-CY;q=0.8,el;q=0.7,en-US;q=0.6",
    "Connection": "keep-alive",
    "Content-Length": "399",
    "Content-Type": "application/json",
    # "Cookie": "EURES_JVSE_SESSIONID=A7701A2992219434D66BB01F64F25C8D; XSRF-TOKEN=26a9ad4e-0ea8-4305-839f-56dc85f18c1b; cck1=%7B%22cm%22%3Atrue%2C%22all1st%22%3Atrue%2C%22closed%22%3Atrue%7D",
    "Host": "europa.eu",
    "Origin": "https://europa.eu",
    "Referer": "https://europa.eu/eures/portal/jv-se/search?page=1&resultsPerPage=10&orderBy=BEST_MATCH&lang=en",
    "Sec-Ch-Ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    # "X-Xsrf-Token": "26a9ad4e-0ea8-4305-839f-56dc85f18c1b",
}


target_url = "https://europa.eu/eures/eures-apps/searchengine/page/jv-search/search"
res = session.post(url=target_url, headers=headers)

print(session.cookies)
print(res)
