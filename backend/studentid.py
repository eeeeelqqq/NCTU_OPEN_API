from req import RequestHandler
from req import reqenv
from req import Service
import json

class StudentidService:
    def __init__(self, db):
        self.db = db
        StudentidService.inst = self

    def get_data(self, filt):
        def gen(filt):
            def cat_string(a, b):
                if a != '':
                    return a + ' AND ' + b
                else:
                    return ' WHERE ' + b
            query = ''
            args = ()
            if filt['id']:
                query = cat_string(query, '"id" LIKE %s ')
                args = args + ('%%%s%%'%(filt['id'],),)
            if filt['name']:
                query = cat_string(query, ' "name" LIKE %s ')
                args = args + ('%%%s%%'%(filt['name'],),)
            return (query, args)
        query, args = gen(filt)
        cur = yield self.db.cursor()
        yield cur.execute('SELECT "id", "name" FROM "student_id" %s;'%(query,), args)
        res = []
        for (_id, name) in cur:
            res.append({'id': _id, 'name': name})
        return res


class StudentidHandler(RequestHandler):
    @reqenv
    def get(self):
        _id = self.get_argument('id', None)
        name = self.get_argument('name', None)
        filt = {'id': _id, 'name': name}
        res = yield from StudentidService.inst.get_data(filt)
        #self.finish(str(res))
        self.finish(json.dumps(res, ensure_ascii=False))

        return
    @reqenv
    def post(self):
        return
