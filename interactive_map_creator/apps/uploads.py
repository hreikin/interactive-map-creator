import streamlit as st
import logging
import utils
from streamlit_uploads_library.library import Library
from streamlit_uploads_library.uploads import UploadFiles
from tiles import CreateTiles

logger = logging.getLogger(__name__)

def app():
    with st.sidebar:
        sidebar_info_msg = st.info("Upload new images or icons and view your previously uploaded files and created tile sets.")
        with st.expander(label="Upload Files", expanded=True):
            upload_images = UploadFiles(save_location="library/images/", header="Images", info_msg="Upload images to create tiles from here.", uid="images", upload_label="Upload Images")
            upload_icons = UploadFiles(save_location="library/icons/", header="Icons", info_msg="Upload custom icons to use on your map here.", uid="icons", upload_label="Upload Icons")
        create_tiles = CreateTiles()
    images_expander = st.expander(label="Images", expanded=True)
    icons_expander = st.expander(label="Icons", expanded=True)
    with images_expander:
        images_library = Library(directory=utils.images_folder, uid="images")
    with icons_expander:
        icons_library = Library(directory=utils.icons_folder, uid="icons")