from req import RequestHandler
from req import reqenv
from req import Service
import json

from bs4 import BeautifulSoup
import urllib.request
import urllib.parse

class MailService:
    def __init__(self, db=None):
        self.db = db
        self.urlbase = 'http://mailsys.nctu.edu.tw/MailNotify/main.asp?dorm='
        self.mapping = {'092': '十三舍', '094': '女二舍', '087': '八舍', '088': '九舍', '095': '研二舍', '093': '竹軒', '091': '十二舍', '086': '七舍', '090': '十一舍', '089': '十舍'}
        self.formatdata = ['id', 'name', 'date', 'type']
        MailService.inst = self

    def get_mail_by_dorm(self, dorm):
        if dorm in self.mapping:
            dormname = self.mapping[dorm]
            res = {'dormid': dorm, 'dormname': dormname, 'content': []}
            url = self.urlbase + dorm
            page = urllib.request.urlopen(url)
            soup = BeautifulSoup(page.read().decode('hkscs'))
            try:
                tables = soup.body.table.find_all('tr')
            except:
                tables = None
            if tables:
                tables = tables[1:]
                for t in tables:
                    lines = t.find_all('font')
                    tmpdata = {'exist': True}
                    for index in range(0,4):
                        tmpdata[self.formatdata[index]] = lines[index].contents[0].strip()
                    res['content'].append(tmpdata)
            return res
        else:
            return {}

    def get_mail(self, dorm=None):
        if dorm == None:
            res = []
            for dorm in self.mapping:
                res.append(self.get_mail_by_dorm(dorm))
            return res
        elif dorm in self.mapping:
            return self.get_mail_by_dorm(dorm)
        else:
            return {}

class MailHandler(RequestHandler):
    @reqenv
    def get(self, dorm=None):
        res = MailService.inst.get_mail(dorm)
        self.finish(json.dumps(res))
        return

if __name__ == '__main__':
    m = MailService()
    print(m.get_mail())
