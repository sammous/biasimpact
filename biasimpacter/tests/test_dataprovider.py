import pytest
import datetime
import os
from app.app import Date, Validator, RSSReader, StoryRSS
from mock import patch
from .conftest import _mock_response, _mock_mongo
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
def rss_reader():
    return RSSReader()

@pytest.fixture
def items(soup, rss_reader):
    yield RSSReader._get_items(soup, rss_reader.items)

def test_date():
    assert Date

def test_validator():
    assert Validator

@patch('app.dataprovider.requests.get')
def test_rssreader(_mock_get, rss_feed):
    mock_resp = _mock_response(content=rss_feed)
    _mock_get.return_value = mock_resp
    rss_reader = RSSReader()
    soup = BeautifulSoup(rss_feed, "xml")
    assert rss_reader.get_xml_feed("test_url")["soup"] == soup

def test_coherent_rss_reader(soup, items, rss_reader):
    items = rss_reader._get_items(soup, rss_reader.items)
    dates = rss_reader._get_dates(items, rss_reader.items_date)
    links = rss_reader._get_links(items, rss_reader.items_link)
    titles = rss_reader._get_titles(items, rss_reader.items_title)
    desc = rss_reader._get_desc(items, rss_reader.items_desc)

    assert len(items) == len(dates) == len(links) == len(titles) == len(desc) == 43


@patch('app.dataprovider.RSSReader.get_xml_feed')
@patch('app.models.ModelRSS')
@patch('app.dataprovider.requests.get')
def test_storyrss(_mock_get, _mock_mongo, xml_feed, rss_reader, rss_feed):
    mock_resp = _mock_response(content=rss_feed)
    _mock_get.return_value = mock_resp
    xml_feed.return_value = rss_reader.get_xml_feed("http://test.com")
    story = StoryRSS("test_media", "http://test.com", _mock_mongo)
    story.save_story()
    assert _mock_mongo.build_index.called_once
    assert _mock_mongo.collection.update_one.call_count == 43
