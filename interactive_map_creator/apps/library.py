import streamlit as st
import utils

def app():
    with st.sidebar:
        sidebar_msg = st.info(
            """
            Upload new files, edit previous maps and view your library of source images, created tiles and maps.
            """
            )
        uploaded_file = st.file_uploader("Upload New File", type=["png", "jpg", "jpeg"], help="Upload a new image to use as map tiles.")
        if uploaded_file is not None:
            utils.save_uploaded_file(uploaded_file, utils.uploads_folder)
    st.header("Library")
    maps_dropdown = st.expander("**Created Maps**", expanded=True)
    source_image_dropdown = st.expander("**Uploaded Images**", expanded=True)
    with maps_dropdown:
        maps_gallery = st.container()
    with maps_gallery:
        utils.create_gallery(utils.maps_folder)
    with source_image_dropdown:
        source_gallery = st.container()
    with source_gallery:
        utils.create_gallery(utils.uploads_folder)