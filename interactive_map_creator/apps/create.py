import streamlit as st
import libs.gdal2tiles.gdal2tiles as gd2
from pathlib import Path
from PIL import Image

def save_uploaded_file(file_to_upload, destination):
    full_path = Path(f"{destination}/{file_to_upload.name}")
    with Image.open(file_to_upload) as f:
        f.save(full_path)
    return full_path

def process_into_tiles(src_img, destination):
    tiles_folder = Path(destination/src_img.stem/"tiles")
    tiles_folder.resolve().mkdir(parents=True, exist_ok=True)
    options = {
        "profile": "raster",
        "zoom": 5,
        "nb_processes": 4,
        "tile_size": 256,
        }
    gd2.generate_tiles(str(src_img.resolve()), tiles_folder, **options)
    return                                                              # Return the tiles or path for the map ?

def app():
    uploads_folder = Path("library/uploads/")
    uploads_folder.resolve().mkdir(exist_ok=True)
    maps_folder = Path("library/maps/")
    maps_folder.resolve().mkdir(exist_ok=True)
    col_1, col_2 = st.columns([5,2])
    with st.sidebar:
        uploaded_file = st.file_uploader("Upload New File", type=["png", "jpg", "jpeg"], help="Upload a new image to use as map tiles.")
        if uploaded_file is not None:
            full_path = save_uploaded_file(uploaded_file, uploads_folder)
            st.cache_data.clear()
    with col_1:
        st.header("Create")
        st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
    with col_2:
        sub_1, sub_2 = st.columns(2)
    with sub_1:
        save_btn = st.button("Save", type="primary", use_container_width=True)
    with sub_2:
        export_btn = st.button("Export", type="secondary", use_container_width=True)
    with col_2:
        create_tiles_options = st.expander(label="**Create Tiles**", expanded=True)
        with create_tiles_options:

            library_options = list()
            for item in uploads_folder.iterdir():
                if item.is_file():
                    library_options.append(item.stem)
            st.text_input(label="Map Name", placeholder="Select a name for your map", help="Select a name for your map.")
            st.selectbox(label="Image File", options=library_options, help="Choose an image from the library to use as the map tile source. To upload a new image use the uploader in the sidebar and then selct it from this menu.")
            st.selectbox(label="Min Zoom", options=range(1,11), index=4, help="Select minimum zoom for tile generation.")
            st.selectbox(label="Max Zoom", options=range(1,11), index=9, help="Select maximum zoom for tile generation.")
            st.selectbox(label="Tile Size", options=[128,256,512], index=1, help="Select size of tiles for tile generation.")
            st.selectbox(label="Number Of Processes", options=range(1,17), index=3, help="Select number of processes to use to generate tiles.")
            create_tiles_btn = st.button("Create Tiles", type="primary", on_click=lambda: process_into_tiles(full_path, maps_folder), use_container_width=True)
            update_tiles_btn = st.button("Update Map", type="secondary", use_container_width=True)