import streamlit as st
import libs.gdal2tiles.gdal2tiles as gd2
from pathlib import Path

def process_into_tiles(src_img, destination, map_name, gdal_options):
    tiles_folder = Path(destination/map_name/"tiles")
    tiles_folder.resolve().mkdir(parents=True, exist_ok=True)
    options = {
        "profile": "raster",
        "zoom": 5,
        "nb_processes": 4,
        "tile_size": 256,
        }
    gd2.generate_tiles(str(src_img), tiles_folder, **gdal_options)
    return                                                              # Return the tiles or path for the map ?

def app():
    uploads_folder = Path("library/uploads/")
    uploads_folder.resolve().mkdir(exist_ok=True)
    maps_folder = Path("library/maps/")
    maps_folder.resolve().mkdir(exist_ok=True)
    col_1, col_2 = st.columns([5,2])
    with col_1:
        st.header("Create")
        st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
    with col_2:
        col_2_sub_1, col_2_sub_2 = st.columns(2)
    with col_2_sub_1:
        save_btn = st.button("Save", type="primary", use_container_width=True)
    with col_2_sub_2:
        export_btn = st.button("Export", type="secondary", use_container_width=True)
    with col_2:
        create_tiles_options = st.expander(label="**Create Tiles**", expanded=True)
        create_map_options = st.expander(label="**Layers**", expanded=True)


    with create_tiles_options:
        library_files = list()
        for item in uploads_folder.iterdir():
            if item.is_file():
                library_files.append(item.name)
        map_name = st.text_input(label="Map Name", placeholder="Select a name for your map", help="Select a name for your map.")
        image_file = st.selectbox(label="Image File", options=library_files, help="Choose an image from the library to use as the map tile source. To upload a new image use the uploader in the sidebar and then select it from this menu.")
        min_zoom = st.selectbox(label="Min Zoom", options=[1,2,3,4,5,6,7,8,9,10], index=4, help="Select minimum zoom for tile generation.")
        max_zoom = st.selectbox(label="Max Zoom", options=[1,2,3,4,5,6,7,8,9,10], index=9, help="Select maximum zoom for tile generation.")
        tile_size = st.selectbox(label="Tile Size", options=[128,256,512], index=1, help="Select size of tiles for tile generation.")
        number_of_processes = st.selectbox(label="Number Of Processes", options=range(1,17), index=3, help="Select number of processes to use to generate tiles.")
        create_tiles_btn = st.button(label="Create Tiles", type="primary", use_container_width=True)
        update_tiles_btn = st.button(label="Update Map", type="secondary", use_container_width=True)
        try:
            if create_tiles_btn and len(map_name) > 0:
                if max_zoom and min_zoom:
                    if max_zoom <= min_zoom:
                        gdal_zoom = min_zoom
                    else:
                        gdal_zoom = [min_zoom, max_zoom]
                    gdal_options = {
                        "profile": "raster",
                        "zoom": gdal_zoom,
                        "nb_processes": number_of_processes,
                        "tile_size": tile_size,
                    }
                    for item in uploads_folder.iterdir():
                        if str(item.name) == str(image_file):
                            process_into_tiles(item.resolve(), maps_folder, map_name, gdal_options)
        except Exception as e:
            print("No file selected:", e)


    with create_map_options:
        st.selectbox(label="Select Layer", options="example")                             # Replace options dynamically in response to button press
        create_map_options_sub_1, create_map_options_sub_2 = st.columns(2)
    with create_map_options_sub_1:
        add_layer_btn = st.button(label="Add Layer", type="primary", use_container_width=True)
    with create_map_options_sub_2:
        del_layer_btn = st.button(label="Remove Layer", type="secondary", use_container_width=True)