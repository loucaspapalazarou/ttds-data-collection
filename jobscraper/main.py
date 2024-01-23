from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.spiderloader import SpiderLoader
import schedule
import argparse
import logging
import time

logging.basicConfig(level=logging.DEBUG)


def main():
    process = CrawlerProcess(get_project_settings())

    # Load all spiders using SpiderLoader
    spider_loader = SpiderLoader.from_settings(process.settings)
    for spider_name in spider_loader.list():
        spider_cls = spider_loader.load(spider_name)
        process.crawl(spider_cls)

    process.start()


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
