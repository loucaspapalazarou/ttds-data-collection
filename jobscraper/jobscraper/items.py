# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst
from w3lib.html import remove_tags
from .utils import s1jobs_jobs24, cvlibrary


class S1JobsAndJobs24Item(scrapy.Item):
    link = scrapy.Field(
        output_processor=TakeFirst(),
    )
    title = scrapy.Field(
        input_processor=MapCompose(remove_tags, s1jobs_jobs24.clean_data),
        output_processor=TakeFirst(),
    )
    company = scrapy.Field(
        input_processor=MapCompose(remove_tags, s1jobs_jobs24.clean_data),
        output_processor=TakeFirst(),
    )
    description = scrapy.Field(
        input_processor=MapCompose(
            lambda x: remove_tags(x, keep=["br", "p"]), s1jobs_jobs24.clean_data
        ),
        output_processor=TakeFirst(),
    )
    date_posted = scrapy.Field(
        input_processor=MapCompose(
            remove_tags, s1jobs_jobs24.clean_data, s1jobs_jobs24.string_to_date
        ),
        output_processor=TakeFirst(),
    )


class Jobs24Item(S1JobsAndJobs24Item):
    id = scrapy.Field(
        input_processor=MapCompose(s1jobs_jobs24.mark_jobs24),
        output_processor=TakeFirst(),
    )


class S1JobsItem(S1JobsAndJobs24Item):
    id = scrapy.Field(
        input_processor=MapCompose(s1jobs_jobs24.mark_s1jobs),
        output_processor=TakeFirst(),
    )


class TotalJobsItem(scrapy.Item):
    pass


class CVLibraryItem(scrapy.Item):
    id = scrapy.Field(
        input_processor=MapCompose(cvlibrary.mark_cvlibrary),
        output_processor=TakeFirst(),
    )
    link = scrapy.Field(
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
