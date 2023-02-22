import streamlit as st
import utils

def app():
    col_1, col_2 = st.columns([5,2])
    with st.sidebar:
        step_1_msg = st.info(
            """
            ### Step 1 (optional)

            Upload a file to use as the base for tile creation. If you want to use a previously uploaded file then it is safe to skip this step.
            """
            )
        upload_options = st.expander(label="Upload", expanded=True)
        step_2_msg = st.info(
            """
            ### Step 2 (optional)

            Create tiles from a previously uploaded image using the options available below. If you want to re-use some previously created tiles then it is safe to skip this step.
            """
            )
        create_tiles_options = st.expander(label="**Create Tiles**", expanded=True)
    with upload_options:
        uploaded_file = st.file_uploader("Upload New File", type=["png", "jpg", "jpeg"], help="Upload a new image to use as map tiles.")
        if uploaded_file is not None:
            utils.save_uploaded_file(uploaded_file, utils.uploads_folder)
    with create_tiles_options:
        library_files = list()
        for item in utils.uploads_folder.iterdir():
            if item.is_file():
                library_files.append(item.name)
        image_file = st.selectbox(label="Image File", options=library_files, help="Choose an image from the library to use as the map tile source. To upload a new image use the uploader in the sidebar and then select it from this menu.")
        min_zoom = st.selectbox(label="Min Zoom", options=range(1,11), index=4, help="Select minimum zoom for tile generation.")
        max_zoom = st.selectbox(label="Max Zoom", options=range(1,11), index=4, help="Select maximum zoom for tile generation.")
        tile_size = st.selectbox(label="Tile Size", options=[128,256,512], index=1, help="Select size of tiles for tile generation.")
        number_of_processes = st.selectbox(label="Number Of Processes", options=range(1,17), index=3, help="Select number of processes to use to generate tiles.")
        create_tiles_btn = st.button(label="Create Tiles", type="primary", use_container_width=True)
        try:
            if create_tiles_btn:
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
                    for item in utils.uploads_folder.iterdir():
                        if str(item.name) == str(image_file):
                            utils.process_into_tiles(item.resolve(), utils.tiles_folder, gdal_options)
        except Exception as e:
            print("No file selected:", e)
    with col_1:
        st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
    with col_2:
        col_2_sub_1, col_2_sub_2 = st.columns(2)
        step_3_msg = st.info(
            """
            ##### Step 3 (required):

            Create your map by defining the options available below. The map will update to reflect your changes, make sure to save often to avoid losing any work.
            """
            )
        map_options = st.expander(label="**Map Options**", expanded=True)
        layer_options = st.expander(label="**Layer Options**", expanded=True)
        pin_options = st.expander(label="**Pin Options**", expanded=True)
        zone_options = st.expander(label="**Zone Options**", expanded=True)
    with col_2_sub_1:
        save_btn = st.button("Save", type="primary", use_container_width=True)
    with col_2_sub_2:
        export_btn = st.button("Export", type="secondary", use_container_width=True)




    with map_options:
        map_name = st.text_input(label="Map Name", placeholder="Select a name for your map", help="Select a name for your map.")
        library_tiles = list()
        for item in utils.tiles_folder.iterdir():
            if item.is_dir():
                library_tiles.append(item.name)
        tile_file = st.selectbox(label="Tile Source", options=library_tiles, help="Choose tiles from the library to use as the map tile source. To create new tiles use the tile creation options available in the sidebar and then select them here.")
    with layer_options:
        st.selectbox(label="Select Layer", options="example")                             # Replace options dynamically in response to button press
        layer_options_sub_1, layer_options_sub_2 = st.columns(2)
    with layer_options_sub_1:
        add_layer_btn = st.button(label="Add Layer", type="primary", use_container_width=True)
    with layer_options_sub_2:
        del_layer_btn = st.button(label="Remove Layer", type="secondary", use_container_width=True)
    with pin_options:
        st.empty()
    with zone_options:
        st.empty()