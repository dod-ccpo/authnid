from psycopg2.extensions import AsIs

class UserRepo():
    def __init__(self, db, autocommit=True):
        self.db = db
        self.autocommit = autocommit

    IS_MATCH = '(%s) = %s'

    def has_user(self, **kwargs):
        match = self.db.mogrify(
                    self.IS_MATCH,
                    (AsIs(','.join(kwargs.keys())), tuple(kwargs.values()))
                ).decode()
        self.db.execute("""
        SELECT CASE WHEN EXISTS (
            SELECT * FROM users WHERE {}
        )
        THEN true
        ELSE false END
        """.format(match))
        return self.db.fetchone()[0]

    def add_user(self, email=None, dod_id=None, first_name=None, last_name=None):
        self.db.execute("""
        INSERT INTO users (email,dod_id,first_name,last_name)
            VALUES (%s,%s,%s,%s)
            RETURNING id;
        """, (email, dod_id, first_name, last_name))
        if self.autocommit:
            self.db.connection.commit()
        uuid = self.db.fetchone()[0]
        return uuid

    def get_user(self, uuid):
        self.db.execute("SELECT * FROM users WHERE id=%s", (uuid,))
        return self.db.fetchone()

    def count(self):
        self.db.execute("SELECT count(*) FROM users")
        return self.db.fetchone()[0]

    def all(self):
        self.db.execute("SELECT * FROM users")
        return self.db.fetchall()
