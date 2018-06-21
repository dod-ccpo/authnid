import psycopg2
import psycopg2.extras


def make_db(config):
    connection = psycopg2.connect(config['DATABASE_URI'])
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

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
        CREATE INDEX IF NOT EXISTS dod_id ON users (email);
    ''')
    connection.commit()

    return cursor
