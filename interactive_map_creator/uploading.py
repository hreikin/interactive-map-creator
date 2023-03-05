import streamlit as st
import logging
from pathlib import Path
from PIL import Image
import utils

logger = logging.getLogger(__name__)

class UploadFiles():
    def __init__(self, expanded=True, label="Upload Icons and Images"):
        self.expanded = expanded
        self.label = label
        self.upload_options = st.expander(label=self.label, expanded=self.expanded)
        with self.upload_options:
            self.upload_options_msg = st.info("Upload images here to use as the base for tile creation or marker icons.")
            self.uploaded_file = st.file_uploader("Upload Image File", type=["png", "jpg", "jpeg"], help="Upload a new image to create map tiles from.")
            self.uploaded_icon = st.file_uploader("Upload Icon File", type=["png", "jpg", "jpeg"], help="Upload a new icon to use as a marker.")
        if self.uploaded_file is not None:
            self.save_uploaded_file(self.uploaded_file, utils.images_folder)
        if self.uploaded_icon is not None:
            self.save_uploaded_file(self.uploaded_icon, utils.icons_folder)

    def save_uploaded_file(self, file_to_upload, destination):
        self.full_path = Path(f"{destination}/{file_to_upload.name}")
        with Image.open(file_to_upload) as f:
            f.save(self.full_path)
        st.cache_resource.clear()