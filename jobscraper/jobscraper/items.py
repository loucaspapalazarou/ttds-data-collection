# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst
from w3lib.html import remove_tags
from .utils import jobs24, cvlibrary


class Jobs24Item(scrapy.Item):
    id = scrapy.Field(
        input_processor=MapCompose(jobs24.url_to_id),
        output_processor=TakeFirst(),
    )
    link = scrapy.Field(
        output_processor=TakeFirst(),
    )
    title = scrapy.Field(
        input_processor=MapCompose(remove_tags, jobs24.clean_data),
        output_processor=TakeFirst(),
    )
    company = scrapy.Field(
        input_processor=MapCompose(remove_tags, jobs24.clean_data),
        output_processor=TakeFirst(),
    )
    description = scrapy.Field(
        input_processor=MapCompose(
            lambda x: remove_tags(x, keep=["br", "p"]), jobs24.clean_data
        ),
        output_processor=TakeFirst(),
    )
    date_posted = scrapy.Field(
        input_processor=MapCompose(
            remove_tags, jobs24.clean_data, jobs24.string_to_date
        ),
        output_processor=TakeFirst(),
    )


class CVLibraryItem(scrapy.Item):
    id = scrapy.Field(
        input_processor=MapCompose(cvlibrary.mark_cvlibrary),
        output_processor=TakeFirst(),
    )
    link = scrapy.Field(
        input_processor=MapCompose(cvlibrary.clean_link),
        output_processor=TakeFirst(),
    )
    title = scrapy.Field(
        input_processor=MapCompose(remove_tags, cvlibrary.clean_data),
        output_processor=TakeFirst(),
    )
    company = scrapy.Field(
        input_processor=MapCompose(remove_tags, cvlibrary.clean_data),
        output_processor=TakeFirst(),
    )
    description = scrapy.Field(
        input_processor=MapCompose(
            lambda x: remove_tags(x, keep=["br", "p"]), cvlibrary.clean_data
        ),
        output_processor=TakeFirst(),
    )
    date_posted = scrapy.Field(
        input_processor=MapCompose(remove_tags, cvlibrary.clean_data),
        output_processor=TakeFirst(),
    )
