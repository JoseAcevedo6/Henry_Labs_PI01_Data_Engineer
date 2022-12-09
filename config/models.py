from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from db import Meta, engine

actor = Table('actor', Meta, Column('id_actor', Integer,
              primary_key=True), Column('actor', String(255)))

listed_in = Table('listed_in', Meta, Column('id_listed_in', Integer,
                                            primary_key=True), Column('listed_in', String(255)))

service = Table('service', Meta, Column('id_service', Integer,
                                        primary_key=True), Column('service', String(255)))

title = Table('title', Meta, Column('id_title', Integer,
              primary_key=True), Column('title', String(255)), Column(
    'release_year', Integer), Column('duration_time', Integer), Column('duration_unit', String(10)))

title_actor = Table('title_actor', Meta, Column(
    'id_actor', Integer), Column('id_title', Integer))

title_listed_in = Table('title_listed_in', Meta, Column(
    'id_listed_in', Integer), Column('id_title', Integer))

title_service = Table('title_service', Meta, Column(
    'id_service', Integer), Column('id_title', Integer))

Meta.create_all(engine)