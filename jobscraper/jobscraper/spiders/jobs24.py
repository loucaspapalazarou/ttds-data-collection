from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import Jobs24Item
from scrapy.loader import ItemLoader


class Jobs24Spider(CrawlSpider):
    name = "jobs24"
    allowed_domains = ["www.jobs24.co.uk"]
    start_urls = ["https://www.jobs24.co.uk/jobs/"]

    rules = (
        Rule(LinkExtractor(allow=(r"page="))),
        Rule(LinkExtractor(allow=(r"/jobs/"))),
        Rule(LinkExtractor(allow=(r"/job/")), callback="parse_item"),
    )

    def parse_item(self, response):
        l = ItemLoader(item=Jobs24Item(), response=response)
        l.add_value("id", response.url.split("-")[-1])
        l.add_value("link", response.url)
        l.add_css("title", "h1.jobDetails__title")
        l.add_css("company", "p.jobDetails")
        l.add_css("date_posted", "p.small")
        l.add_css("description", "div.jobDescription")
        return l.load_item()
