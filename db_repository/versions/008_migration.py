from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
<<<<<<< HEAD
chart = Table('chart', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('pnr', Integer),
    Column('name', String(length=64)),
    Column('seat', Integer),
    Column('password', String(length=4)),
)

=======
>>>>>>> c045df47a2aa7e5976d4d1588c1c3f23d7832987

def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
<<<<<<< HEAD
    post_meta.tables['chart'].columns['password'].create()
=======
>>>>>>> c045df47a2aa7e5976d4d1588c1c3f23d7832987


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
<<<<<<< HEAD
    post_meta.tables['chart'].columns['password'].drop()
=======
>>>>>>> c045df47a2aa7e5976d4d1588c1c3f23d7832987
