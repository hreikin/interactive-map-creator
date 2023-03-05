import streamlit as st
import logging
from mapmaking import CreateMap

logger = logging.getLogger(__name__)

def app():
    with st.sidebar:
        info_msg = st.info("Create your new map by following the steps outlined below, if you have uploaded images and icons or created a tile set previously it is safe to skip those steps.")
    create = CreateMap()