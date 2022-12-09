-- SQLite

/*1 Máxima duración según tipo de film (película/serie), por plataforma y por año.
    El request debe ser: get_max_duration(año, plataforma, [min o season])*/

SELECT title, release_year, service, MAX(duration_time) duration, duration_unit FROM title 
JOIN title_service ON title_service.id_title = title.id_title
JOIN service ON service.id_service = title_service.id_service
WHERE release_year = 2020 AND service = 'Netflix' AND duration_unit = 'Min';


/*  Cantidad de películas y series (separado) por plataforma. 
    El request debe ser: get_count_plataform(plataforma)*/

SELECT duration_unit as type, COUNT(duration_unit) cantidad FROM title 
JOIN title_service ON title_service.id_title = title.id_title
JOIN service ON service.id_service = title_service.id_service
WHERE service = 'Netflix' AND duration_unit = 'Season'
UNION
SELECT duration_unit, COUNT(duration_unit) FROM title 
JOIN title_service ON title_service.id_title = title.id_title
JOIN service ON service.id_service = title_service.id_service
WHERE service = 'Netflix' AND duration_unit = 'Min';


/*3 Cantidad de veces que se repite un género y plataforma con mayor frecuencia del mismo.
    El request debe ser: get_listedin('genero')*/

SELECT total, service, total_per_service FROM
    (SELECT listed_in, COUNT(listed_in) total FROM title_service 
    JOIN title_listed_in ON title_listed_in.id_title = title_service.id_title
    JOIN listed_in ON listed_in.id_listed_in = title_listed_in.id_listed_in
    JOIN service ON service.id_service = title_service.id_service
    WHERE listed_in = 'Comedy') a
JOIN
    (SELECT listed_in, service, COUNT(listed_in) total_per_service FROM title_service 
    JOIN title_listed_in ON title_listed_in.id_title = title_service.id_title
    JOIN listed_in ON listed_in.id_listed_in = title_listed_in.id_listed_in
    JOIN service ON service.id_service = title_service.id_service
    WHERE listed_in = 'Comedy'
    GROUP BY service ORDER BY COUNT(listed_in) DESC LIMIT 1) b
ON a.listed_in = b.listed_in;


/*4 Actor que más se repite según plataforma y año.
    El request debe ser: get_actor(plataforma, año)*/

SELECT actor, COUNT(service) cantidad FROM title_actor 
JOIN title ON title.id_title = title_actor.id_title
JOIN title_service ON title_service.id_title = title.id_title
JOIN service ON service.id_service = title_service.id_service
JOIN actor ON actor.id_actor = title_actor.id_actor
WHERE service = 'Netflix' AND release_year = 2019
GROUP BY actor ORDER BY COUNT(service) DESC LIMIT 1;