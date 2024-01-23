import pandas as pd
from sqlalchemy import create_engine
from streamlit import secrets


class Db:
    def __init__(self):
        self.engine = create_engine(secrets['db_con_string'])

    def get_club_topics(self):
        return pd.read_sql(f"select * from {secrets['club_topics_table']}", self.engine)

    def get_expressions(self):
        return pd.read_sql(f"select * from {secrets['club_expression_table']}", self.engine)

    def get_other_chunks(self):
        return pd.read_sql(f"select * from {secrets['other_chunks_table']}", self.engine)


