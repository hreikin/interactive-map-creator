import streamlit as st
from pathlib import Path
from PIL import Image

def save_uploaded_file(file_to_upload, destination):
    full_path = Path(f"{destination}/{file_to_upload.name}")
    with Image.open(file_to_upload) as f:
        f.save(full_path)

def fetch_files(directory):
    all_files = list()
    all_filenames = list()
    file_extensions = (".png", ".jpg", ".jpeg")
    if directory.stem == "maps":
        for item in directory.rglob("screenshot.*"):
            all_files.append(str(item.resolve()))
            all_filenames.append(str(item.parent.name))
    if directory.stem == "uploads":
        for item in directory.rglob("*"):
            if item.is_file() and str(item).endswith(file_extensions):
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
    uploads_folder = Path("library/uploads/")
    uploads_folder.resolve().mkdir(parents=True, exist_ok=True)
    maps_folder = Path("library/maps/")
    maps_folder.resolve().mkdir(parents=True, exist_ok=True)
    with st.sidebar:
        sidebar_msg = st.info(
            """
            Upload new files, edit previous maps and view your library of source images, created tiles and maps.
            """
            )
        uploaded_file = st.file_uploader("Upload New File", type=["png", "jpg", "jpeg"], help="Upload a new image to use as map tiles.")
        if uploaded_file is not None:
            save_uploaded_file(uploaded_file, uploads_folder)
            st.cache_data.clear()
    st.header("Library")
    maps_dropdown = st.expander("**Created Maps**", expanded=True)
    source_image_dropdown = st.expander("**Uploaded Images**", expanded=True)
    with maps_dropdown:
        maps_gallery = st.container()
    with maps_gallery:
        create_gallery(maps_folder)
    with source_image_dropdown:
        source_gallery = st.container()
    with source_gallery:
        create_gallery(uploads_folder)