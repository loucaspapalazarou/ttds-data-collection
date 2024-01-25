# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
from scrapy.utils.project import get_project_settings


class JobscraperMongoPipeline:
    def __init__(self) -> None:
        settings = get_project_settings()
        self.connection = pymongo.MongoClient(
            host=settings.get("MONGODB_HOSTNAME"),
            port=settings.get("MONGODB_PORT"),
        )
        db = self.connection[settings.get("MONGODB_DBATABASE")]
        self.collection = db[settings.get("MONGODB_COLLECTION")]

    def process_item(self, item, spider):
        # Prepare the filter and update document
        filter_doc = {"id": item["id"]}  # Assuming 'id' is the field in item
        update_doc = {"$setOnInsert": dict(item)}  # Fields to set on insert

        # Update the collection, insert if the id does not exist
        self.collection.update_one(
            filter_doc, update_doc, upsert=True  # Ensures insert if not exists
        )
        return item
