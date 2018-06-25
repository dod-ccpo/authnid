import psycopg2
import psycopg2.extras

def connect_db(uri):
    return psycopg2.connect(uri)

def make_cursor(connection):
    return connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

def make_db(config):
    connection = connect_db(config['DATABASE_URI'])
    cursor = make_cursor(connection)
    cursor.execute('''
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
        CREATE TABLE IF NOT EXISTS users (
            id uuid DEFAULT uuid_generate_v4() PRIMARY KEY,
            email VARCHAR(254) NOT NULL,
            dod_id VARCHAR(16),
            first_name VARCHAR(128),
            last_name VARCHAR(128)
        );
        CREATE INDEX IF NOT EXISTS users_email ON users (email);
        CREATE INDEX IF NOT EXISTS dod_id ON users (dod_id);
    ''')
    connection.commit()
    connection.close()

