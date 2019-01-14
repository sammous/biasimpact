#coding: utf-8
import requests
import datetime
from bs4 import BeautifulSoup
from dateutil.parser import parse

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
    ITEMS_LINK = [
        "link"
    ]
    ITEMS_TITLE = [
        "title"
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
        self.items_desc = ElementsXML.ITEMS_DESC
        self.items_link = ElementsXML.ITEMS_LINK
        self.items_title = ElementsXML.ITEMS_TITLE

    @staticmethod
    def _get_items(soup, items):
        """
        Get items from the RSS feed.
        """
        for el in items:
            items = soup.findAll(el)
            if len(items) > 0:
                return items
        return [None for i in range(len(list(items)))]
    
    @staticmethod
    def _get_dates(items, items_date):
        """
        Get dates from items.
        """
        dates = []
        for el in items_date:
            for i in items:
                d = i.findAll(el)
                if len(d) > 0:
                    dates.append(d[0].text)
            if len(dates) > 0:
                return dates
        return [None for i in range(len(list(items)))]

    @staticmethod
    def _get_desc(items, items_desc):
        """
        Get descriptions from items.
        """
        desc = []
        for el in items_desc:
            for i in items:
                d = i.findAll(el)
                if len(d) > 0:
                    desc.append(d[0].text)
            if len(desc) > 0:
                return desc
        return [None for i in range(len(list(items)))]

    @staticmethod
    def _get_links(items, items_link):
        """
        Get links from items.
        """
        links = []
        for el in items_link:
            for i in items:
                l = i.findAll(el)
                if len(l) > 0:
                    links.append(l[0].text)
            if len(links) > 0:
                return links
        return [None for i in range(len(list(items)))]

    @staticmethod
    def _get_titles(items, items_title):
        """
        Get titles from items.
        """
        titles = []
        for el in items_title:
            for i in items:
                t = i.findAll(el)
                if len(t) > 0:
                    titles.append(t[0].text)
            if len(titles) > 0:
                return titles
        return [None for i in range(len(list(items)))]

    @staticmethod
    def empty_to_nones(l, size):
        if l == []:
            return [None for i in range(size)]
        else:
            return l

    def get_xml_feed(self, url):
        """
        Format RSS feed and extract items and its information.
        """
        try:
            page = requests.get(url, headers=self.header)
            soup = BeautifulSoup(page.text, "xml")
        except requests.exceptions.RequestException as e:
            self.app.logger.error(e)
            return
        items = self._get_items(soup, self.items)
        items_soup = list(map(lambda x: BeautifulSoup(str(x), "xml"), items))
        desc = self.empty_to_nones(self._get_desc(
            items_soup, self.items_desc), len(items))
        dates = self.empty_to_nones(self._get_dates(items_soup, self.items_date), len(items))
        links = self.empty_to_nones(self._get_links(items_soup, self.items_link), len(items))
        titles = self.empty_to_nones(self._get_titles(items_soup, self.items_title), len(items))

        if len(desc) == len(items) + 1:
            desc = desc[1:]

        return {
            "soup": soup,
            "feedElement": items,
            "feedDescElement": desc,
            "feedLinkElement": links,
            "feedTitleElement": titles,
            "feedDateElement": dates
        }

class StoryRSS(RSSReader):
    def __init__(self, app, name, url, database,
                language='fr', header={"User-Agent": "Mozilla/5.0"}):
        self.url = url
        self.name = name
        self.database = database
        self.rss = RSSReader(app=app,language=language, header=header).get_xml_feed(url)
        self.app = app

    def save_story(self):
        try:
            element = self.rss['feedElement']
            desc_element = self.rss['feedDescElement']
            date_element = self.rss['feedDateElement']
            link_element = self.rss['feedLinkElement']
            title_element = self.rss['feedTitleElement']
            for el, desc, date, title, link in zip(element, desc_element, date_element, title_element, link_element):
                data = {
                    "raw_item": str(el) if el else None,
                    "date_article": parse(date, ignoretz=True) if date else None,
                    "desc": str(desc) if desc else None,
                    "title": str(title) if title else None,
                    "link": str(link) if link else None,
                    "date_parsed": datetime.datetime.utcnow(),
                    "media": self.name,
                }
                self.database.rss_feed.insert_one(data)
        except Exception as e:
            self.app.logger.debug(e)
