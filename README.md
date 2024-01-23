# Notes

### Note 1
Found and tried:
```
https://github.com/Bunsly/JobSpy
```

Seems to retrieve some postings but crashes way to often and in upredictable ways

### Note 2

Indeed.com does not support their public API anymore. Pre-made github wrappers don't work. Tried using python `requests` but they use Cloudflare security, almost impossible to break through.

https://stackoverflow.com/questions/49087990/python-request-being-blocked-by-cloudflare

Success only using Selenium, which is sloppy and unreliable. 0.5-3s per job posting. With average 400k jobs we need ~270h to scrape everythin. Can get 2x-3x fatser with multiproc

Found this: https://github.com/MrFuguDataScience/Webscraping

Looking into mimicing the cookie exchange process

### Note 3

Glassdoor API is only for partners and a manual acceptance is needed.

Tried `requests` but this also seems to have some type of security which I could not bypass

Try Selenium?

### Note 4

workable.com looks like it is for recruiters to post jobs etc. and there is no endpoint to find all jobs, just jobs that I have posted. Also the API is free for 15 days


### General

https://morihosseini.medium.com/python-web-scraping-a-beginners-guide-to-scraping-job-listings-9d185855e7cb

Ask about ethicacy

subdomain, county, search
au.indeed.com - Australia
be.indeed.com - Belgium
ca.indeed.com - Canada
de.indeed.com - Germany
fr.indeed.com - France
ie.indeed.com - Ireland
ma.indeed.com - Morocco - Maroc
nl.indeed.com - Netherlands
nz.indeed.com - New Zealand
uk.indeed.com - United Kingdom - United Kingdom
vn.indeed.com - Vietnam

useful: https://docs.scrapy.org/en/latest/topics/practices.html

get proxies: https://api.proxyscrape.com/v3/free-proxy-list/get?request=getproxies