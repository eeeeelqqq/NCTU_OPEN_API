from req import RequestHandler
from req import reqenv
from req import Service
import json
import time

from bs4 import BeautifulSoup
import urllib.request
import urllib.parse

class MailService:
    def __init__(self, db=None):
        self.db = db
        self.expire_time = 300
        self.urlbase = 'http://mailsys.nctu.edu.tw/MailNotify/main.asp?dorm='
        self.mapping = {'092': '十三舍', '094': '女二舍', '087': '八舍', '088': '九舍', '095': '研二舍', '093': '竹軒', '091': '十二舍', '086': '七舍', '090': '十一舍', '089': '十舍'}
        self.expire = {}
        for i in self.mapping:
            self.expire[i] = 0
        self.formatdata = ['id', 'name', 'date', 'type']
        MailService.inst = self

    def parse_mail_by_department(self, department):
        if department in self.mapping:
            departmentname = self.mapping[department]
            res = {'departmentid': department, 'departmentname': departmentname, 'content': []}
            url = self.urlbase + department
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

    def parse_mail(self, department=None):
        if department == None:
            res = []
            for department in self.mapping:
                res.append(self.parse_mail_by_department(department))
            return res
        elif department in self.mapping:
            return [self.parse_mail_by_department(department)]
        else:
            return []

    def get_mail_type(self, name):
        cur = yield self.db.cursor()
        yield cur.execute('SELECT "id" FROM "mail_type" WHERE "name" = %s;', (name,))
        if cur.rowcount != 1:
            yield cur.execute('INSERT INTO "mail_type" ("name") VALUES(%s) RETURNING "id";', (name,))
            return cur.fetchone()[0]
        return cur.fetchone()[0] 

    def get_mail_by_department(self, department, departmentid):
        departmentname = self.mapping[department]
        cur = yield self.db.cursor()
        if time.time() - self.expire[department] > self.expire_time:
            res = self.parse_mail_by_department(department)
            content = res['content']
            for c in content:
                yield cur.execute('SELECT "id" from "department_mail"'
                        ' WHERE "id" = %s;', (c['id'],))
                if cur.rowcount != 1:
                    date = c['date'].replace('/', '-')
                    _type = yield from self.get_mail_type(c['type'])
                    yield cur.execute('INSERT INTO "department_mail" '
                            '("id", "departmentid", "name", "date", "type", "exist") '
                            'VALUES(%s, %s, %s, %s, %s, %s);', 
                            (c['id'], departmentid, c['name'], date, _type, True))
            self.expire[department] = time.time()
        yield cur.execute('SELECT "id", "name", "date", "type", "exist" FROM "department_mail" '
                'WHERE "departmentid" = %s;', (departmentid,))
        res = []
        for (_id, name, date, _type, exist) in cur:
            res.append({'id': _id,
                'departmentid': departmentid,
                'departmentname': departmentname,
                'name': name,
                'date': date.strftime('%Y/%M/%d'),
                'type': _type,
                'exist': exist})
        return res

    def get_department_id(self, department):
        cur = yield self.db.cursor()
        yield cur.execute('SELECT "real_id" FROM "department" WHERE "id" = %s;', (department,))
        if cur.rowcount != 1:
            return -1
        else:
            return cur.fetchone()[0]

    def get_department(self, departmentid):
        cur = yield self.db.cursor()
        yield cur.execute('SELECT "id" FROM "department" WHERE "real_id" = %s;', (departmentid,))
        if cur.rowcount != 1:
            return ''
        else:
            return cur.fetchone()[0]


    def get_mail(self, department=None):
        cur = yield self.db.cursor()
        if department:
            departmentid = department
            department = yield from self.get_department_id(department)
            if department == -1:
                return []
            res = yield from self.get_mail_by_department(department, departmentid)
            return res
        else:
            res = []
            for department in self.mapping:
                departmentid = yield from self.get_department(department)
                tmp = yield from self.get_mail_by_department(department, departmentid)
                res.extend(tmp)
            return res


class MailHandler(RequestHandler):
    @reqenv
    def get(self, department=None):
        res = yield from MailService.inst.get_mail(department)
        self.finish(json.dumps(res))
        return

if __name__ == '__main__':
    m = MailService()
