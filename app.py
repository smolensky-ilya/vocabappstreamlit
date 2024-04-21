import streamlit as st
from random import randint
from db_connection import Db
from gpt import Gpt

st.set_page_config(page_title='Vocab Booster 3000 | SMK')
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

# INIT GPT
if "gpt" not in st.session_state:
    st.session_state.gpt = Gpt()


def apply_explainer(what: str = None):
    def inner():
        st.session_state.explain_prompt = what
    return inner


def insert_chunk_columns(prefix, interator_list):
    cols = st.columns(chunk_columns)
    iterator = chunk_iterator(interator_list)
    for i, each in enumerate(cols):
        for j in range(chunks_per_column):
            button_text = next(iterator)
            each.button(button_text, on_click=apply_explainer(what=button_text), key=f"{prefix}_" + button_text +
                                                                                     str(randint(1, 10000)))


def clean_session_state(exception: list = None):
    for key in st.session_state.keys():
        if key not in ['gpt', 'messages'] + (exception if exception is not None else []):
            del st.session_state[key]


def get_other_chunks():
    clean_session_state()
    st.session_state.other_expressions = database.get_other_chunks(limit=limits_for_db)['expression'].to_list()


def get_sc_mats():
    clean_session_state()
    st.session_state.sc_data = database.get_club_topics(pars_per_page)
    st.session_state.sc_expressions = database.get_expressions(topics=st.session_state.sc_data['topic'],
                                                               limit=limits_for_db)


def generate_materials():
    clean_session_state()
    st.session_state.chunks_for_generation = database.get_random_exp_from_both(limits_for_db)['expressions'].to_list()
    prompt = f'Please generate a short question on a modern topic to discuss using Advanced English and these chunks:' \
             f'{", ".join(st.session_state.chunks_for_generation[:2])}. ' \
             f'Please just write the question and nothing else.'
    st.session_state.generated_question = st.session_state.gpt.ask_gpt(prompt)
    prompt = 'Please write a paragraph answering the question using advanced English and the same chunks.' \
             'Please make those chunks bold in the text using markdown.'
    st.session_state.generated_response = st.session_state.gpt.ask_gpt(prompt)


def toggle_chat():
    clean_session_state(exception=['open_chat', 'chunks_for_generation', 'generated_question', 'generated_response'])
    st.session_state.open_chat = not st.session_state.open_chat


def chunk_iterator(list_of_chunks):
    for each in list_of_chunks:
        yield each


def main():
    # MAIN
    st.header(':rocket: :blue[_Vocab Booster 3000_]', divider='rainbow')
    st.button('Generate a discussion question :robot_face:', use_container_width=True, on_click=generate_materials)
    st.button('Get Some Chunks :open_book:', use_container_width=True, on_click=get_other_chunks)
    st.button('Get Some Speaking Club Materials :nerd_face:', use_container_width=True, on_click=get_sc_mats)
    st.button(f'{"Open" if not st.session_state.open_chat else "Close"} GPT :the_horns:', use_container_width=True,
              on_click=toggle_chat)

    if 'generated_question' in st.session_state:
        st.subheader(st.session_state.generated_question)
        st.write('')
        st.markdown(st.session_state.generated_response)
        insert_chunk_columns(prefix='gen', interator_list=st.session_state.chunks_for_generation)

    if 'other_expressions' in st.session_state:
        insert_chunk_columns(prefix='exp', interator_list=st.session_state.other_expressions)

    if 'explain_prompt' in st.session_state:
        with st.chat_message("assistant"):
            with st.spinner('A KNOW-IT-ALL is thinking :nerd_face:'):
                prompt = "Please explain what this chunk means: " + st.session_state.explain_prompt
                st.write(f"{st.session_state.gpt.ask_gpt(prompt)}!")

    if "sc_data" in st.session_state and "sc_expressions" in st.session_state:
        data = st.session_state.sc_data
        expressions = st.session_state.sc_expressions
        for index, row in data.iterrows():
            st.write(f"---")
            st.markdown(f"<i>{row['topic'].replace('_', ' ')}</i>", unsafe_allow_html=True)
            st.subheader(f"{row['questions'][2:]}")
            st.write(f"")
            st.write(f"{row['answers']}")
            st.write(f"")
            insert_chunk_columns(prefix='sc', interator_list=expressions.
                                 query('topic == @row["topic"]')['expressions'].to_list())

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
