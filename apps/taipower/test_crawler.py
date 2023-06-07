import pytest
import requests

from server import CrawlerServicer

class MockResponse:

    def __init__(self, status):

        self.status_code = 0
        self.text = ''

        if status == 200:
            self._generate_200()

        if status == 400:
            self._generate_400()

        if status == 500:
            self._generate_500()

    def _generate_200(self):
        self.status_code = 200
        
        with open('app/taipower/test/001.csv', 'rb') as f:
            self.text = f.read().decode('utf8')

    def _generate_400(self):
        self.status_code = 404
        self.text = '{msg: not found}'

def test_get_url_success(mocker):

    service = CrawlerServicer()

    mocker.patch("requests.get", return_value=MockResponse(200))

    result, timestamp = service._data_parser("https://data.taipower.com.tw/opendata/apply/file/d006019/001.csv")

    print(result, timestamp)

    assert result == {'North Generate': '1019.8', 'North Consumption': '1312.4', 'Central Generate': '904.7', 'Central Consumption': '961.1', 'South Generate': '1576.2', 'South Consumption': '1193.5', 'East Generate': '14.2', 'East Consumption': '47.9'}
    assert timestamp == '2023-06-07 12:50'

def test_get_url_failed(mocker):

    service = CrawlerServicer()

    mocker.patch("requests.get", return_value=MockResponse(400))

    result, timestamp = service._data_parser("https://data.taipower.com.tw/opendata/apply/file/d006019/001.csv")

    assert result == {}
    assert timestamp == None

def test_generate_query(mocker):

    service = CrawlerServicer()

    timestamp = '2023-06-07 12:50'
    location = 'North Generate'
    value = 35.2

    result = service._generate_query(location, value, timestamp)

    assert str(result) == 'None,location=North\\ Generate value=35.2 1686142200000000000'
