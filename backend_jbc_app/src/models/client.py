from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, Boolean
from src.config.db import meta, engine
from src.models.document_type import document_types

clients = Table(
    'clients', meta,
    Column('id', Integer, primary_key=True),
    Column('document_type_id', Integer, ForeignKey('document_types.id')),
    Column('first_name', String(255)),
    Column('last_name', String(255)),
    Column('document_number', String(20)),
    Column('phone', String(15)),
    Column('email', String(255)),
    Column('address', String(255)),
    Column('created_at',DateTime),
    Column('updated_at',DateTime,nullable=True),
    Column('status',Boolean,default=True),
)

meta.create_all(engine)