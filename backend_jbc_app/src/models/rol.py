from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String, Boolean, DateTime
from src.config.db import meta, engine

roles = Table('roles', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(255)),
    Column('status', Boolean, default=True),
    Column('created_date', DateTime),
    Column('updated_date', DateTime, nullable=True),
)

meta.create_all(engine)