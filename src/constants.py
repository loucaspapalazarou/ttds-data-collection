from dotenv import load_dotenv
import os

load_dotenv()

CONSTANTS = {
    "postgres_host": os.getenv("POSTGRES_HOST"),
    "postgres_user": os.getenv("POSTGRES_USER"),
    "postgres_password": os.getenv("POSTGRES_PASSWORD"),
    "postgres_db": os.getenv("POSTGRES_DB"),
    "scrape_duration": 20,  # 14,400 seconds = 4 hours
    "scrape_time": "00:00",
    "deletion_interval": "20 days",
}
