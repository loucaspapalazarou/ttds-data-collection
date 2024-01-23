from scrapy.crawler import CrawlerProcess
from jobscraper.spiders.jobs24 import Jobs24Spider
from jobscraper.spiders.s1jobs import S1JobsSpider
from jobscraper.spiders.cvlibrary import CvlibrarySpider
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())

process.crawl(Jobs24Spider)
process.crawl(S1JobsSpider)
process.crawl(CvlibrarySpider)
process.start()
