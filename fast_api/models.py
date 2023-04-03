from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base, Engine


class Actor(Base):
    __tablename__ = 'actor'
    id_actor = Column(Integer, primary_key=True, index=True)
    actor = Column(String)
    movie_title_actor = relationship('Movie_title_actor', backref='actor')
    serie_title_actor = relationship('Serie_title_actor', backref='actor')


class Listed_in(Base):
    __tablename__ = 'listed_in'
    id_listed_in = Column(Integer, primary_key=True, index=True)
    listed_in = Column(String)
    movie_title_listed_in = relationship('Movie_title_listed_in', backref='listed_in')
    serie_title_listed_in = relationship('Serie_title_listed_in', backref='listed_in')


class Movie(Base):
    __tablename__ = 'movie'
    id_movie = Column(Integer, primary_key=True, index=True)
    id_title = Column(Integer, ForeignKey('title.id_title'), index=True)
    release_year = Column(Integer)
    duration = Column(Integer)


class Movie_title_actor(Base):
    __tablename__ = 'movie_title_actor'
    id_title = Column(Integer, ForeignKey('title.id_title'), index=True)
    id_actor = Column(Integer, ForeignKey('actor.id_actor'), index=True)
    __mapper_args__ = {'primary_key': [id_title, id_actor]}


class Movie_title_listed_in(Base):
    __tablename__ = 'movie_title_listed_in'
    id_title = Column(Integer, ForeignKey('title.id_title'), index=True)
    id_listed_in = Column(Integer, ForeignKey('listed_in.id_listed_in'), index=True)
    __mapper_args__ = {'primary_key': [id_title, id_listed_in]}


class Movie_title_service(Base):
    __tablename__ = 'movie_title_service'
    id_title = Column(Integer, ForeignKey('title.id_title'), index=True)
    id_service = Column(Integer, ForeignKey('service.id_service'), index=True)
    __mapper_args__ = {'primary_key': [id_title, id_service]}


class Serie(Base):
    __tablename__ = 'serie'
    id_serie = Column(Integer, primary_key=True, index=True)
    id_title = Column(Integer, ForeignKey('title.id_title'), index=True)
    release_year = Column(Integer)
    duration = Column(Integer)


class Serie_title_actor(Base):
    __tablename__ = 'serie_title_actor'
    id_title = Column(Integer, ForeignKey('title.id_title'), index=True)
    id_actor = Column(Integer, ForeignKey('actor.id_actor'), index=True)
    __mapper_args__ = {'primary_key': [id_title, id_actor]}


class Serie_title_listed_in(Base):
    __tablename__ = 'serie_title_listed_in'
    id_title = Column(Integer, ForeignKey('title.id_title'), index=True)
    id_listed_in = Column(Integer, ForeignKey('listed_in.id_listed_in'), index=True)
    __mapper_args__ = {'primary_key': [id_title, id_listed_in]}


class Serie_title_service(Base):
    __tablename__ = 'serie_title_service'
    id_title = Column(Integer, ForeignKey('title.id_title'), index=True)
    id_service = Column(Integer, ForeignKey('service.id_service'), index=True)
    __mapper_args__ = {'primary_key': [id_title, id_service]}


class Service(Base):
    __tablename__ = 'service'
    id_service = Column(Integer, primary_key=True, index=True)
    service_name = Column(String)
    movie_title_service = relationship('Movie_title_service', backref='service')
    serie_title_service = relationship('Serie_title_service', backref='service')


class Title(Base):
    __tablename__ = 'title'
    id_title = Column(Integer, primary_key=True, index=True)
    title_name = Column(String)
    movie = relationship('Movie', backref='title')
    movie_title_actor = relationship('Movie_title_actor', backref='title')
    movie_title_listed_in = relationship('Movie_title_listed_in', backref='title')
    movie_title_service = relationship('Movie_title_service', backref='title')
    serie = relationship('Serie', backref='title')
    serie_title_actor = relationship('Serie_title_actor', backref='title')
    serie_title_listed_in = relationship('Serie_title_listed_in', backref='title')
    serie_title_service = relationship('Serie_title_service', backref='title')


Base.metadata.create_all(bind=Engine)
