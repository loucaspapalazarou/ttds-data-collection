from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader


class GovukSpider(CrawlSpider):
    name = "govuk"
    allowed_domains = ["findajob.dwp.gov.uk"]
    start_urls = ["https://findajob.dwp.gov.uk/search/"]

    rules = (
        Rule(LinkExtractor(allow=(r"p="))),
        Rule(LinkExtractor(allow=(r"/search/"))),
        Rule(LinkExtractor(allow=(r"/details/")), callback="parse_item"),
    )

    def parse_item(self, response):
        print(response.css("h1.govuk-heading-l::text").get())
        # l = ItemLoader(item=Jobs24Item(), response=response)
        # l.add_value("id", response.url.split("-")[-1])
        # l.add_value("link", response.url)
        # l.add_css("title", "h1.jobDetails__title")
        # l.add_css("company", "p.jobDetails")
        # l.add_css("date_posted", "p.small")
        # l.add_css("description", "div.jobDescription")
        # return l.load_item()
