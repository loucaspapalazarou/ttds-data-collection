# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2
import pymongo
from scrapy.utils.project import get_project_settings


class JobscraperPostgresPipeline:
    def __init__(self) -> None:
        settings = get_project_settings()

        ## Create/Connect to database
        self.connection = psycopg2.connect(
            host=settings.get("POSTGRES_HOSTNAME"),
            user=settings.get("POSTGRES_USERNAME"),
            password=settings.get("POSTGRES_PASSWORD"),
            dbname=settings.get("POSTGRES_DATABASE"),
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
                description text
            );
            """
        )
        self.connection.commit()

    def process_item(self, item, spider):
        # Define insert statement with placeholders for each column
        insert_statement = """
            INSERT INTO jobs (id, link, title, company, date_posted, description)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """

        # Tuple with values for each placeholder in the insert statement
        data_tuple = (
            item.get("id", ""),  # Using .get() to avoid KeyErrors if a field is missing
            item.get("link", ""),
            item.get("title", ""),
            item.get("company", ""),
            item.get("date_posted", ""),
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
        self.collection.insert_one(dict(item))
        return item
