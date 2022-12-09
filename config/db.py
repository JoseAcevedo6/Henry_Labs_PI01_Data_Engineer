from sqlalchemy import create_engine, MetaData



engine = create_engine('sqlite:///database.db', connect_args={'check_same_thread': False})

Meta = MetaData()

conn = engine.connect()