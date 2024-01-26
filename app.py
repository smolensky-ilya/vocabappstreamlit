import streamlit as st
from db_connection import Db


st.set_page_config(page_title='Speaking Club Material', initial_sidebar_state='collapsed')
database = Db()
pars_per_page_def = 5
chunk_columns_def = 4
chunks_per_column_def = 5


def rev_link_gen(chunk):
    return f'<a href="https://context.reverso.net/translation/english-russian/{chunk}" ' \
           f'target="_blank" style="color: inherit; text-decoration: none;"><i>{chunk}</i></a>'


def chunk_iterator(list_of_chunks):
    for each in list_of_chunks:
        yield each


def main():
    # SIDEBAR
    st.sidebar.subheader('Settings')
    pars_per_page = st.sidebar.number_input('Paragraphs / page', min_value=1, max_value=10, value=pars_per_page_def)
    chunk_columns = st.sidebar.number_input('Chunk cols', min_value=1, max_value=10, value=chunk_columns_def)
    chunks_per_column = st.sidebar.number_input('Chunks / col', min_value=1, max_value=10, value=chunks_per_column_def)
    limits_for_db = chunks_per_column * chunk_columns

    # MAIN
    get_other_chunks = st.button('Get Some Chunks', use_container_width=True)
    get_sc_mats = st.button('Get Some Speaking Material', use_container_width=True)

    if get_other_chunks:
        cols = st.columns(chunk_columns)
        expressions = chunk_iterator(database.get_other_chunks(limit=limits_for_db)['expression'].to_list())
        for each in cols:
            for _ in range(chunks_per_column):
                each.markdown(rev_link_gen(next(expressions)), unsafe_allow_html=True)

    if get_sc_mats:
        data = database.get_club_topics(pars_per_page)
        expressions = database.get_expressions(topics=data['topic'], limit=limits_for_db)
        for index, row in data.iterrows():
            st.write(f"---")
            st.markdown(f"<i>{row['topic'].replace('_', ' ')}</i>", unsafe_allow_html=True)
            st.subheader(f"{row['questions'][2:]}")
            st.write(f"")
            st.write(f"{row['answers']}")
            st.write(f"")
            exp_list = chunk_iterator(expressions.query('topic == @row["topic"]')['expressions'].to_list())
            cols = st.columns(chunk_columns)
            for each in cols:
                for _ in range(chunks_per_column):
                    each.markdown(rev_link_gen(next(exp_list)), unsafe_allow_html=True)


if __name__ == "__main__":
    main()
