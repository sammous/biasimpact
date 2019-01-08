import pytest
import datetime
import os
from app import create_app, Date, Validator, RSSReader
from mock import patch
from .conftest import _mock_response
from bs4 import BeautifulSoup

@pytest.fixture
def rss_feed():
    datapath = os.path.join(os.path.dirname(__file__), "data")
    with open(os.path.join(datapath, 'rssfeed_20mins.txt'), 'r') as f:
        return f.read()

@pytest.fixture
def soup(rss_feed):
    yield BeautifulSoup(rss_feed, "xml")

@pytest.fixture
def rss_reader(app):
    yield RSSReader(app)

def test_date():
    assert Date

def test_validator():
    assert Validator

@patch('app.prepare.requests.get')
def test_rssreader(_mock_get, rss_feed, app):
    mock_resp = _mock_response(content=rss_feed)
    _mock_get.return_value = mock_resp
    rss_reader = RSSReader(app)
    soup = BeautifulSoup(rss_feed, "xml")
    assert rss_reader.get_xml_feed("test_url")["soup"] == soup


def test_get_items(soup, rss_reader):
    items = rss_reader._get_items(soup, rss_reader.items)
    assert len(items) == 43

def test_get_dates(soup, rss_reader):
    dates = rss_reader._get_dates(soup, rss_reader.items_date)
    assert len(dates) == 43

def test_get_des(soup, rss_reader):
    desc = rss_reader._get_desc(soup, rss_reader.items_desc)
    assert len(desc) == 44
