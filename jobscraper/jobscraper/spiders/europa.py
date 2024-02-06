from typing import Iterable
import scrapy
from scrapy.http import Request


class EuropaSpider(scrapy.Spider):
    name = "europa"

    def start_requests(self):
        yield scrapy.Request(
            "https://europa.eu/eures/portal/jv-se/search?page=1&resultsPerPage=10&orderBy=BEST_MATCH&lang=en",
            meta={"playwright": True},
        )

    def parse(self, response):
        yield {"text": response.text}
