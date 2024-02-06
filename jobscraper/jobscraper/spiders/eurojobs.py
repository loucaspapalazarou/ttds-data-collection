from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import EurojobsItem
from scrapy.loader import ItemLoader


class EurojobsSpider(CrawlSpider):
    name = "eurojobs"
    allowed_domains = ["eurojobs.com"]
    start_urls = ["https://eurojobs.com/browse-by-country/"]

    rules = (
        Rule(LinkExtractor(allow=(r"/browse-by-country/"))),
        Rule(LinkExtractor(allow=(r"/job/.*")), callback="parse_item"),
    )

    def parse_item(self, response):
        l = ItemLoader(item=EurojobsItem(), response=response)
        l.add_value("id", response.url.split("/")[5])
        l.add_value("link", response.url)
        l.add_css("title", "h2")
        l.add_css("company", "span.company-name")
        l.add_xpath("date_posted", '//*[@id="col-narrow-right"]/div[3]/div')
        l.add_xpath("description", '//*[@id="col-wide"]/div/div')
        return l.load_item()
