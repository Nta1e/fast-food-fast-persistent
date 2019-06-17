import time
from os import getenv

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

load_dotenv()


class Database(object):
    '''This class handles the connection to the database'''

    def __init__(self, app=None):
        self.app = app
        self.retries = 10
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        while(self.retries):
            try:
                self.conn = psycopg2.connect(
                    database=getenv('DB_NAME'),
                    host=getenv("DB_HOST"),
                    port=getenv("DB_PORT"),
                    user=getenv('DB_USER'),
                    password=getenv('DB_PASSWORD'))
                self.cur = self.conn.cursor(cursor_factory=RealDictCursor)
                break;
            except psycopg2.OperationalError:
                self.retries -= 1
                print(f"*** {self.retries} retries left! ***")
                time.sleep(2)

    def query(self, query):
        self.cur.execute(query)

    def close(self):
        self.cur.close()
        self.conn.close()
