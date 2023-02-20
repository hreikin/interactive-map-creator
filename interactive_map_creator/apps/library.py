import streamlit as st
from pathlib import Path

@st.cache_data(show_spinner="Fetching files...")
def fetch_files(directory):
    all_files = list()
    all_filenames = list()
    for item in directory.iterdir():
        if item.is_file():
            all_files.append(str(item.resolve()))
            all_filenames.append(str(item.name))

    return all_files, all_filenames

@st.cache_data(show_spinner="Loading gallery...")
def create_gallery(directory):
    col1, col2, col3, col4, col5 = st.columns(5)
    col_list = [col1, col2, col3, col4, col5]
    col_idx = 0
    filename_idx = 0
    gallery_files, gallery_filenames = fetch_files(directory)
    for img in gallery_files:
        with col_list[col_idx]:
            st.image(img, caption=gallery_filenames[filename_idx])
            if col_idx < 4:
                col_idx += 1
            else:
                col_idx = 0
            filename_idx += 1

def app():

    uploads_folder = Path("uploads")
    uploads_folder.resolve().mkdir(exist_ok=True)
    maps_folder = Path("maps")
    maps_folder.resolve().mkdir(exist_ok=True)
    
    st.header("Library")
    st.file_uploader("Upload New File", type=["png", "jpg", "jpeg"], help="Upload a new image to use as map tiles.")

    maps_dropdown = st.expander("Created Maps", expanded=True)
    source_image_dropdown = st.expander("Uploaded Images", expanded=True)
    with maps_dropdown:
        maps_gallery = st.container()
    with maps_gallery:
        create_gallery(maps_folder)
    with source_image_dropdown:
        source_gallery = st.container()
    with source_gallery:
        create_gallery(uploads_folder)