from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, Text, Boolean
from src.config.db import meta,engine

users = Table('users', meta, 
    Column('id',Integer,primary_key=True),
    Column('name',String(255)),
    Column('email',String(255)),
    Column('password',String(255)),
    Column('photo',String(255),nullable=True),
    Column('failed_attempts', Integer, default=0),
    Column('lock_time',DateTime, nullable=True),
    Column('created_at',DateTime),
    Column('updated_at',DateTime,nullable=True),
    Column('status',Boolean,default=True),
    )

meta.create_all(engine)