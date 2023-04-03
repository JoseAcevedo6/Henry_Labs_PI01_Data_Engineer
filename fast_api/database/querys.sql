-- 1. Máxima duración según tipo de film (película/serie), por plataforma y por año.
-- El request debe ser: get_max_duration (año, plataforma, [min o season])

SELECT title.title_name, movie.release_year, service.service_name, MAX(movie.duration) duration, 'Min' as 'duration_unit' 
FROM title
JOIN movie ON movie.id_title = title.id_title
JOIN movie_title_service ON movie_title_service.id_title = title.id_title
JOIN service ON service.id_service = movie_title_service.id_service
WHERE movie.release_year = 1992 AND service.service_name = 'Netflix' -- duration_unit = min

SELECT title.title_name, serie.release_year, service.service_name, MAX(serie.duration) duration, 'Season' as 'duration_unit'  
FROM title
JOIN serie ON serie.id_title = title.id_title
JOIN serie_title_service ON serie_title_service.id_title = title.id_title
JOIN service ON service.id_service = serie_title_service.id_service
WHERE serie.release_year = 1992 AND service.service_name = 'Netflix' -- duration_unit = season


-- 2. Cantidad de películas y series (separado) por plataforma. El request debe ser: get_count_plataform(plataforma)

SELECT COUNT(*) cantidad, service.service_name, 'Movie' as 'Type' FROM title JOIN movie_title_service ON movie_title_service.id_title = title.id_title
JOIN service ON service.id_service = movie_title_service.id_service WHERE service.service_name = 'Netflix'
    UNION
SELECT COUNT(*) cantidad, service.service_name, 'Serie' as 'Type' FROM title JOIN serie_title_service ON serie_title_service.id_title = title.id_title
JOIN service ON service.id_service = serie_title_service.id_service WHERE service.service_name = 'Netflix'


-- 3. Cantidad de veces que se repite un género y plataforma con mayor frecuencia del mismo.
-- El request debe ser: get_listedin('genero'). Como ejemplo de género pueden usar 'comedy',
-- que deberia devolverles un count de 2099 para la plataforma de Amazon.

SELECT listed_in, COUNT(*) cantidad, titles_listed_in.service_name FROM
    (SELECT movie_title_listed_in.id_title, listed_in.listed_in, service.service_name FROM movie_title_listed_in 
    JOIN movie_title_service ON movie_title_listed_in.id_title = movie_title_service.id_title 
    JOIN service ON service.id_service = movie_title_service.id_service
    JOIN listed_in ON listed_in.id_listed_in = movie_title_listed_in.id_listed_in
    WHERE listed_in.listed_in = 'Comedy'
        UNION ALL
    SELECT serie_title_listed_in.id_title, listed_in.listed_in, service.service_name FROM serie_title_listed_in 
    JOIN serie_title_service ON serie_title_listed_in.id_title = serie_title_service.id_title 
    JOIN service ON service.id_service = serie_title_service.id_service
    JOIN listed_in ON listed_in.id_listed_in = serie_title_listed_in.id_listed_in
    WHERE listed_in.listed_in = 'Comedy') titles_listed_in
GROUP BY titles_listed_in.service_name ORDER BY cantidad DESC LIMIT 1


-- 4. Actor que más se repite según plataforma y año. El request debe ser: get_actor(plataforma, año)

SELECT COUNT(*) cantidad, title_actor.actor FROM
    (SELECT actor.actor, movie.release_year, service.service_name FROM movie 
    JOIN movie_title_service ON movie_title_service.id_title = movie.id_title 
    JOIN service ON service.id_service = movie_title_service.id_service
    JOIN movie_title_actor ON movie_title_actor.id_title = movie.id_title
    JOIN actor ON actor.id_actor = movie_title_actor.id_actor
    WHERE service.service_name = 'Hulu' and movie.release_year = 2018
        UNION ALL
    SELECT actor.actor, serie.release_year, service.service_name FROM serie 
    JOIN serie_title_service ON serie_title_service.id_title = serie.id_title 
    JOIN service ON service.id_service = serie_title_service.id_service
    JOIN serie_title_actor ON serie_title_actor.id_title = serie.id_title
    JOIN actor ON actor.id_actor = serie_title_actor.id_actor
    WHERE service.service_name = 'Hulu' and serie.release_year = 2018) title_actor
GROUP BY title_actor.actor ORDER BY cantidad DESC LIMIT 3

