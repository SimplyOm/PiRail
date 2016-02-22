from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
post = Table('post', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('body', VARCHAR(length=140)),
    Column('timestamp', DATETIME),
    Column('user_id', INTEGER),
)

user = Table('user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('nickname', VARCHAR(length=64)),
    Column('email', VARCHAR(length=120)),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('pnr', Integer),
    Column('name', String(length=64)),
    Column('food', String(length=20)),
    Column('sanitation', String(length=20)),
    Column('journey', String(length=20)),
    Column('feedback', String(length=200)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['post'].drop()
    pre_meta.tables['user'].columns['email'].drop()
    pre_meta.tables['user'].columns['nickname'].drop()
    post_meta.tables['user'].columns['feedback'].create()
    post_meta.tables['user'].columns['food'].create()
    post_meta.tables['user'].columns['journey'].create()
    post_meta.tables['user'].columns['name'].create()
    post_meta.tables['user'].columns['pnr'].create()
    post_meta.tables['user'].columns['sanitation'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['post'].create()
    pre_meta.tables['user'].columns['email'].create()
    pre_meta.tables['user'].columns['nickname'].create()
    post_meta.tables['user'].columns['feedback'].drop()
    post_meta.tables['user'].columns['food'].drop()
    post_meta.tables['user'].columns['journey'].drop()
    post_meta.tables['user'].columns['name'].drop()
    post_meta.tables['user'].columns['pnr'].drop()
    post_meta.tables['user'].columns['sanitation'].drop()
