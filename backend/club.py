from req import RequestHandler
from req import reqenv
from req import Service
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import json

class ClubService:
    def __init__(self, db=None):
        self.db = db
        self.urlbase = "https://infonews.nctu.edu.tw/index.php?SuperType=3&action=moreclub&pagekey=%s&categoryid=all"
        ClubService.inst = self

    def get_club_by_page(self, _page):
        if _page and _page != '0':
            url = self.urlbase% str(_page)
            page = urllib.request.urlopen(url)
            soup = BeautifulSoup(page.read())
            soup = soup.table.find_all("tr")
            club = []
            for idx, i in enumerate(soup[1:]):
                r = idx % 3
                if r == 0:
                    tmp = {}
                    tmp['title'] = i.find_all("td")[1].string
                elif r == 1:
                    date = i.find_all("td")[1].string.split('-')
                    tmp['start'] = date[0]
                    tmp['end'] = date[1]
                elif r == 2:
                    tmp['club'] = i.find_all("td")[1].string
                    club.append(tmp)
            return {'page': _page, 'content': club}
        else:
            return {}


class ClubHandler(RequestHandler):
    @reqenv
    def get(self, page=None):
        if page:
            self.finish(json.dumps(ClubService.inst.get_club_by_page(page)))
        else:
            self.finish(json.dumps({}))
        return 

if __name__ == '__main__':
    c = ClubService()
    print(c.get_club_by_page(10))
