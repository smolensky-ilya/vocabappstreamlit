import pandas as pd
from sqlalchemy import create_engine
from streamlit import secrets


class Db:
    def __init__(self):
        self.engine = create_engine(secrets['db_con_string'])

    def get_club_topics(self, limit):
        return pd.read_sql(f"SELECT * FROM {secrets['club_topics_table']} ORDER BY rand() LIMIT {limit}",
                           self.engine)

    def get_expressions(self, topics: list, limit):
        joining = ", ".join([f"'{x}'" for x in pd.unique(topics)])
        return pd.read_sql(f"SELECT * FROM (SELECT *, ROW_NUMBER() OVER (PARTITION BY topic ORDER BY RAND()) as "
                           f"rn FROM {secrets['club_expression_table']} WHERE topic IN ({joining})) AS subquery "
                           f"WHERE rn <= {limit}", self.engine).iloc[:, :-1]

    def get_other_chunks(self, limit):
        return pd.read_sql(f"SELECT * FROM {secrets['other_chunks_table']} ORDER BY rand() LIMIT {limit}", self.engine)

    def get_random_exp_from_both(self, limit):
        return pd.read_sql(f"SELECT * FROM "
                           f"(SELECT expressions FROM {secrets['club_expression_table']} "
                           f"UNION "
                           f"SELECT expression FROM {secrets['other_chunks_table']}) as exp "
                           f"ORDER BY rand() LIMIT {limit}", self.engine)
