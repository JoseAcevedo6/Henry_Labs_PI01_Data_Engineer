from pandas import DataFrame, concat, read_csv, read_json

from config import Engine
from models import base_metadata


def cleansing(df, column):

    dicc = {'["#]': '', r"[-'\._()]": " ", '4k': '', 'uhd': '', '&': 'and'}
    dicc_listed_in = {
        '["#/+&,]': '', r"['\._()]": " ", 'documentaries|docuseries': 'documentary', 'stand.+up': 'stand-up',
        'shows|show|series|movies|film|tv|videos|features|young|audience|musicals|and': '', 'thrillers': 'thriller',
        'concerts': 'concert', 'classics': 'classic', 'action-adventure': 'action adventure', 'historical': 'history',
        'romantic': 'romance', 'dramas': 'drama', 'musical': 'music', 'comedies': 'comedy', 'mysteries': 'mystery',
        'military.+war': 'military-war', 'health.+wellness': 'health-wellness', 'science.+fiction': 'sci-fi',
        'black.+stories': 'black-stories', 'late.+night': 'late-night', 'faith.*spirituality': 'faith-spirituality',
        'coming.*of.*age': 'coming-of-age', 'special.+interest': 'special-interest', 'cooking.*food': 'cooking-food',
        'soap.*opera.*melodrama': 'soap-opera-melodrama',
        }

    dicc = dicc_listed_in if column == 'listed_in' else dicc

    df[column] = df[column].str.lower()
    df[column].replace(dicc, regex=True, inplace=True)
    df[column].replace({'  ': ' ', '   ': ' ', 'st-up': 'stand-up'}, regex=True, inplace=True)
    df[column] = df[column].str.strip()
    df[column] = df[column].str.title()

    return df[column]


def create_df_actor_listed_in(df, column, sep=' '):

    # Funcion para separar valores de filas de una dataframe[column] y rotornar un nuevo dataframe con dichos valores
    # en una sola columna. Recibe como primer parametro una columna de un dataframe y como segundo parametro el
    # elemento por el cual queremos separar (default white space).

    df_aux = df[column].str.split(sep, expand=True)

    # Convertimos el dataframe en un objeto numpy para unificar todo en una columna con el metodo flatten
    df_aux = df_aux.to_numpy().flatten()

    # Convertimos nuevamente a dataframe, eliminamos valores nulos, espacios en blanco si procede, valores repetidos
    # y ordenamos
    df_aux = DataFrame(df_aux)
    df_aux[0] = df_aux[0].str.strip()

    df_aux.replace({'': None, 'sin dato': None}, inplace=True)
    df_aux.dropna(inplace=True)
    df_aux.drop_duplicates(inplace=True)
    df_aux.drop(df_aux[df_aux[0].str.len() == 1].index, inplace=True)
    df_aux.sort_values(0, inplace=True)
    df_aux.reset_index(drop=True, inplace=True)
    df_aux.index += 1
    df_aux.reset_index(drop=False, inplace=True)

    column_name = 'actor' if column == 'cast' else column
    df_aux.columns = [f'id_{column_name}', column_name]

    return df_aux


def split_rows_df(df, column, split):

    df_aux = df[df[column] == split].copy()

    df_aux['duration'].replace({'sin dato': None}, regex=False, inplace=True)
    df_aux['duration'] = df_aux['duration'].astype('Int64')
    df_aux['duration'].fillna(int(df_aux['duration'].mean(skipna=True)), inplace=True)
    df_aux['duration'].replace({0: 1}, regex=False, inplace=True)

    df_aux = df_aux[['title_name', 'id_service', 'cast', 'release_year', 'duration', 'listed_in']]

    return df_aux


def create_df_aux(df, col1, col2, sep):

    df = df[[col1, col2]]
    df.set_index(col1, inplace=True)
    df = df[col2].str.split(sep, expand=True)

    df_aux = DataFrame()

    for i in range(len(df.columns)):
        df_aux = concat([df_aux, df[i]], axis=0)

    df_aux = df_aux[0].str.strip()
    df_aux.replace({'': None, 'sin dato': None}, inplace=True)
    df_aux.dropna(inplace=True)
    df_aux = df_aux.reset_index()
    df_aux.drop(df_aux[df_aux[0].str.len() == 1].index, inplace=True)
    df_aux.columns = [col1, 'actor' if col2 == 'cast' else col2]
    df_aux = df_aux.sort_values(col1)
    df_aux.drop_duplicates(inplace=True)

    return df_aux


def etl_data():

    df_amazon = read_csv("fast_api/datasets/amazon_prime_titles.csv")
    df_amazon['id_service'] = 1
    df_disney = read_csv("fast_api/datasets/disney_plus_titles.csv")
    df_disney['id_service'] = 2
    df_hulu = read_csv("fast_api/datasets/hulu_titles.csv")
    df_hulu['id_service'] = 3
    df_netflix = read_json("fast_api/datasets/netflix_titles.json")
    df_netflix['id_service'] = 4

    df_concated = concat([df_amazon, df_disney, df_hulu, df_netflix], axis=0, ignore_index=True)
    df_concated['duration'] = df_concated['duration'].str.split(expand=True)[0]
    df_concated.rename({'title': 'title_name'}, axis=1, inplace=True)
    df_concated.fillna('sin dato', inplace=True)

    df_concated['title_name'] = cleansing(df_concated, 'title_name')
    df_concated['cast'] = cleansing(df_concated, 'cast')
    df_concated['listed_in'] = cleansing(df_concated, 'listed_in')

    df_concated.sort_values('title_name', inplace=True)
    df_concated.reset_index(drop=True, inplace=True)

    df_actor = create_df_actor_listed_in(df_concated, 'cast', ',')

    df_listed_in = create_df_actor_listed_in(df_concated, 'listed_in')

    df_service = DataFrame({'id_service': [1, 2, 3, 4], 'service_name': ['Amazon', 'Disney', 'Hulu', 'Netflix']})

    df_title = df_concated[['title_name']]
    df_title = df_title.drop_duplicates()
    df_title.reset_index(drop=True, inplace=True)
    df_title.index += 1
    df_title = df_title.rename_axis('id_title').reset_index()

    df_movie = split_rows_df(df_concated, 'type', 'Movie')
    df_movie = df_movie.merge(df_title, how='left', on='title_name')

    df_serie = split_rows_df(df_concated, 'type', 'TV Show')
    df_serie = df_serie.merge(df_title, how='left', on='title_name')

    df_movie_title_service = df_movie[['id_title', 'id_service']].copy()
    df_movie_title_service.drop_duplicates(inplace=True)

    df_serie_title_service = df_serie[['id_title', 'id_service']].copy()
    df_serie_title_service.drop_duplicates(inplace=True)

    df_movie_title_actor = create_df_aux(df_movie, 'id_title', 'cast', ',')
    df_movie_title_actor = df_movie_title_actor.merge(df_actor, how='left', on='actor')
    df_movie_title_actor.drop(['actor'], axis=1, inplace=True)

    df_serie_title_actor = create_df_aux(df_serie, 'id_title', 'cast', ',')
    df_serie_title_actor = df_serie_title_actor.merge(df_actor, how='left', on='actor')
    df_serie_title_actor.drop(['actor'], axis=1, inplace=True)

    df_movie_title_listed_in = create_df_aux(df_movie, 'id_title', 'listed_in', ' ')
    df_movie_title_listed_in = df_movie_title_listed_in.merge(df_listed_in, how='left', on='listed_in')
    df_movie_title_listed_in.drop(['listed_in'], axis=1, inplace=True)

    df_serie_title_listed_in = create_df_aux(df_serie, 'id_title', 'listed_in', ' ')
    df_serie_title_listed_in = df_serie_title_listed_in.merge(df_listed_in, how='left', on='listed_in')
    df_serie_title_listed_in.drop(['listed_in'], axis=1, inplace=True)

    df_movie = df_movie[['id_title', 'release_year', 'duration']]
    df_movie.sort_values(by=['duration', 'id_title'], inplace=True)
    df_movie.drop_duplicates(subset=['id_title'], keep='last', inplace=True)

    df_serie = df_serie[['id_title', 'release_year', 'duration']]
    df_serie.sort_values(by=['duration', 'id_title'], ascending=False, inplace=True)
    df_serie.drop_duplicates(subset=['id_title'], keep='first', inplace=True)

    df_actor.to_sql('actor', Engine, if_exists='append', index=False)
    df_listed_in.to_sql('listed_in', Engine, if_exists='append', index=False)
    df_movie.to_sql('movie', Engine, if_exists='append', index=False)
    df_movie_title_actor.to_sql('movie_title_actor', Engine, if_exists='append', index=False)
    df_movie_title_listed_in.to_sql('movie_title_listed_in', Engine, if_exists='append', index=False)
    df_movie_title_service.to_sql('movie_title_service', Engine, if_exists='append', index=False)
    df_serie.to_sql('serie', Engine, if_exists='append', index=False)
    df_serie_title_actor.to_sql('serie_title_actor', Engine, if_exists='append', index=False)
    df_serie_title_listed_in.to_sql('serie_title_listed_in', Engine, if_exists='append', index=False)
    df_serie_title_service.to_sql('serie_title_service', Engine, if_exists='append', index=False)
    df_service.to_sql('service', Engine, if_exists='append', index=False)
    df_title.to_sql('title', Engine, if_exists='append', index=False)


base_metadata.create_all(bind=Engine)
etl_data()
