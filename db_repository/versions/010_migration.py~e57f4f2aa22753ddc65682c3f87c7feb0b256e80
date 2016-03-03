from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
discuss = Table('discuss', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('message', String(length=200)),
    Column('user_id', Integer),
    Column('discussion_id', Integer),
)

discussion = Table('discussion', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('topic', String(length=50)),
    Column('message', String(length=200)),
    Column('user_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['discuss'].create()
    post_meta.tables['discussion'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['discuss'].drop()
    post_meta.tables['discussion'].drop()
