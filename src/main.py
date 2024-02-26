"""
Main script for running web scraping tasks and scheduling their execution.

This script defines functions to run different web scraping tasks and schedule their execution if required.
It includes functions to run a job scraper using Scrapy, run the Europascraper module, and run a removal task
to delete old entries from the database. The main function initializes and starts multiple processes to run
these tasks concurrently. It also provides a signal handler to terminate processes gracefully upon receiving
a SIGINT signal (Ctrl+C).
"""

import argparse
import logging
import multiprocessing
import signal
import time

from scrapy.crawler import CrawlerProcess
from scrapy.spiderloader import SpiderLoader
from scrapy.utils.project import get_project_settings
import schedule

from europascraper import europa
from db import db
from constants import CONSTANTS

# Prepare the logger
logging.basicConfig(level=logging.DEBUG)


def run_jobscraper():
    """
    Run the job scraper by initializing and starting the Scrapy process for each spider defined in the project settings.
    """
    settings = get_project_settings()
    spider_loader = SpiderLoader.from_settings(settings)
    process = CrawlerProcess(settings)
    for spider_name in spider_loader.list():
        process.crawl(spider_name)
    process.start()


def run_europascraper():
    """
    Run the Europascraper module.
    """
    europa.run()


def run_removal_task():
    """
    Run the removal task scheduled to execute daily to remove old entries from the database.
    """
    schedule.every().day.at(CONSTANTS["scrape_time"]).do(db.remove_old_entries)
    logging.info(f"Deleting old rows every day at {CONSTANTS['scrape_time']} AM.")
    while True:
        schedule.run_pending()
        time.sleep(10)


def _main():
    """
    Main function to initialize and start multiple processes for running different tasks.
    """
    db.init_database()

    # Start both scrapers as separate processes
    process_jobscraper = multiprocessing.Process(target=run_jobscraper)
    process_europascraper = multiprocessing.Process(target=run_europascraper)
    process_removal = multiprocessing.Process(target=run_removal_task)

    # Define a signal handler for SIGINT (Ctrl+C)
    def signal_handler(sig, frame):
        logging.info("Received Ctrl+C. Terminating processes...")
        process_jobscraper.terminate()
        process_europascraper.terminate()
        process_removal.terminate()
        process_jobscraper.join()
        process_europascraper.join()
        process_removal.join()
        logging.info("Processes terminated.")
        exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    process_jobscraper.start()
    process_europascraper.start()
    process_removal.start()

    timeout = CONSTANTS["scrape_duration"]
    process_jobscraper.join(timeout=timeout)
    process_europascraper.join(timeout=timeout)
    process_removal.join(timeout=timeout)

    # Check if any process is still alive and terminate if necessary
    if process_jobscraper.is_alive():
        process_jobscraper.terminate()
    if process_europascraper.is_alive():
        process_europascraper.terminate()
    if process_removal.is_alive():
        process_removal.terminate()


def main():
    try:
        _main()
    except Exception:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--schedule",
        action="store_true",
        help=f"Schedule the task to run daily at {CONSTANTS['scrape_time']} AM",
    )
    args = parser.parse_args()
    if args.schedule:
        schedule.every().day.at(CONSTANTS["scrape_time"]).do(main)
        logging.info(
            f"Task scheduled to run every day at {CONSTANTS['scrape_time']} AM."
        )
        while True:
            schedule.run_pending()
            time.sleep(10)
    else:
        logging.info("Running task now.")
        main()
