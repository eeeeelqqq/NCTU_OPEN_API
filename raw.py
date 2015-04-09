from bs4 import BeautifulSoup
import urllib.request
import urllib.parse


class News:
    def __init__(self, year, month, idx):
        url = "https://infonews.nctu.edu.tw/view/bulletinDetail_go.php?id="
        self.base = "https://infonews.nctu.edu.tw"
        year = '{0:04}'.format(year)
        month = '{0:02}'.format(month)
        idx = '{0:05}'.format(idx)
        self.index = str(year) + str(month) + str(idx)
        url += self.index
        self.page = urllib.request.urlopen(url)
        self.soup = BeautifulSoup(self.page.read())
        self.title = None
        self.user = None
        self.department = None
        self.phone = None
        #self.type = None
        self.category = None
        self.target = None
        self.start = None
        self.end = None
        self.pos = None
        self.content = None
        self.attach = None
        self.parse()

    def parse(self):
        b = self.soup.find(id="BulletinDtl")
        #self._type = b.img['alt']
        table = b.table.find_all('tr')
        self.title = table[1].string
        provider = table[2].string.split('：')[1]
        p = provider.split('/')
        self.user = p[0]
        self.department = p[1]
        meta = self.soup.find('tr', {"class": "style6"}).find_all('td')
        self.category = meta[0].string
        self.target = meta[1].string
        self.start = meta[2].string
        self.end = meta[3].string
        self.pos = meta[4].a.string.strip()
        self.content = self.soup.find(style="max-width:680px").div
        attach = []
        for i in self.soup.findAll('a', {"target": "_BLANK"}):
            a = {}
            a['attach_url'] = self.base + i['href'][2:]
            a['attach_name'] = i.string
            attach.append(a)

    def __str__(self):
        return self.index

    def print(self):
        print(self.index, self.content ,self.title)

n = News(2015, 4, 1)
n.print()
