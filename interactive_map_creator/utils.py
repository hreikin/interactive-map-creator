import streamlit as st
import logging, subprocess, sys, threading
from pathlib import Path
from PIL import Image

logger = logging.getLogger(__name__)

library_folder = Path("library/")
library_folder.resolve().mkdir(parents=True, exist_ok=True)
icons_folder = Path(f"{library_folder}/icons")
icons_folder.resolve().mkdir(parents=True, exist_ok=True)
images_folder = Path(f"{library_folder}/images")
images_folder.resolve().mkdir(parents=True, exist_ok=True)
tiles_folder = Path(f"{library_folder}/tiles/")
tiles_folder.resolve().mkdir(parents=True, exist_ok=True)
maps_folder = Path(f"{library_folder}/maps/")
maps_folder.resolve().mkdir(parents=True, exist_ok=True)
tileserver_root = Path(f"{library_folder}/tiles/")

home_images = [
    Path("assets/images/example_map_01.png"),
    Path("assets/images/example_map_02.png"),
]

@st.cache_resource
def create_server():
    thread = threading.Thread(target=start_server).start()
    return thread

def start_server():
    process = subprocess.run([sys.executable, "-m", "http.server", "-d", tileserver_root, "8888"])
    return process

@st.cache_data
def load_images(images=list()):
    for img in images:
        st.image(str(img.resolve()))
