from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.spiderloader import SpiderLoader
import schedule
import argparse
import logging
import time
import os
import psycopg2
from europascraper import europa
from multiprocessing import Process


logging.basicConfig(level=logging.DEBUG)


def init_database():
    # Connect to the specific database
    connection = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        dbname=os.getenv("POSTGRES_DB"),
    )
    cursor = connection.cursor()

    # Create table if it doesn't exist
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS jobs(
            id text PRIMARY KEY,
            link VARCHAR(255),
            title VARCHAR(255),
            company VARCHAR(255),
            date_posted VARCHAR(255),
            location VARCHAR(255),
            description text,
            timestamp timestamp DEFAULT current_timestamp
        );
        """
    )
    # Create the trigger function
    cursor.execute(
        """
        CREATE OR REPLACE FUNCTION delete_old_rows()
        RETURNS TRIGGER AS $$
        BEGIN
            DELETE FROM jobs WHERE timestamp < NOW() - INTERVAL '7 days';
            RETURN NULL;
        END;
        $$ LANGUAGE plpgsql;
        """
    )
    cursor.execute(
        """
        CREATE OR REPLACE TRIGGER delete_old_rows_trigger
        AFTER INSERT ON jobs
        EXECUTE FUNCTION delete_old_rows();
        """
    )

    connection.commit()
    cursor.close()
    connection.close()


def run_jobscraper():
    settings = get_project_settings()
    spider_loader = SpiderLoader.from_settings(settings)
    process = CrawlerProcess(settings)
    for spider_name in spider_loader.list():
        process.crawl(spider_name)
    process.start()


def run_europascraper():
    europa.run()


def main():
    init_database()

    # Start both scrapers as separate processes
    process_jobscraper = Process(target=run_jobscraper)
    process_europascraper = Process(target=run_europascraper)

    try:
        process_jobscraper.start()
        process_europascraper.start()
    except KeyboardInterrupt:
        return

    timeout = 10
    process_jobscraper.join(timeout=timeout)
    process_europascraper.join(timeout=timeout)

    # Check if any process is still alive and terminate if necessary
    if process_jobscraper.is_alive():
        process_jobscraper.terminate()
    if process_europascraper.is_alive():
        process_europascraper.terminate()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--schedule",
        action="store_true",
        help="Schedule the task to run daily at 00:00 AM",
    )
    args = parser.parse_args()
    if args.schedule:
        schedule.every().day.at("00:00").do(main)
        logging.info("Task scheduled to run every day at 00:00 AM.")
        while True:
            schedule.run_pending()
            time.sleep(10)
    else:
        logging.info("Running task now.")
        main()
