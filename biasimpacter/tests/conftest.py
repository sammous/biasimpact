import pytest
import sys
import os
from mock import patch, Mock, MagicMock

sys.path.append(
    os.path.join(
        os.path.dirname(__file__),
        '..',
        'app'))

def _mock_response(
        status=200,
        content="CONTENT",
        json_data=None,
        headers=None,
        raise_for_status=None,
        iter_content=None):
    '''
    Mocking get requests response.
    '''
    mock_resp = Mock()
    # mock raise_for_status call w/optional error
    mock_resp.raise_for_status = Mock()
    if raise_for_status:
        mock_resp.raise_for_status.side_effect = raise_for_status
    # set status code and content
    mock_resp.status_code = status
    mock_resp.content = content
    mock_resp.text = content
    mock_resp.headers = headers
    mock_resp.iter_content = MagicMock()
    mock_resp.iter_content.__iter__.return_value = iter_content
    # add json data if provided
    if json_data:
        mock_resp.json = Mock(
            return_value=json_data
        )
    return mock_resp

def _mock_mongo(
        uri=None,
        database=None,
        collection=None,
        build_index=None):
    mock_mongo = Mock()
    mock_collection = MagicMock()
    mock_mongo.collection = mock_collection
    mock_collection.insert_one = Mock()
    return mock_mongo

