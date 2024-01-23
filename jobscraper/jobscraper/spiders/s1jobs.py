from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import S1JobsItem
from scrapy.loader import ItemLoader


class S1JobsSpider(CrawlSpider):
    name = "s1jobs"
    allowed_domains = ["www.s1jobs.com"]
    start_urls = ["https://www.s1jobs.com/jobs/"]

    rules = (
        Rule(LinkExtractor(allow=(r"page="))),
        Rule(LinkExtractor(allow=(r"/jobs/"))),
        Rule(LinkExtractor(allow=(r"/job/")), callback="parse_item"),
    )

    def parse_item(self, response):
        l = ItemLoader(item=S1JobsItem(), response=response)
        l.add_value("id", response.url.split("-")[-1])
        l.add_value("link", response.url)
        l.add_css("title", "h1.jobDetails__title")
        l.add_css("company", "p.jobDetails")
        l.add_css("date_posted", "p.small")
        l.add_css("description", "div.jobDescription")
        return l.load_item()
