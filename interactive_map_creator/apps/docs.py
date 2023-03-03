import streamlit as st
import logging
import utils

logger = logging.getLogger(__name__)

def app():
    with st.sidebar:
        sidebar_msg = st.info(
            """
            Here you can find helpful user guides, FAQ's and links to the source code and documentation.
            """
            )