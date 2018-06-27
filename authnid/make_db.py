import psycopg2
import psycopg2.extras

def connect_db(uri):
    conn = psycopg2.connect(uri, cursor_factory=psycopg2.extras.DictCursor)
    conn.set_session(autocommit=True)
    return conn

def make_cursor(connection):
    return connection.cursor()

def make_db(config):
    connection = connect_db(config['DATABASE_URI'])
    cursor = make_cursor(connection)
    cursor.execute('''
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
        CREATE TABLE IF NOT EXISTS users (
            id uuid DEFAULT uuid_generate_v4() PRIMARY KEY,
            email VARCHAR,
            dod_id VARCHAR,
            first_name VARCHAR,
            last_name VARCHAR
        );
        CREATE INDEX IF NOT EXISTS users_email ON users (email);
        CREATE INDEX IF NOT EXISTS dod_id ON users (dod_id);
    ''')
    connection.commit()
    connection.close()

