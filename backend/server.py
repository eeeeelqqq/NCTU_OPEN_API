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

import pg

class IndexHandler(RequestHandler):
    @reqenv
    def get(self):
        self.finish(json.dumps({'version': 0.1}))
        return


if __name__ == '__main__':
    httpsock = tornado.netutil.bind_sockets(config.PORT)
    tornado.process.fork_processes(config.PROCESSES)
    db = pg.AsyncPG(config.DBNAME,config.DBUSER,config.DBPASSWORD,dbtz='+8')
    app = tornado.web.Application([
        ('/apis/', IndexHandler),
        ],cookie_secret = 'cookie',autoescape = 'xhtml_escape')
    srv = tornado.httpserver.HTTPServer(app)
    srv.add_sockets(httpsock)
    tornado.ioloop.IOLoop.instance().start()
