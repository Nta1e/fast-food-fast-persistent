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
            "dbname='d9qctcer3pq18m'  user='jbuzgihuevyrav' port='5432' host='ec2-23-23-80-20.compute-1.amazonaws.com' password='f19a69dd3f99061fc38411a8af5ff7c0a9450f546eccf890034d8f7c68410228'")
        self.cur = self.conn.cursor(cursor_factory=RealDictCursor)

    def query(self, query):
        self.cur.execute(query)

    def close(self):
        self.cur.close()
        self.conn.close()
