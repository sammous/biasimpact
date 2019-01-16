import pytest
import datetime
import os
from app.app import Date, Validator, RSSReader
from mock import patch
from .conftest import _mock_response
from bs4 import BeautifulSoup

@pytest.fixture
def rss_feed():
    datapath = os.path.join(os.path.dirname(__file__), "data")
    with open(os.path.join(datapath, 'rss-20mins.xml'), 'r') as f:
        return f.read()

@pytest.fixture
def soup(rss_feed):
    yield BeautifulSoup(rss_feed, "xml")

@pytest.fixture
@patch('app.app.logging')
def rss_reader(mock_logging):
    return RSSReader(mock_logging)

@pytest.fixture
def items(soup, rss_reader):
    yield RSSReader._get_items(soup, rss_reader.items)

def test_date():
    assert Date

def test_validator():
    assert Validator


@patch('app.app.logging')
@patch('app.dataprovider.requests.get')
def test_rssreader(_mock_get, mock_logging, rss_feed):
    mock_resp = _mock_response(content=rss_feed)
    _mock_get.return_value = mock_resp
    rss_reader = RSSReader(mock_logging)
    soup = BeautifulSoup(rss_feed, "xml")
    assert rss_reader.get_xml_feed("test_url")["soup"] == soup

def test_coherent_rss_reader(soup, items, rss_reader):
    items = rss_reader._get_items(soup, rss_reader.items)
    dates = rss_reader._get_dates(items, rss_reader.items_date)
    links = rss_reader._get_links(items, rss_reader.items_link)
    titles = rss_reader._get_titles(items, rss_reader.items_title)
    desc = rss_reader._get_desc(items, rss_reader.items_desc)

    assert len(items) == len(dates) == len(links) == len(titles) == len(desc) == 43
