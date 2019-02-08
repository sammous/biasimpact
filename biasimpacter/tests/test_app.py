import pytest
import os
from app.app import read_source

@pytest.fixture
def datapath():
    datapath = os.path.join(os.path.dirname(__file__), "data")
    return os.path.join(datapath, 'source.txt')

@pytest.fixture
def source():
    datapath = os.path.join(os.path.dirname(__file__), "data")
    with open(os.path.join(datapath, 'source.txt'), 'r') as f:
        return [line.rstrip().split(", ") for line in f]

def test_read_source(datapath, source):
    test_source = read_source(datapath)
    assert test_source == source