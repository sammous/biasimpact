# Bias Impact [![Build Status](https://travis-ci.org/sammous/biasimpact.svg?branch=master)](https://travis-ci.org/sammous/biasimpact)

## BiasImpacter

Back end of the BiasImpact application

Tested on : 
* docker : Docker version 18.09.0, build 4d60db4
* docker-compose : docker-compose version 1.23.2, build 1110ad01
### Installation

Environnement Variable needed :
````python
mongo_host = os.getenv("BIASIMPACTER_DC_MONGO_HOST")
mongo_port = os.getenv("MONGO_PORT")
mongo_db = os.getenv("APP_MONGO_DB")
mongo_user = os.getenv("APP_MONGO_USER")
mongo_pw = os.getenv("APP_MONGO_PASS")
````

The `script` folder contains a `bash` script that creates a user to MongoDB.

Create an `.env` for _docker-compose_ where you replace ****** with values you want.
```bash
MONGO_ROOT_USERNAME=**********
MONGO_ROOT_PASSWORD=**********
MONGO_HOST=localhost
MONGO_PORT=27017

APP_MONGO_DB=biasimpact
APP_MONGO_USER=**********
APP_MONGO_PASS=**********

BIASIMPACTER_OUTPUT=biasimpacter_output.log
BIASIMPACTER_DC_MONGO_HOST=mongo
...
```
Check the file `.env.example`.

A cronjob is created to trigger daily scraping. It can be seen in the file `biasimpacter/crontab.sh`.

#### Source file

`source.txt` is the source file read to get RSS feeds with the following format : "*media_region*, *url_feed*" for each line.

#### Dataprovider

The dataprovider is composed by the `RSSReader` and the `StoryRSS`.
The `RSSReader` reads rss feeds and the `StoryRSS` aggregates the feeds to save it in a database.
