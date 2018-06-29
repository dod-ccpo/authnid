"""add unique index constraints

Revision ID: 44a0c7b54ef6
Revises: 85d52c4ca2ec
Create Date: 2018-06-29 09:39:16.757348

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '44a0c7b54ef6'
down_revision = '85d52c4ca2ec'
branch_labels = None
depends_on = None


def upgrade():
    db = op.get_bind()
    db.execute("""DROP INDEX ix_users_email;""")
    db.execute("""DROP INDEX ix_users_dod_id;""")
    db.execute("""
        CREATE UNIQUE INDEX ix_users_email ON users (email);
    """)
    db.execute("""
        CREATE UNIQUE INDEX ix_users_dod_id ON users (dod_id);
    """)


def downgrade():
    db = op.get_bind()
    db.execute("""DROP INDEX ix_users_email;""")
    db.execute("""DROP INDEX ix_users_dod_id;""")
    db.execute("""
        CREATE INDEX ix_users_email ON users (email);
    """)
    db.execute("""
        CREATE INDEX ix_users_dod_id ON users (dod_id);
    """)
