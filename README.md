# UPDATE
- update to reflect current code
- start cloud db instance and instructions 

# TTDS Data collection module

This repository contains the code for the data collection part of the TTDS assignment.

## Instructions

The data is stored in a PostgreSQL instance running locally on Docker. To start the local instance:

```
docker compose up -d
```

The credentials can be found in the `.env` file in the root repository. If you do not have one, copy the example:


```
cp .env.example .env
```

At a later stage, the credentials will be changed to reflect the remote database.

To run the code (strongly suggest you use a virtual environment):

```
pip install -r requirements.txt
```

```
cd jobscraper
```

```
python main.py
```

## Data

The data is structured like so:

- `id`: The job id, prefixed with the site it was collected from
- `link`: The job's link
- `title`: Job title
- `company`: Company that posted the job
- `location`: The best approximation of the job's location. Not always provided, and if so, it is assumed using the website context.
- `date_posted`: The date that the job was posted
- `description`: The job listing description
- `timestamp`: Automatically added field in order to auto-delete entries older than X amount of days.

## Constants

The `src/` directory contains the file `constants.py`. This file contains all the constants used in the code. These include: 

- Loading and handling of the database credentials
- The `scrape_duration` which denotes the amount of time that the code wil run for.
- The `scrape_time` which denotes the time of day that the code will be run.
- The `deletion_interval` denotes how old an entry should be for it to be removed from the database.

## Notes

- The code is split into 2 parts. The scrapy part collects data using the scrapy framework from various sites in the UK and one for the EU. The second part is a custom-made scraper for the official EU jobs website.
  
- Both are run in the `main.py` function using separate processes. Both store their data in the same PostgreSQL instance.
  
- If left alone, both scrapers will run for a long and unpredictable amount of time. Thus, a timeout of 14,400 seconds (=4 hours) is set in the `constants.py` file.
  
- Although the code can be run instantly using `main.py`, we can schedule the execution by providing the `-s` flag. This will schedule the task to run every day at the time specified in the `constants.py` file.
