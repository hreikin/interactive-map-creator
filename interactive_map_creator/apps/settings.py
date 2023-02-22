import streamlit as st
import utils

def app():
    with st.sidebar:
        sidebar_msg = st.info(
            """
            Some text.
            """
            )