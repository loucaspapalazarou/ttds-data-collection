from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import CVLibraryItem
from scrapy.loader import ItemLoader


class CVLibrarySpider(CrawlSpider):
    name = "cvlibrary"
    allowed_domains = ["www.cv-library.co.uk"]
    start_urls = ["https://www.cv-library.co.uk/jobs/"]
    rules = (
        Rule(LinkExtractor(allow=(r"/jobs"))),
        Rule(LinkExtractor(allow=(r"/job/"), deny=(r"/apply")), callback="parse_item"),
    )

    def parse_item(self, response):
        l = ItemLoader(item=CVLibraryItem(), response=response)
        l.add_value("id", response.url.split("/")[4])
        l.add_value("link", response.url)
        l.add_css("title", "span[data-jd-title]")
        l.add_css("company", "a[data-open-js]")
        l.add_css("date_posted", "span[data-jd-posted]")
        l.add_css("description", "div.job__description")
        return l.load_item()
