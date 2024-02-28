# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst
from w3lib.html import remove_tags
from .utils import jobs24, eurojobs


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
    date_posted = scrapy.Field(
        input_processor=MapCompose(
            remove_tags, jobs24.clean_data, jobs24.string_to_date
        ),
        output_processor=TakeFirst(),
    )
    location = scrapy.Field(
        input_processor=MapCompose(jobs24.link_to_location),
        output_processor=TakeFirst(),
    )
    description = scrapy.Field(
        input_processor=MapCompose(
            lambda x: remove_tags(x, keep=["br", "p"]), jobs24.clean_data
        ),
        output_processor=TakeFirst(),
    )


class EurojobsItem(scrapy.Item):
    id = scrapy.Field(
        input_processor=MapCompose(eurojobs.mark_eurojobs),
        output_processor=TakeFirst(),
    )
    link = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst(),
    )
    title = scrapy.Field(
        input_processor=MapCompose(remove_tags, eurojobs.clean_title),
        output_processor=TakeFirst(),
    )
    company = scrapy.Field(
        input_processor=MapCompose(remove_tags, eurojobs.clean_data),
        output_processor=TakeFirst(),
    )
    location = scrapy.Field(
        input_processor=MapCompose(remove_tags, eurojobs.clean_location),
        output_processor=TakeFirst(),
    )
    description = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )
    date_posted = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )
