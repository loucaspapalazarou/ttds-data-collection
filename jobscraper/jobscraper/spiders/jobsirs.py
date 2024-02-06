from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import Jobs24Item
from scrapy.loader import ItemLoader


class JobsirsSpider(CrawlSpider):
    name = "jobsirs"
    allowed_domains = ["www.jobs.irs.gov"]
    start_urls = ["https://www.jobs.irs.gov/careers"]

    rules = (
        Rule(LinkExtractor(allow=(r"page="))),
        Rule(LinkExtractor(allow=(r"/GetJob/"))),
        Rule(LinkExtractor(allow=(r"/job/")), callback="parse_item"),
    )

    def parse_item(self, response):
        print(response.url)
