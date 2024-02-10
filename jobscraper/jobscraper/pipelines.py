# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
import psycopg2
import pymongo
from scrapy.utils.project import get_project_settings
from pymongo.server_api import ServerApi


class JobscraperMongoPipeline:
    def __init__(self) -> None:
        settings = get_project_settings()
        self.connection = pymongo.MongoClient(
            host=os.getenv("MONGODB_HOSTNAME"),
            port=os.getenv("MONGODB_PORT"),
            server_api=ServerApi("1"),
        )
        db = self.connection[os.getenv("MONGODB_DBATABASE")]
        self.collection = db[os.getenv("MONGODB_COLLECTION")]

    def process_item(self, item, spider):
        # Prepare the filter and update document
        filter_doc = {"id": item["id"]}  # Assuming 'id' is the field in item
        update_doc = {"$setOnInsert": dict(item)}  # Fields to set on insert

        # Update the collection, insert if the id does not exist
        self.collection.update_one(
            filter_doc, update_doc, upsert=True  # Ensures insert if not exists
        )
        return item


class JobscraperPostgresPipeline:
    def __init__(self) -> None:
        ## Create/Connect to database
        self.connection = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST", "localhost"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            dbname=os.getenv("POSTGRES_DB"),
        )

        self.cur = self.connection.cursor()

        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS jobs(
                id text PRIMARY KEY,
                link VARCHAR(255),
                title VARCHAR(255),
                company VARCHAR(255),
                date_posted VARCHAR(255),
                location VARCHAR(255),
                description text
            );
            """
        )
        self.connection.commit()

    def process_item(self, item, spider):
        # Define insert statement with placeholders for each column
        insert_statement = """
            INSERT INTO jobs (id, link, title, company, date_posted, location, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """

        # Tuple with values for each placeholder in the insert statement
        data_tuple = (
            item.get("id", ""),  # Using .get() to avoid KeyErrors if a field is missing
            item.get("link", ""),
            item.get("title", ""),
            item.get("company", ""),
            item.get("date_posted", ""),
            item.get("location", ""),
            item.get("description", ""),
        )

        try:
            self.cur.execute(insert_statement, data_tuple)
            self.connection.commit()
        except Exception as e:
            print(f"Error: {e}")
            self.connection.rollback()
        finally:
            return item

    def close_spider(self, spider):
        ## Close cursor & connection to database
        self.cur.close()
        self.connection.close()
