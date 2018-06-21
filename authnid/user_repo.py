class UserRepo():
    def __init__(self, db):
        self.db = db

    def add_user(self, email=None, dod_id=None, first_name=None, last_name=None):
        self.db.execute("""
        INSERT INTO users (email,dod_id,first_name,last_name)
            VALUES (%s,%s,%s,%s)
            RETURNING id;
        """, (email, dod_id, first_name, last_name))
        self.db.connection.commit()
        uuid = self.db.fetchone()[0]
        return uuid

    def get_user(self, uuid):
        self.db.execute("SELECT * FROM users WHERE id=%s", (uuid,))
        return self.db.fetchone()

