import sqlite3 as sql

def connect_execute(query):

    conn = sql.connect('database/titles.db')
    cursor = conn.cursor()
    cursor.execute(query)
    respuesta = cursor.fetchall()
    
    return respuesta

def query1(release_year, service, type):

    query =    f"SELECT title, release_year, service, MAX(duration_time) duration, duration_unit FROM title\
                JOIN title_service ON title_service.id_title = title.id_title\
                JOIN service ON service.id_service = title_service.id_service\
                WHERE release_year = {release_year} AND service = '{service}' AND duration_unit = '{type}'"
    return query

def query2(service):

    query =    f"SELECT duration_unit as type, COUNT(duration_unit) cantidad FROM title JOIN title_service ON title_service.id_title = title.id_title\
                JOIN service ON service.id_service = title_service.id_service WHERE service = '{service}' AND duration_unit = 'Season'\
                UNION\
                SELECT duration_unit, COUNT(duration_unit) FROM title JOIN title_service ON title_service.id_title = title.id_title\
                JOIN service ON service.id_service = title_service.id_service WHERE service = '{service}' AND duration_unit = 'Min'"

    return query

def query3(listed_in):

    query =    f"SELECT total, service, total_per_service FROM\
                    (SELECT listed_in, COUNT(listed_in) total FROM title_service\
                    JOIN title_listed_in ON title_listed_in.id_title = title_service.id_title\
                    JOIN listed_in ON listed_in.id_listed_in = title_listed_in.id_listed_in\
                    JOIN service ON service.id_service = title_service.id_service\
                    WHERE listed_in = '{listed_in}') a\
                JOIN\
                    (SELECT listed_in, service, COUNT(listed_in) total_per_service FROM title_service\
                    JOIN title_listed_in ON title_listed_in.id_title = title_service.id_title\
                    JOIN listed_in ON listed_in.id_listed_in = title_listed_in.id_listed_in\
                    JOIN service ON service.id_service = title_service.id_service\
                    WHERE listed_in = '{listed_in}'\
                    GROUP BY service ORDER BY COUNT(listed_in) DESC LIMIT 1) b\
                ON a.listed_in = b.listed_in"

    return query

def query4(service, release_year):

    query = f"SELECT actor, COUNT(service) cantidad FROM title_actor\
            JOIN title ON title.id_title = title_actor.id_title\
            JOIN title_service ON title_service.id_title = title.id_title\
            JOIN service ON service.id_service = title_service.id_service\
            JOIN actor ON actor.id_actor = title_actor.id_actor\
            WHERE service = '{service}' AND release_year = {release_year}\
            GROUP BY actor ORDER BY COUNT(service) DESC LIMIT 1"

    return query
