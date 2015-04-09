from req import RequestHandler
from req import reqenv
from req import Service

class NewsService:
    def __init__(self, db=None):
        self.db = db
        NewsService.inst = self

class NewsHandler(RequestHandler):
    @reqenv
    def get(self, nid=None):
        pass
