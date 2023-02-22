import streamlit as st
from interactive_map_creator import utils

def app():
    with st.sidebar:
        sidebar_msg = st.info(
            """
            Some text.
            """
            )
    st.header("Settings")