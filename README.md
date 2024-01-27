# TTDS Data collection module

This module is fully dockerized and stores the data in a local mongodb instance.

Build
```
docker-compose build
```

and run
```
docker-compose up -d
```

or
```
docker-compose up -d --build
```

Inspect the stored documents using

```
docker exec -it ttds-data-collection_mongodb_1 mongosh
```

Then from the mongo shell

```
use jobs_db
```

Connt the documents

```
db.jobs.countDocuments()
```

The data collected can be [exported from mongo](https://www.mongodb.com/docs/database-tools/mongoexport/) in various formats and subsequently extracted from the container if needed. 

### other random notes

Useful scrapy docs to not get blocked: https://docs.scrapy.org/en/latest/topics/practices.html 

Free proxies (not that good): https://api.proxyscrape.com/v3/free-proxy-list/get?request=getproxies
