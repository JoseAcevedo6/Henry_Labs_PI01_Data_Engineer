from sqlalchemy import create_engine, func, sql, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQL_DATABASE_URL = 'sqlite:///./src/streamServices.db'

Engine = create_engine(SQL_DATABASE_URL, connect_args={'check_same_thread': False}, pool_pre_ping=True, echo=True)

Session = sessionmaker(autocommit=False, autoflush=False, bind=Engine)

Func = func

Column = sql.column

Desc = desc

Base = declarative_base()
