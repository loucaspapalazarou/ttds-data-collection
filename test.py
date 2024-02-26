import requests

session = requests.Session()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
}

session.get("https://www.cv-library.co.uk", headers=headers)

for c in session.cookies:
    print(c)

r = session.get("https://www.cv-library.co.uk/jobs", headers=headers)

print(r)
