import pandas as pd
from sqlalchemy import create_engine


def cleansing(df, column):

    dicc = {'["#]': '', "[-'\._()]": " ", '4K': '', 'Uhd': '',
            '&': 'And', 'Seasons': 'Season'}
    dicc_listed_in = {'["#/+&,]': '', "['\._()]": " ", 'And|Movies|Film|Series|Tv|Videos|Features|Young|Audience|Musicals': '', 'Shows': 'Show', 'Thrillers': 'Thriller', 'Concerts': 'Concert', 'Dramas': 'Drama', 'Classics': 'Classic', 'Action-Adventure': 'Action Adventure', 'Romantic': 'Romance', 'Historical': 'History', 'Documentaries|Docuseries': 'Documentary', 'Musical': 'Music',
                      'Comedies': 'Comedy', 'Mysteries': 'Mystery', 'Military.+War': 'Military-War', 'Health.+Wellness': 'Health-Wellness', 'Science.+Fiction': 'Sci-Fi', 'Black.+Stories': 'Black-Stories', 'Late.+Night': 'Late-Night', 'Coming.*Of.*Age': 'Coming-Of-Age', 'Stand.+Up': 'Stand-Up', 'Special.+Interest': 'Special-Interest', 'Soap.*Opera.*Melodrama': 'Soap-Opera-Melodrama'}

    dicc = dicc_listed_in if column == 'listed_in' else dicc

    df[column] = df[column].str.title()
    df[column].replace(dicc, regex=True, inplace=True)
    df[column].replace({'  ': ' ', '   ': ' '}, regex=True, inplace=True)
    df[column] = df[column].str.strip()

    return df[column]


def create_df_actor_listed_in(df, column, sep=' '):

    # Funcion para separar valores de filas de una dataframe[column] y rotornar un nuevo dataframe con dichos valores en una sola columna.
    # # Recibe como primer parametro una columna de un dataframe y como segundo parametro el elemento por el cual queremos separar (default white space).

    column_name = 'actor' if column == 'cast' else column

    df_aux = df[column].str.split(sep, expand=True)

    # Convertimos el dataframe en un objeto numpy para unificar todo en una columna con el metodo flatten
    df_aux = df_aux.to_numpy().flatten()

    # Convertimos nuevamente a dataframe, eliminamos valores nulos, espacios en blanco si procede, valores repetidos y ordenamos
    df_aux = pd.DataFrame(df_aux)
    df_aux[0] = df_aux[0].str.strip()

    df_aux.replace({'': None}, inplace=True)

    df_aux.dropna(inplace=True)
    df_aux.drop_duplicates(inplace=True)
    df_aux.columns = [column_name]
    df_aux.drop(df_aux[df_aux[column_name].str.len() == 1].index, inplace=True)
    df_aux = df_aux.sort_values(column_name)
    df_aux.reset_index(drop=True, inplace=True)
    df_aux.index += 1
    df_aux.index.name = f"id_{column_name}"
    df_aux.reset_index(drop=False, inplace=True)

    return df_aux


def create_df_aux(df, col1, col2, sep):

    df = df[[col1, col2]]
    df.set_index(col1, inplace=True)
    df = df[col2].str.split(sep, expand=True)

    df_aux = pd.DataFrame()

    for i in range(len(df.columns)):
        df_aux = pd.concat([df_aux, df[i]], axis=0)

    df_aux = df_aux[0].str.strip()
    df_aux.replace({'': None}, inplace=True)
    df_aux = df_aux.reset_index()
    df_aux.columns = [col1, 'actor' if col2 == 'cast' else col2]
    df_aux = df_aux.sort_values('title')
    df_aux.dropna(inplace=True)

    return df_aux


df_amazon = pd.read_csv("datasets/amazon_prime_titles.csv")
df_amazon['service'] = 'Amazon'
df_disney = pd.read_csv("datasets/disney_plus_titles.csv")
df_disney['service'] = 'Disney'
df_hulu = pd.read_csv("datasets/hulu_titles.csv")
df_hulu['service'] = 'Hulu'
df_netflix = pd.read_json("datasets/netflix_titles.json")
df_netflix['service'] = 'Netflix'

df_title = pd.concat([df_amazon, df_disney, df_hulu,
                     df_netflix], axis=0, ignore_index=True)
df_title = pd.concat(
    [df_title, df_title['duration'].str.split(expand=True)], axis=1)
df_title.rename(columns={0: 'duration_time', 1: 'duration_unit'}, inplace=True)
df_title.drop(['show_id', 'type', 'director', 'country', 'date_added',
              'rating', 'duration', 'description'], axis=1, inplace=True)
df_title.fillna('Sin Dato', inplace=True)

df_title['title'] = cleansing(df_title, 'title')
df_title['cast'] = cleansing(df_title, 'cast')
df_title['listed_in'] = cleansing(df_title, 'listed_in')
df_title['duration_unit'] = cleansing(df_title, 'duration_unit')

df_actor = create_df_actor_listed_in(df_title, 'cast', ',')
df_actor.drop(df_actor[(df_actor['actor'] == 'Sin Dato')].index, inplace=True)
df_listed_in = create_df_actor_listed_in(df_title, 'listed_in')

df_service = pd.DataFrame(
    ['Amazon', 'Disney', 'Hulu', 'Netflix'], columns=['service'])
df_service.index.name = "id_service"
df_service.index += 1
df_service.reset_index(drop=False, inplace=True)

df_title_actor = create_df_aux(df_title, 'title', 'cast', ',')
df_title_actor.drop(
    df_title_actor[(df_title_actor['actor'] == 'Sin Dato')].index, inplace=True)
df_title_actor = df_title_actor.merge(df_actor, how='left', on='actor')

df_title_listed_in = create_df_aux(df_title, 'title', 'listed_in', ' ')
df_title_listed_in = df_title_listed_in.merge(
    df_listed_in, how='left', on='listed_in')

df_title_service = df_title[['title', 'service']]
df_title_service = df_title_service.sort_values('title')
df_title_service = df_title_service.merge(df_service, how='left', on='service')

df_title.drop(['cast', 'listed_in', 'service'], axis=1, inplace=True)
df_title = df_title.sort_values(by=['title', 'duration_time'])
df_title['duration_unit'].replace(
    {'Sin Dato': 'Min'}, regex=False, inplace=True)
df_title.drop_duplicates(['title', 'duration_unit'],
                         keep='first', inplace=True)
df_title.reset_index(drop=True, inplace=True)
df_title.index.name = "id_title"
df_title.index += 1
df_title.reset_index(drop=False, inplace=True)
df_title['duration_time'].replace(
    {'Sin Dato': None}, regex=False, inplace=True)
df_title['duration_time'] = df_title['duration_time'].astype('Int64')
df_title['duration_time'].fillna(
    int(df_title['duration_time'].median(skipna=True)), inplace=True)

df_title_actor = df_title_actor.merge(
    df_title[['id_title', 'title']], how='left', on='title')
df_title_actor['id_actor'] = df_title_actor['id_actor'].astype('Int64')
df_title_actor.drop(['title', 'actor'], axis=1, inplace=True)

df_title_listed_in = df_title_listed_in.merge(
    df_title[['id_title', 'title']], how='left', on='title')
df_title_listed_in.drop(['title', 'listed_in'], axis=1, inplace=True)

df_title_service = df_title_service.merge(
    df_title[['id_title', 'title']], how='left', on='title')
df_title_service.drop(['title', 'service'], axis=1, inplace=True)


file_db = create_engine('sqlite:///./database/titles.db')

df_title.to_sql('title', file_db, if_exists='replace', index=False)
df_actor.to_sql('actor', file_db, if_exists='replace', index=False)
df_listed_in.to_sql('listed_in', file_db, if_exists='replace', index=False)
df_service.to_sql('service', file_db, if_exists='replace', index=False)
df_title_actor.to_sql('title_actor', file_db, if_exists='replace', index=False)
df_title_listed_in.to_sql('title_listed_in', file_db,
                          if_exists='replace', index=False)
df_title_service.to_sql('title_service', file_db,
                        if_exists='replace', index=False)
