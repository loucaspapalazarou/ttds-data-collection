from dotenv import load_dotenv
import os

load_dotenv()

CONSTANTS = {
    "scrape_duration": 12_000,
    "scrape_time": "00:00",
    "postgres_host": os.getenv("POSTGRES_HOST"),
    "postgres_user": os.getenv("POSTGRES_USER"),
    "postgres_password": os.getenv("POSTGRES_PASSWORD"),
    "postgres_db": os.getenv("POSTGRES_DB"),
    "deletion_interval": "7 days",
}

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
