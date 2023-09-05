from fastapi import APIRouter, status, responses, encoders, Query
from fastapi.responses import RedirectResponse

from database.config import Func, Column, Session, Desc
from database.models import Actor, Listed_in, Movie, Serie, Service, Title, Movie_title_actor, Movie_title_listed_in, \
    Movie_title_service, Serie_title_actor, Serie_title_listed_in, Serie_title_service
from schemas import Get_max_duration, Get_count_platform, Get_most_frequent_listedin, Get_actor, Get_listed_in

router = APIRouter()


@router.get('/', include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url='/docs')


@router.get("/get_max_duration",
            response_model=Get_max_duration,
            tags=['Querys'],
            name='Get the max duration of a movie(min) or a season filtered by release year and service')
def get_max_duration(
        platform: str = Query(description='[Amazon, Disney, Hulu, Netflix]'),
        year: int = Query(description='From 1925 to 2021'),
        type: str = Query(description="[Min, Season]")):

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


@router.get("/get_count_platform",
            response_model=Get_count_platform,
            tags=['Querys'],
            name='Get the amount of movies and series filtered by streaming service')
def get_count_platform(platform: str = Query(description='[Amazon, Disney, Hulu, Netflix]')):

    db = Session()

    movie_query = db.query(
        Column("Movie").label('type'), Func.count(Title.title_name).label('amount'), Service.service_name)\
        .select_from(Title).join(Movie_title_service)\
        .join(Service).where(Service.service_name == platform.capitalize())

    serie_query = db.query(
        Column("Serie").label('type'), Func.count(Title.title_name).label('amount'), Service.service_name)\
        .select_from(Title).join(Serie_title_service).\
        join(Service).where(Service.service_name == platform.capitalize())

    query = movie_query.union(serie_query).all()
    result_dicts = [r._asdict() for r in query]

    db.close()

    return responses.JSONResponse(status_code=status.HTTP_200_OK, content=encoders.jsonable_encoder(result_dicts))


@router.get("/get_most_frequent_listedin",
            response_model=Get_most_frequent_listedin,
            tags=['Querys'],
            name="Get the streaming service with the most genre's frequency")
def get_most_frequent_listedin(
        listed_in: str = Query(description='Go to the Query /get_listed_in to see all available genres')):

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
    count_listed_in = gen_query.with_entities(Listed_in.listed_in, Func.count().label('amount'), Service.service_name)\
        .group_by(Service.service_name).order_by(Desc(Func.count()))
    count_listed_in = count_listed_in.first()._asdict() if count_listed_in else None

    db.close()

    return responses.JSONResponse(status_code=status.HTTP_200_OK, content=encoders.jsonable_encoder(count_listed_in))


@router.get("/get_actor",
            response_model=Get_actor,
            tags=['Querys'],
            name='Get the most frequent actor filtered by year and streaming service')
def get_actor(platform: str = Query(description='[Amazon, Disney, Hulu, Netflix]'),
              release_year: int = Query(description='From 1925 to 2021')):

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
        Actor.actor, Func.count(Actor.actor).label('amount'), Serie.release_year, Service.service_name)\
        .group_by(Actor.actor).order_by(Desc(Func.count(Actor.actor)))

    if 'Sin Dato' in actor_count.first():
        actor_count = actor_count.offset(1).first()._asdict()
    else:
        actor_count = actor_count.first()._asdict()

    db.close()

    return responses.JSONResponse(status_code=status.HTTP_200_OK, content=encoders.jsonable_encoder(actor_count))


@router.get("/get_listed_in",
            response_model=Get_listed_in,
            tags=['Querys'],
            name="Get the genre's list")
def get_listed_in():

    db = Session()

    query = db.query(Listed_in.listed_in).select_from(Listed_in).all()
    result_dicts = {'listed_in': [r[0] for r in query]}
    result_dicts = result_dicts
    print(result_dicts, '<----- este es resultdicts')

    db.close()

    return responses.JSONResponse(status_code=status.HTTP_200_OK, content=encoders.jsonable_encoder(result_dicts))
