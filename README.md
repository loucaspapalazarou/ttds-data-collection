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

## Notes

- The code is split into 2 parts. The scrapy part collects data using the scrapy framework from various sites in the UK and one for the EU. The second part is a custom-made scraper for the official EU jobs website.
  
- Both are run in the `main.py` function using separate processes. Both store their data in the same PostgreSQL instance.
  
- If left alone, both scrapers will run for a long and unpredictable amount of time. Thus, a timeout of 12,000 seconds is set in the `main.py` file.
  
- Although the code can be run instantly using `main.py`, we can schedule the execution by providing the `-s` flag. This will schedule the task to run every day at 00:00.
