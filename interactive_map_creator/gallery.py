import streamlit as st
import logging

logger = logging.getLogger(__name__)

# @st.cache_resource(show_spinner="Refreshing gallery...")
# @st.cache_data(show_spinner="Refreshing gallery...")
#
# Enabling either of the above causes the following error:
#
# TypeError: CachedFunc.__init__() takes 2 positional arguments but 4 were given
# Traceback:
# File "/data/data/com.termux/files/home/git/interactive-map-creator/.venv/lib/python3.11/site-packages/streamlit/runtime/scriptrunner/script_runner.py", line 565, in _run_script
#     exec(code, module.__dict__)
# File "/data/data/com.termux/files/home/git/interactive-map-creator/interactive_map_creator/main.py", line 5, in <module>
#     from apps import create, docs, home, maps, uploads
# File "/data/data/com.termux/files/home/git/interactive-map-creator/interactive_map_creator/apps/maps.py", line 4, in <module>
#     from gallery import ImageGallery, MapGallery
# File "/data/data/com.termux/files/home/git/interactive-map-creator/interactive_map_creator/gallery.py", line 76, in <module>
#     class MapGallery(ImageGallery):
class ImageGallery():
    def __init__(self, directory, expanded=True, file_extensions=(".png", ".jpg", ".jpeg"), label="**Images**"):
        self.directory = directory
        self.expanded = expanded
        self.file_extensions = file_extensions
        self.label = label
        self.gallery = self.create_gallery()

    def fetch_files(self):
        self.all_files = list()
        self.all_filenames = list()
        for item in self.directory.rglob("*"):
            if item.is_file() and item.name.endswith(self.file_extensions):
                self.all_files.append(str(item.resolve()))
                self.all_filenames.append(str(item.name))
        return self.all_files, self.all_filenames

    # @st.cache_resource(show_spinner="Refreshing gallery...")
    # @st.cache_data(show_spinner="Refreshing gallery...")
    #
    # Enabling either of the above causes the following error:
    #
    # TypeError: ImageGallery.create_gallery() missing 1 required positional argument: 'self'
    # Traceback:
    # File "/data/data/com.termux/files/home/git/interactive-map-creator/.venv/lib/python3.11/site-packages/streamlit/runtime/scriptrunner/script_runner.py", line 565, in _run_script
    #     exec(code, module.__dict__)
    # File "/data/data/com.termux/files/home/git/interactive-map-creator/interactive_map_creator/main.py", line 70, in <module>
    #     app["func"]()
    # File "/data/data/com.termux/files/home/git/interactive-map-creator/interactive_map_creator/apps/uploads.py", line 15, in app
    #     tiles_gallery = MapGallery(directory=utils.tiles_folder, label="**Tiles**")
    #                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # File "/data/data/com.termux/files/home/git/interactive-map-creator/interactive_map_creator/gallery.py", line 93, in __init__
    #     super(MapGallery, self).__init__(directory, expanded, file_extensions, label)
    # File "/data/data/com.termux/files/home/git/interactive-map-creator/interactive_map_creator/gallery.py", line 27, in __init__
    #     self.gallery = self.create_gallery()
    #                    ^^^^^^^^^^^^^^^^^^^^^
    # File "/data/data/com.termux/files/home/git/interactive-map-creator/interactive_map_creator/gallery.py", line 107, in create_gallery
    #     return super().create_gallery()
    #            ^^^^^^^^^^^^^^^^^^^^^^^^
    # File "/data/data/com.termux/files/home/git/interactive-map-creator/.venv/lib/python3.11/site-packages/streamlit/runtime/caching/cache_utils.py", line 186, in __call__
    #     return self._get_or_create_cached_value(args, kwargs)
    #            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # File "/data/data/com.termux/files/home/git/interactive-map-creator/.venv/lib/python3.11/site-packages/streamlit/runtime/caching/cache_utils.py", line 211, in _get_or_create_cached_value
    #     return self._handle_cache_miss(cache, value_key, func_args, func_kwargs)
    #            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # File "/data/data/com.termux/files/home/git/interactive-map-creator/.venv/lib/python3.11/site-packages/streamlit/runtime/caching/cache_utils.py", line 265, in _handle_cache_miss
    #     computed_value = self._info.func(*func_args, **func_kwargs)
    #                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def create_gallery(self):
        self.source_image_dropdown = st.expander(label=self.label, expanded=self.expanded)
        with self.source_image_dropdown:
            self.source_gallery = st.container()
        with self.source_gallery:
            self.col1, self.col2, self.col3, self.col4, self.col5 = st.columns(5)
            self.col_list = [self.col1, self.col2, self.col3, self.col4, self.col5]
            self.col_idx = 0
            self.filename_idx = 0
            self.gallery_files, self.gallery_filenames = self.fetch_files()
            for img in self.gallery_files:
                with self.col_list[self.col_idx]:
                    st.image(img, caption=self.gallery_filenames[self.filename_idx], use_column_width=True)
                    if self.col_idx < 4:
                        self.col_idx += 1
                    else:
                        self.col_idx = 0
                    self.filename_idx += 1
        return self.source_image_dropdown

# @st.cache_resource(show_spinner="Refreshing gallery...")
# @st.cache_data(show_spinner="Refreshing gallery...")
class MapGallery(ImageGallery):
    def __init__(self, directory, expanded=True, file_extensions=(".png", ".jpg", ".jpeg"), label="**Images**"):
        super(MapGallery, self).__init__(directory, expanded, file_extensions, label)

    def fetch_files(self):
        self.all_files = list()
        self.all_filenames = list()
        for item in self.directory.rglob("screenshot.*"):
            if item.is_file():
                self.all_files.append(str(item.resolve()))
                self.all_filenames.append(str(item.parent.name))
        return self.all_files, self.all_filenames

    # @st.cache_resource(show_spinner="Refreshing gallery...")
    # @st.cache_data(show_spinner="Refreshing gallery...")
    def create_gallery(_self):
        return super().create_gallery()