"""create users table

Revision ID: 85d52c4ca2ec
Revises:
Create Date: 2018-06-27 16:19:46.848258

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85d52c4ca2ec'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    db = op.get_bind()
    db.execute("""CREATE EXTENSION "uuid-ossp";""")
    db.execute("""
        CREATE TABLE users (
            id uuid DEFAULT uuid_generate_v4() PRIMARY KEY,
            email VARCHAR,
            dod_id VARCHAR,
            first_name VARCHAR,
            last_name VARCHAR
        );
    """)
    db.execute("""
        CREATE INDEX ix_users_email ON users (email);
    """)
    db.execute("""
        CREATE INDEX ix_users_dod_id ON users (dod_id);
    """)


def downgrade():
    db = op.get_bind()
    db.execute("""DROP INDEX ix_users_email;""")
    db.execute("""DROP INDEX ix_users_dod_id;""")
    db.execute("""DROP TABLE users;""")
    db.execute("""DROP EXTENSION "uuid-ossp";""")
