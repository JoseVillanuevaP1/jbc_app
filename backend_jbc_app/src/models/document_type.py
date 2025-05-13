from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, Boolean
from src.config.db import meta, engine


document_types = Table(
    'document_types', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(30)),
    Column('created_at',DateTime),
    Column('updated_at',DateTime,nullable=True),
    Column('status',Boolean,default=True),
)

meta.create_all(engine)