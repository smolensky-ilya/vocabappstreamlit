import streamlit as st
from db_connection import Db


st.set_page_config(page_title='Speaking Club Material')
database = Db()
pars_per_page = 5


def rev_link_gen(chunk):
    return f"<a href='https://context.reverso.net/translation/english-russian/{chunk}' " \
           f"target='_blank' style='color: inherit; text-decoration: none;'><i>{chunk}</i></a>"


def main():
    columns = st.columns(2)
    for each in columns:
        each.write('col')
        sub_cols = each.columns(3)
        for each1 in sub_cols:
            each1.write('1')

    refresh = st.button('Get Some Speaking Material', use_container_width=True)
    if refresh:
        data = database.get_club_topics(pars_per_page)
        expressions = database.get_expressions(topics=data['topic'], limit=20)
        for index, row in data.iterrows():
            st.write(f"---")
            st.markdown(f"<i>{row['topic'].replace('_', ' ')}</i>", unsafe_allow_html=True)
            st.subheader(f"{row['questions'][2:]}")
            st.write(f"")
            st.write(f"{row['answers']}")
            st.write(f"")
            exp_list = expressions.query('topic == @row["topic"]')['expressions'].to_list()
            col1, col2, col3, col4 = st.columns(4)
            for i, each in enumerate(exp_list):
                if i % 4 == 0:
                    col1.markdown(rev_link_gen(each), unsafe_allow_html=True)
                elif i % 4 == 1:
                    col2.markdown(rev_link_gen(each), unsafe_allow_html=True)
                elif i % 4 == 2:
                    col3.markdown(rev_link_gen(each), unsafe_allow_html=True)
                else:
                    col4.markdown(rev_link_gen(each), unsafe_allow_html=True)


if __name__ == "__main__":
    main()
