import streamlit as st
from db_connection import Db
from gpt import Gpt

st.set_page_config(page_title='Speaking Club Material', initial_sidebar_state='collapsed')
database = Db()
pars_per_page = 5
chunk_columns = 4
chunks_per_column = 5
limits_for_db = chunk_columns * chunks_per_column

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# OPEN CHAT
if "open_chat" not in st.session_state:
    st.session_state.open_chat = False

# OPEN CHAT
if "gpt" not in st.session_state:
    st.session_state.gpt = Gpt()


def apply_explainer(what: str = None):
    def inner():
        st.session_state.explain_prompt = what
    return inner


def clean_session_state(exception: str = None):
    for key in st.session_state.keys():
        if key not in ['gpt', 'messages'] + ([exception] if exception is not None else []):
            st.session_state[key] = None


def get_other_chunks():
    clean_session_state()
    st.session_state.other_expressions = database.get_other_chunks(limit=limits_for_db)['expression'].to_list()


def get_sc_mats():
    clean_session_state()
    st.session_state.sc_data = database.get_club_topics(pars_per_page)
    st.session_state.sc_expressions = database.get_expressions(topics=st.session_state.sc_data['topic'],
                                                               limit=limits_for_db)


def toggle_chat():
    clean_session_state(exception='open_chat')
    st.session_state.open_chat = not st.session_state.open_chat


def chunk_iterator(list_of_chunks):
    for each in list_of_chunks:
        yield each


def main():
    # MAIN
    st.header(':rocket: :blue[_Vocab Booster 3000_]', divider='rainbow')
    st.button('Generate discussion materials *COMING_SOON', use_container_width=True, on_click=get_other_chunks,
              disabled=True)
    st.button('Get Some Chunks', use_container_width=True, on_click=get_other_chunks)
    st.button('Get Some Speaking Club Materials', use_container_width=True, on_click=get_sc_mats)
    st.button(f'{"Open" if not st.session_state.open_chat else "Close"} GPT', use_container_width=True,
              on_click=toggle_chat)

    if 'other_expressions' in st.session_state:
        if st.session_state.other_expressions is not None:
            cols = st.columns(chunk_columns)
            iterator = chunk_iterator(st.session_state.other_expressions)
            for i, each in enumerate(cols):
                for _ in range(chunks_per_column):
                    button_text = next(iterator)
                    each.button(button_text, on_click=apply_explainer(what=button_text), key="exp_" + button_text +
                                                                                             str(i) + str(_))

    if 'explain_prompt' in st.session_state:
        if st.session_state.explain_prompt is not None:
            with st.chat_message("assistant"):
                prompt = "Please explain what this chunk means: " + st.session_state.explain_prompt
                st.write(f"{st.session_state.gpt.ask_gpt(prompt)}!")

    if "sc_data" in st.session_state and "sc_expressions" in st.session_state:
        if st.session_state.sc_data is not None and st.session_state.sc_expressions is not None:
            data = st.session_state.sc_data
            expressions = st.session_state.sc_expressions
            for index, row in data.iterrows():
                st.write(f"---")
                st.markdown(f"<i>{row['topic'].replace('_', ' ')}</i>", unsafe_allow_html=True)
                st.subheader(f"{row['questions'][2:]}")
                st.write(f"")
                st.write(f"{row['answers']}")
                st.write(f"")
                cols = st.columns(chunk_columns)
                iterator = chunk_iterator(expressions.query('topic == @row["topic"]')['expressions'].to_list())
                for i, each in enumerate(cols):
                    for _ in range(chunks_per_column):
                        button_text = next(iterator)
                        each.button(button_text, on_click=apply_explainer(what=button_text), key="sc_" + button_text +
                                                                                                 str(i) + str(_))

    if st.session_state.open_chat:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if chat_prompt := st.chat_input(placeholder="Your message", max_chars=1000):
            with st.chat_message("user"):
                st.write(f"{chat_prompt}")
                st.session_state.messages.append({"role": "user", "content": chat_prompt})
            with st.chat_message("assistant"):
                gpt_reply = st.session_state.gpt.ask_gpt(chat_prompt)
                st.write(f"{gpt_reply}")
                st.session_state.messages.append({"role": "assistant", "content": gpt_reply})


if __name__ == "__main__":
    main()
