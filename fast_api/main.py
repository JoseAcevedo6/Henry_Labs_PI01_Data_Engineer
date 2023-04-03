from fastapi import FastAPI, status, responses, encoders
import uvicorn

from database import Func, Column, Session, Desc
from models import Actor, Listed_in, Movie, Serie, Service, Title, Movie_title_actor, Movie_title_listed_in,\
    Movie_title_service, Serie_title_actor, Serie_title_listed_in, Serie_title_service


app = FastAPI()


@app.get("/get_max_duration")
def get_max_duration(year: int, platform: str, type: str):

    db = Session()

    if type.lower() == 'min':
        query = db.query(
            Title.title_name, Movie.release_year, Func.max(Movie.duration), Movie.duration,
            Column("Min").label('duration_unit'), Service.service_name)\
            .select_from(Title).join(Movie).join(Movie_title_service).join(Service)\
            .where(Movie.release_year == year).where(Service.service_name == platform.capitalize()).all()
    if type.lower() == 'season':
        query = db.query(
            Title.title_name, Serie.release_year, Func.max(Serie.duration), Movie.duration,
            Column("Season").label('duration_unit'), Service.service_name)\
            .select_from(Title).join(Serie).join(Serie_title_service).join(Service)\
            .where(Serie.release_year == year).where(Service.service_name == platform.capitalize()).all()

    result_dicts = [r._asdict() for r in query]

    db.close()

    return responses.JSONResponse(status_code=status.HTTP_200_OK, content=encoders.jsonable_encoder(result_dicts))


@app.get("/get_count_platform")
def get_count_platform(platform: str):

    db = Session()

    movie_query = db.query(
        Column("Movie").label('type'), Func.count(Title.title_name).label('cantidad'), Service.service_name)\
        .select_from(Title).join(Movie_title_service)\
        .join(Service).where(Service.service_name == platform.capitalize())

    serie_query = db.query(
        Column("Serie").label('type'), Func.count(Title.title_name).label('cantidad'), Service.service_name)\
        .select_from(Title).join(Serie_title_service).\
        join(Service).where(Service.service_name == platform.capitalize())

    query = movie_query.union(serie_query).all()
    result_dicts = [r._asdict() for r in query]

    db.close()

    return responses.JSONResponse(status_code=status.HTTP_200_OK, content=encoders.jsonable_encoder(result_dicts))


@app.get("/get_listedin")
def get_listedin(listed_in: str):

    db = Session()

    query1 = db.query(Movie_title_listed_in.id_title, Listed_in.listed_in, Service.service_name)\
        .select_from(Movie_title_listed_in)\
        .join(Movie_title_service, Movie_title_service.id_title == Movie_title_listed_in.id_title)\
        .join(Service, Service.id_service == Movie_title_service.id_service)\
        .join(Listed_in, Listed_in.id_listed_in == Movie_title_listed_in.id_listed_in)\
        .where(Listed_in.listed_in == listed_in.capitalize())

    query2 = db.query(Serie_title_listed_in.id_title, Listed_in.listed_in, Service.service_name)\
        .select_from(Serie_title_listed_in)\
        .join(Serie_title_service, Serie_title_service.id_title == Serie_title_listed_in.id_title)\
        .join(Service, Service.id_service == Serie_title_service.id_service)\
        .join(Listed_in, Listed_in.id_listed_in == Serie_title_listed_in.id_listed_in)\
        .where(Listed_in.listed_in == listed_in.capitalize())

    gen_query = query1.union_all(query2)
    count_listed_in = gen_query.with_entities(Listed_in.listed_in, Func.count().label('count'), Service.service_name)\
        .group_by(Service.service_name).order_by(Desc(Func.count()))
    count_listed_in = count_listed_in.first()._asdict() if count_listed_in else None

    db.close()

    return responses.JSONResponse(status_code=status.HTTP_200_OK, content=encoders.jsonable_encoder(count_listed_in))


@app.get("/get_actor")
def get_actor(platform: str, release_year: int):

    db = Session()

    query1 = db.query(Actor.actor, Movie.release_year, Service.service_name)\
        .select_from(Movie)\
        .join(Movie_title_service, Movie_title_service.id_title == Movie.id_title)\
        .join(Service, Service.id_service == Movie_title_service.id_service)\
        .join(Movie_title_actor, Movie_title_actor.id_title == Movie.id_title)\
        .join(Actor, Actor.id_actor == Movie_title_actor.id_actor)\
        .where(Service.service_name == platform.capitalize()).where(Movie.release_year == release_year)

    query2 = db.query(Actor.actor, Serie.release_year, Service.service_name)\
        .select_from(Serie)\
        .join(Serie_title_service, Serie_title_service.id_title == Serie.id_title)\
        .join(Service, Service.id_service == Serie_title_service.id_service)\
        .join(Serie_title_actor, Serie_title_actor.id_title == Serie.id_title)\
        .join(Actor, Actor.id_actor == Serie_title_actor.id_actor)\
        .where(Service.service_name == platform.capitalize()).where(Serie.release_year == release_year)

    actor_count = query1.union_all(query2)
    actor_count = actor_count.with_entities(
        Actor.actor, Func.count(Actor.actor).label('count'), Serie.release_year, Service.service_name)\
        .group_by(Actor.actor).order_by(Desc(Func.count(Actor.actor)))

    if 'Sin Dato' in actor_count.first():
        actor_count = actor_count.offset(1).first()._asdict()
    else:
        actor_count = actor_count.first()._asdict()

    db.close()

    return responses.JSONResponse(status_code=status.HTTP_200_OK, content=encoders.jsonable_encoder(actor_count))


if __name__ == '__main__':
    uvicorn.run('endpoints:app', host='127.0.0.1', port=8080, reload=True)
