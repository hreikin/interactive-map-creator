import streamlit as st
import logging
import utils
from gallery import MapGallery

logger = logging.getLogger(__name__)

def app():
    with st.sidebar:
        sidebar_msg = st.info(
            """
            Your own personal atlas, view your collection of maps.
            """
        )
    maps_gallery = MapGallery(directory=utils.maps_folder)