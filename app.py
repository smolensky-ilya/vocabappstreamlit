import pandas as pd
import random
import streamlit as st
from db_connection import Db


st.set_page_config(page_title='Speaking Club Material')
database = Db()


def get_club_data():
    data = database.get_club_topics()
    expressions = database.get_expressions()
    return data, expressions


def pick_random(df):
    qs = pd.unique(df['questions'])
    random_q = qs[random.randint(0, len(qs) - 1)]
    filtered = df.query('questions == @random_q').reset_index(drop=True)
    topic = filtered['topic'][0]
    responses = filtered['answers']
    rand_r = responses[random.randint(0, len(responses) - 1)]
    return random_q, rand_r, topic


def main():

    refresh = st.button('Refresh', use_container_width=True)
    if refresh:
        st.rerun()
    data, expressions = get_club_data()
    for x in range(5):
        rq, rr, rand_top = pick_random(data)
        st.write(f"----")
        st.markdown(f"<i>{rand_top.replace('_', ' ')}</i>", unsafe_allow_html=True)
        st.subheader(f"{rq}")
        st.write(f"")
        st.write(f"{rr}")
        st.write(f"")
        exp_list = random.sample(expressions.query('topic == @rand_top')['expressions'].to_list(), 20)
        col1, col2, col3, col4 = st.columns(4)
        for i, each in enumerate(exp_list):
            if i % 4 == 0:
                col1.markdown(f"<i>{each}</i>", unsafe_allow_html=True)
            elif i % 4 == 1:
                col2.markdown(f"<i>{each}</i>", unsafe_allow_html=True)
            elif i % 4 == 2:
                col3.markdown(f"<i>{each}</i>", unsafe_allow_html=True)
            else:
                col4.markdown(f"<i>{each}</i>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
