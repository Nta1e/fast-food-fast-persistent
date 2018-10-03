import psycopg2
from psycopg2.extras import RealDictCursor


class Database(object):
    '''This class handles the connection to the database'''

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.conn = psycopg2.connect(
            "dbname='fastfoodfast'  user='grey' host='127.0.0.1' password='Grey'")
        self.cur = self.conn.cursor(cursor_factory=RealDictCursor)

    def query(self, query):
        self.cur.execute(query)

    def close(self):
        self.cur.close()
        self.conn.close()
