from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import TotalJobsItem
from scrapy.loader import ItemLoader


class TotaljobsSpider(CrawlSpider):
    name = "totaljobs"
    allowed_domains = ["www.totaljobs.com"]
    start_urls = ["https://www.totaljobs.com/jobs/"]

    rules = (
        Rule(LinkExtractor(allow=(r"page="))),
        Rule(LinkExtractor(allow=(r"/jobs/"))),
        Rule(LinkExtractor(allow=(r"/job/")), callback="parse_item"),
    )

    def parse_item(self, response):
        l = ItemLoader(item=TotalJobsItem(), response=response)
        l.add_value("id", response.url.split("-")[-1])
        l.add_value("link", response.url)
        l.add_css("title", "h1#job-title")
        l.add_css("company", "a#companyJobsLink")
        # l.add_css("date_posted", "p.small")
        # l.add_css("description", "div.jobDescription")
        return l.load_item()
