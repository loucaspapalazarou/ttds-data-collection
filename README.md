# TTDS Data collection modeule

This module is fully dockerized and stores the data in a local mongodb instance.

Build
```
docker-compose build
```

and run

```
docker-compose up
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

### other random notes

Useful scrapy docs to not get blocked: https://docs.scrapy.org/en/latest/topics/practices.html 

Free proxues (not that good): https://api.proxyscrape.com/v3/free-proxy-list/get?request=getproxies