import streamlit as st
import logging
import utils
from gallery import ImageGallery, MapGallery
from tiles import CreateTiles
from uploading import UploadFiles

logger = logging.getLogger(__name__)

def app():
    with st.sidebar:
        sidebar_info_msg = st.info("Upload new images or icons and view your previously uploaded files and created tile sets.")
        upload_files = UploadFiles()
        create_tiles = CreateTiles()
    tiles_gallery = MapGallery(directory=utils.tiles_folder, label="**Tiles**")
    images_gallery = ImageGallery(directory=utils.images_folder)
    icons_gallery = ImageGallery(directory=utils.icons_folder, label="**Icons**")