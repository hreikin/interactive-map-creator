import streamlit as st
from pathlib import Path
from streamlit_uploads_library.gallery import Gallery
import logging

logger = logging.getLogger(__name__)

class MapGallery(Gallery):
    def __init__(self, directory, file_extensions=(".png", ".jpg", ".jpeg"), image_alignment="center", number_of_columns=5, show_details=False, uid="map-gallery"):
        self.directory = directory
        self.file_extensions = file_extensions
        self.image_alignment = image_alignment
        self.number_of_columns = number_of_columns
        self.show_details = show_details
        self.uid = uid
        super(Gallery, self).__init__(self.directory, self.file_extensions, self.image_alignment, self.number_of_columns, self.show_details, self.uid)

    def fetch_files(self, directory, file_extensions):
        """Returns a list of all files.
        Returns a list of files to be used by create_library().
        Args:
            directory (str): A str() of the path to the folder containing the library images, for example, "assets".
            file_extensions (tuple): A tuple() containing strings of the file extensions to include in the library, default is (".png", ".jpg", ".jpeg").
        
        Returns:
            all_files (list): A list of files.
            all_filenames (list): A list of filenames.
        """
        all_files = list()
        for item in directory.rglob("screenshot*"):
            if item.is_file() and item.name.endswith(file_extensions):
                all_files.append(str(item.resolve()))
        return all_files

    @st.cache_resource(experimental_allow_widgets=True, show_spinner="Refreshing gallery...")
    def create_gallery(_self, directory, file_extensions, image_alignment, number_of_columns, show_details, uid):
        """Creates a simple gallery with columns.
        Creates a gallery using columns out of streamlit widgets.
        Args:
            directory (str): A str() of the path to the folder containing the gallery images, for example, "assets".
            file_extensions (tuple): A tuple() containing strings of the file extensions to include in the gallery, default is (".png", ".jpg", ".jpeg").
            image_alignment (str): A str() with the CSS keyword used to align the images and details columns.
            number_of_columns (int): An int() indicating the number of columns to create.
            show_details (bool): A bool() that when set to True allows the creation of libraries, default is False to create a gallery.
            uid (str): A str() containing a unique identifier allowing you to create multiple libraries on the same page containing the same images.
        
        Returns:
            library_gallery_container (st.container): A streamlit widget containing the gallery.
        """
        return super().create_library(directory, file_extensions, image_alignment, number_of_columns, show_details, uid)