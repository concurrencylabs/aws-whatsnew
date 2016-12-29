
## AWS What's New Web Scraper

This repo is a fun, quick-and-dirty Python script that I wrote to count the number of AWS announcements in a given year.

Every year, I'm curious about the number of AWS announcements and instead of counting them manually,
I spent a few minutes writing this Python script. It extracts information from the following site:
https://aws.amazon.com/about-aws/whats-new/2016


### Install and run

Clone this repo, create and activate a virtualenv and run:

```pip install -r requirements.txt```


To run it, just execute the following:

```python scrape.py --year=2016```


That's it, the script will generate three files:
announcements_year.txt , months_year.txt and wordcloud_year.txt


This is a chart that compares the number of announcements made in 2015 and 2016 by month:

![2016 vs 2015 announcements](https://www.concurrencylabs.com/img/announcements-line-chart.png)

And this is a word cloud with the 2016 announcements:

![2016 word cloud](https://www.concurrencylabs.com/img/announcements-wordcloud-2016.png)









