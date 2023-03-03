import streamlit as st
import logging
import utils

logger = logging.getLogger(__name__)

def app():
    with st.sidebar:
        sidebar_msg = st.info(
            """
            Your own personal atlas, view your collection of maps.
            """
            )
    maps_dropdown = st.expander("**Created Maps**", expanded=True)
    with maps_dropdown:
        maps_gallery = st.container()
    with maps_gallery:
        utils.create_gallery(utils.maps_folder)