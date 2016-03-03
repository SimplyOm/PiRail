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
    Column('mobile', String(length=10)),
    Column('train', String(length=5)),
    Column('start', Integer),
    Column('end', Integer),
=======
discussion = Table('discussion', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('topic', String(length=50)),
    Column('message', String(length=200)),
    Column('user_id', Integer),
    Column('timestamp', DateTime),
)

discuss = Table('discuss', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('message', String(length=200)),
    Column('user_id', Integer),
    Column('discussion_id', Integer),
    Column('timestamp', DateTime),
>>>>>>> e57f4f2aa22753ddc65682c3f87c7feb0b256e80
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
<<<<<<< HEAD
    post_meta.tables['chart'].columns['end'].create()
    post_meta.tables['chart'].columns['start'].create()
    post_meta.tables['chart'].columns['train'].create()
=======
    post_meta.tables['discussion'].columns['timestamp'].create()
    post_meta.tables['discuss'].columns['timestamp'].create()
>>>>>>> e57f4f2aa22753ddc65682c3f87c7feb0b256e80


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
<<<<<<< HEAD
    post_meta.tables['chart'].columns['end'].drop()
    post_meta.tables['chart'].columns['start'].drop()
    post_meta.tables['chart'].columns['train'].drop()
=======
    post_meta.tables['discussion'].columns['timestamp'].drop()
    post_meta.tables['discuss'].columns['timestamp'].drop()
>>>>>>> e57f4f2aa22753ddc65682c3f87c7feb0b256e80
