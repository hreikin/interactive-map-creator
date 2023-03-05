import streamlit as st
import logging
from pathlib import Path
import libs.gdal2tiles.gdal2tiles as gd2
import utils

logger = logging.getLogger(__name__)

class CreateTiles():
    def __init__(self, expanded=True, label="Create Map Tiles"):
        self.expanded = expanded
        self.label = label
        self.library_files = list()
        for item in utils.images_folder.iterdir():
            if item.is_file():
                self.library_files.append(item.name)
        st.session_state["library_files"] = self.library_files
        st.session_state["create_tiles_min_zoom"] = 0
        st.session_state["create_tiles_max_zoom"] = 19
        st.session_state["number_of_processes"] = 7
        self.create_tiles_options = st.expander(label=self.label, expanded=self.expanded)
        with self.create_tiles_options:
            self.create_tiles_options_msg = st.info("Create tiles from a previously uploaded image using the options available below.")
            self.create_tiles_form = st.form(key="create_tiles_form")
        with self.create_tiles_form:
            self.image_file = st.selectbox(label="Image File", options=st.session_state["library_files"], help="Choose an image from the library to use as the map tile source. To upload a new image use the uploader in the sidebar and then select it from this menu.")
            self.create_tiles_min_zoom = st.selectbox(label="Min Zoom", options=range(1,21), index=st.session_state["create_tiles_min_zoom"], help="Select minimum zoom for tile generation.")
            self.create_tiles_max_zoom = st.selectbox(label="Max Zoom", options=range(1,21), index=st.session_state["create_tiles_max_zoom"], help="Select maximum zoom for tile generation.")
            self.number_of_processes = st.selectbox(label="Number Of Processes", options=range(1,17), index=st.session_state["number_of_processes"], help="Select number of processes to use to generate tiles.")
            self.create_tiles_warning_msg = st.empty()
            self.create_tiles_spinner = st.empty()
            self.create_tiles_btn = st.form_submit_button(label="Create Tiles", type="primary", use_container_width=True)
        if self.create_tiles_btn:
            with self.create_tiles_warning_msg:
                st.warning("This process may take a long time, do not refresh the page or navigate away from it.")
            with self.create_tiles_spinner:
                with st.spinner("Creating tiles..."):
                    self.src_img = Path(utils.images_folder/str(self.image_file)).resolve()
                    self.process_into_tiles(self.src_img, self.create_tiles_min_zoom, self.create_tiles_max_zoom, self.number_of_processes)
            with self.create_tiles_warning_msg:
                st.empty()
        
    def process_into_tiles(self, src_img, min_zoom, max_zoom, number_of_processes):
        self.tiles_folder = Path(utils.tiles_folder/src_img.stem)
        self.tiles_folder.resolve().mkdir(parents=True, exist_ok=True)
        if max_zoom <= min_zoom:
            self.gdal_zoom = min_zoom
        else:
            self.gdal_zoom = [min_zoom, max_zoom]
        self.gdal_options = {
            "profile": "raster",
            "zoom": self.gdal_zoom,
            "nb_processes": number_of_processes,
            "tile_size": 256,
        }
        for item in utils.images_folder.iterdir():
            if str(item.name) == str(src_img.name):
                gd2.generate_tiles(str(src_img), self.tiles_folder, **self.gdal_options)
        st.cache_resource.clear()
        return  # Return the tiles or path for the map ?