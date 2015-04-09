import tornado.ioloop
import tornado.web 
import tornado.httpserver
import tornado.process
import tornado.netutil
from req import Service
from req import reqenv
from req import RequestHandler
import config
import json

from mail import MailService
from mail import MailHandler
from club import ClubService
from club import ClubHandler

import pg

class IndexHandler(RequestHandler):
    @reqenv
    def get(self):
        self.finish(json.dumps({'version': 0.1, 'method': 'GET'}))
        return
    
    @reqenv
    def post(self):
        self.finish(json.dumps({'version': 0.1, 'method': 'POST'}))
        return


if __name__ == '__main__':
    httpsock = tornado.netutil.bind_sockets(config.PORT)
    tornado.process.fork_processes(config.PROCESSES)
    db = pg.AsyncPG(config.DBNAME,config.DBUSER,config.DBPASSWORD,dbtz='+8')
    app = tornado.web.Application([
        ('/api/', IndexHandler),
        ('/api/dorm/', MailHandler),
        ('/api/dorm/(\d+)/', MailHandler),
        ('/api/club/', ClubHandler),
        ('/api/club/(\d+)/', ClubHandler),
        ],cookie_secret = config.COOKIES,autoescape = 'xhtml_escape')
    srv = tornado.httpserver.HTTPServer(app)
    srv.add_sockets(httpsock)
    Service.Mail = MailService(db)
    Service.Club = ClubService(db)
    tornado.ioloop.IOLoop.instance().start()
