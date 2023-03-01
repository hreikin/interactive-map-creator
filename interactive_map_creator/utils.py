import streamlit as st
import subprocess
import sys
from pathlib import Path
from PIL import Image
import libs.gdal2tiles.gdal2tiles as gd2

server_started = False
webserver_root = Path("library/tiles/")
uploads_folder = Path("library/uploads/")
uploads_folder.resolve().mkdir(parents=True, exist_ok=True)
icons_folder = Path(f"{uploads_folder}/icons")
icons_folder.resolve().mkdir(parents=True, exist_ok=True)
tiles_folder = Path("library/tiles/")
tiles_folder.resolve().mkdir(parents=True, exist_ok=True)
maps_folder = Path("library/maps/")
maps_folder.resolve().mkdir(parents=True, exist_ok=True)

home_images = [
    Path("assets/images/example_map_01.png"),
    Path("assets/images/example_map_02.png"),
]

def create_server():
    subprocess.run([sys.executable, "-m", "http.server", "-d", webserver_root, "8888"])


def load_images(images=list()):
    for img in images:
        st.image(str(img.resolve()))

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

def process_into_tiles(src_img, destination, gdal_options):
    tiles_folder = Path(destination/src_img.stem)
    tiles_folder.resolve().mkdir(parents=True, exist_ok=True)
    gd2.generate_tiles(str(src_img), tiles_folder, **gdal_options)
    return                                                              # Return the tiles or path for the map ?