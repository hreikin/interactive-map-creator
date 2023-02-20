import streamlit as st
from pathlib import Path
from PIL import Image

def save_uploaded_file(file_to_upload, location):
    with Image.open(file_to_upload) as f:
        full_path = Path(f"{location}/{file_to_upload.name}")
        f.save(full_path)

def app():

    uploads_folder = Path("uploads")
    uploads_folder.resolve().mkdir(exist_ok=True)
    maps_folder = Path("maps")
    maps_folder.resolve().mkdir(exist_ok=True)
    col_1, col_2 = st.columns([5,2])

    with col_1:
        st.header("Create")
        st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")

    with col_2:
        uploaded_file = st.file_uploader("Upload New File", type=["png", "jpg", "jpeg"], help="Upload a new image to use as map tiles.")
        if uploaded_file is not None:
            save_uploaded_file(uploaded_file, uploads_folder)
            st.cache_data.clear()
        
        save_btn = st.button("Save", type="primary")
        export_btn = st.button("Export", type="primary")