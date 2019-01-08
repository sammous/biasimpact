#coding: utf-8
import requests
import datetime
from bs4 import BeautifulSoup


class ElementsXML:
    ITEMS = [
        "entry",
        "item"
    ]
    ITEMS_DESC = [
        "description",
        "summary",
        "content"
    ]
    ITEMS_DATE = [
        "pubDate",
        "updated",
        "date"
    ]


class Date:
    now = datetime.datetime.now()
    week = datetime.datetime.now().isocalendar()[1]
    month = str(datetime.datetime.now().year) + '.' + str(datetime.datetime.now().month)

class Validator:
    valid = True

class RSSReader(Validator, Date, ElementsXML):
    def __init__(self, app, language='fr', header={"User-Agent": "Mozilla/5.0"}):
        self.app = app
        self.language = language
        self.header = header
        self.app.logger.debug('Initializing RSSReader...')
        self.items = ElementsXML.ITEMS
        self.items_date = ElementsXML.ITEMS_DATE
        self.items_desc =ElementsXML.ITEMS_DESC

    @staticmethod
    def _get_items(soup, items):
        for el in items:
            items = soup.findAll(el)
            if len(items) > 0:
                return items
        return None
    
    @staticmethod
    def _get_dates(soup, items_date):
        for el in items_date:
            dates = soup.findAll(el)
            if len(dates) > 0:
                return dates
            return None

    @staticmethod
    def _get_desc(soup, items_desc):
        for el in items_desc:
            desc = soup.findAll(el)
            if len(desc) > 0:
                return desc
            return None

    def get_xml_feed(self, url):
        try:
            page = requests.get(url, headers=self.header)
            soup = BeautifulSoup(page.text, "xml")
        except requests.exceptions.RequestException as e:
            self.app.logger.error(e)

        items = self._get_items(soup, self.items)
        desc = self._get_desc(soup, self.items_desc)
        dates = self._get_dates(soup, self.items_date)

        return {
            "soup": soup,
            "feedElement": items,
            "feedDescElement": desc,
            "feedDateElement": dates
        }


class StoryRSS(RSSReader):
    def __init__(self, url):
        self.url = url
        
    
