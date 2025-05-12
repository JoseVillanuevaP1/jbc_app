from sqlalchemy import Table, Column, Integer, ForeignKey
from src.config.db import meta, engine

user_roles = Table('user_roles', meta,
    Column('id_user', Integer, ForeignKey('users.id')),
    Column('id_rol', Integer, ForeignKey('roles.id'))
)

meta.create_all(engine)