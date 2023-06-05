import requests

class TaipowerCrawler:
    def __init__(self):
        pass

    def get_data(self):
        r = requests.get('https://data.taipower.com.tw/opendata/apply/file/d006019/001.csv')
        r = r.text.split('\r\n')
        print(r[1].split(',')[1:])