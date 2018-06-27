import psycopg2
import psycopg2.extras

def connect_db(uri):
    conn = psycopg2.connect(uri, cursor_factory=psycopg2.extras.DictCursor)
    conn.set_session(autocommit=True)
    return conn

def make_cursor(connection):
    return connection.cursor()
