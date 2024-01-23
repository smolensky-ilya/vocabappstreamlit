import pandas as pd
from sqlalchemy import create_engine
import streamlit as st


class Db:
    def __init__(self):
        connection_string = ''
