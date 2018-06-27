from psycopg2.extensions import AsIs

class UserRepo():
    def __init__(self, cursor):
        self.cursor = cursor

    IS_MATCH = '(%s) = %s'

    def _build_match(self, **kwargs):
        return self.cursor.mogrify(
                    self.IS_MATCH,
                    (AsIs(','.join(kwargs.keys())), tuple(kwargs.values()))
                ).decode()

    def has_user(self, **kwargs):
        match = self._build_match(**kwargs)
        self.cursor.execute("""
        SELECT CASE WHEN EXISTS (
            SELECT * FROM users WHERE {}
        )
        THEN true
        ELSE false END
        """.format(match))
        return self.cursor.fetchone()[0]

    def add_user(self, email=None, dod_id=None, first_name=None, last_name=None):
        self.cursor.execute("""
        INSERT INTO users (email,dod_id,first_name,last_name)
            VALUES (%s,%s,%s,%s)
            RETURNING id;
        """, (email, dod_id, first_name, last_name))
        uuid = self.cursor.fetchone()[0]
        return uuid

    def get_user(self, **kwargs):
        match = self._build_match(**kwargs)
        self.cursor.execute("SELECT * FROM users WHERE {}".format(match))
        return self.cursor.fetchone()

    def count(self):
        self.cursor.execute("SELECT count(*) FROM users")
        return self.cursor.fetchone()[0]

    def all(self):
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()

    def ensure_user_exists(self, **kwargs):
        if self.has_user(**kwargs):
            user = self.get_user(**kwargs)
            return user.get('id')
        else:
            return self.add_user(**kwargs)
