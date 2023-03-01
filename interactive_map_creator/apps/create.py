import streamlit as st
import logging
import folium
from streamlit_folium import st_folium
import utils

logger = logging.getLogger(__name__)

def app():
    with st.sidebar:
        sidebar_sub_1, sidebar_sub_2 = st.columns(2)
        step_1_title = st.subheader("Step 1 (optional):")
        upload_options = st.expander(label="Upload Files")
        step_2_title = st.subheader("Step 2 (optional):")
        create_tiles_options = st.expander(label="Create Tiles")
        step_3_title = st.subheader("Step 3 (required):")
        step_3_msg = st.info("Create your map by defining the options available below, the map will update to reflect your changes.")
        map_options = st.expander(label="Map Options")
        marker_options = st.expander(label="Marker Options")
        zone_options = st.expander(label="Zone Options")
    with upload_options:
        step_1_msg = st.info("Upload files here to use as the base for tile creation or marker icons. If you want to use a previously uploaded file then it is safe to skip this step.")
        uploaded_file = st.file_uploader("Upload Base Image File", type=["png", "jpg", "jpeg"], help="Upload a new image to create map tiles from.")
        uploaded_icon = st.file_uploader("Upload Icon", type=["png", "jpg", "jpeg", "ico"], help="Upload a new icon.")
        if uploaded_file is not None:
            utils.save_uploaded_file(uploaded_file, utils.uploads_folder)
    with create_tiles_options:
        step_2_msg = st.info("Create tiles from a previously uploaded image using the options available below. If you want to re-use some previously created tiles then it is safe to skip this step.")
        library_files = list()
        for item in utils.uploads_folder.iterdir():
            if item.is_file():
                library_files.append(item.name)
        image_file = st.selectbox(label="Image File", options=library_files, help="Choose an image from the library to use as the map tile source. To upload a new image use the uploader in the sidebar and then select it from this menu.")
        min_zoom = st.selectbox(label="Min Zoom", options=[1,2,3,4,5,6,7,8,9,10], index=2, help="Select minimum zoom for tile generation.")
        max_zoom = st.selectbox(label="Max Zoom", options=[1,2,3,4,5,6,7,8,9,10], index=6, help="Select maximum zoom for tile generation.")
        tile_size = st.selectbox(label="Tile Size", options=[128,256,512], index=1, help="Select size of tiles for tile generation.")
        number_of_processes = st.selectbox(label="Number Of Processes", options=range(1,17), index=3, help="Select number of processes to use to generate tiles.")
        create_tiles_warnig_msg = st.warning("This process may take a long time, do not refresh the page or navigate away from it.")
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
            logger.info("No file selected:", e)
    with sidebar_sub_1:
        save_btn = st.button("Save Map", type="primary", use_container_width=True)
    with sidebar_sub_2:
        download_btn = st.button("Download Map", type="secondary", use_container_width=True)

    with map_options:
        map_name = st.text_input(label="Map Name", placeholder="Select a name for your map", help="Select a name for your map, this will also be the base layers name in the layers control on the map.")
        library_tiles = list()
        for item in utils.tiles_folder.iterdir():
            if item.is_dir():
                library_tiles.append(item.name)
        base_layer = st.selectbox(label="Base Layer", options=library_tiles, help="Choose tiles from the library to use as the map tile source for the base layer. To create new tiles use the tile creation options available in the sidebar and then select them here.")

    with marker_options:
        create_marker_tab, delete_marker_tab = st.tabs(["Create Marker", "Delete Marker"])
    with create_marker_tab:
        icons_list = list()
        for icon in utils.icons_folder.iterdir():
            icons_list.append(icon.stem)
        marker_name = st.text_input(label="Name (ID)", placeholder="Choose a name for the marker", help="Choose a name for the marker to be used as its ID. This will not be displayed on the map.")
        marker_icon = st.selectbox(label="Icon", options=icons_list, help="Choose icons from the library to use with your marker.")
        marker_options_sub_1, marker_options_sub_2 = st.columns(2)
    with marker_options_sub_1:
        marker_lat = st.number_input(label="Lat", value=0.00000000000000, help="Latitude of the marker.")
        marker_width = st.number_input(label="Width", value=0, help="Width of the marker.")
        marker_popup_checkbox = st.checkbox(label="Add Popup", value=True)
    with marker_options_sub_2:
        marker_lng = st.number_input(label="Lng", value=0.00000000000000, help="Longitude of the marker.")
        marker_height = st.number_input(label="Height", value=0, help="Height of the marker.")
        marker_tooltip_checkbox = st.checkbox(label="Add Tooltip", value=True)
    with create_marker_tab:
        if marker_popup_checkbox:
            marker_popup_text = st.text_input(label="Popup Content", placeholder="Create some content for your popup", help="The text that will be displayed when the user clicks the marker and the popup shows.")
        else:
            marker_popup_text = st.empty()
        if marker_tooltip_checkbox:
            marker_tooltip_text = st.text_input(label="Tooltip Content", placeholder="Create some content for your tooltip", help="The text that will be displayed when the user hovers over the marker and the tooltip shows.")
        else:
            marker_tooltip_text = st.empty()
        add_marker_btn = st.button(label="Add Marker", type="primary", use_container_width=True)
    with delete_marker_tab:
        del_warning_message = st.warning("This will permanently delete the selected marker from the map with no way of recovering it.")
        del_marker_selection = st.selectbox(label="Marker To Delete", options=" example", help="Choose the marker you wish to delete, this will permanently remove it from the map.")
        del_marker_btn = st.button(label="Remove Marker", type="secondary", use_container_width=True)
    with zone_options:
        st.empty()

    if base_layer:
        m = folium.Map(location=(-75, 0), tiles=None, width="100%", height="100%", zoom_start=3, max_bounds=True)
        folium.TileLayer(tiles=f"http://127.0.0.1:8888/{base_layer}/{{z}}/{{x}}/{{-y}}.png", name=map_name, min_zoom=min_zoom, max_zoom=max_zoom, attr="@hreikin").add_to(m)

        # Markers feature group.
        markers_fg = folium.FeatureGroup("Markers")
        markers_fg.add_to(m)
        # Zones feature group.
        zones_fg = folium.FeatureGroup("Zones")
        zones_fg.add_to(m)
        # Needs to be added last.
        folium.LayerControl().add_to(m)

        map_data = st_folium(m, width=1175)
        logger.info(map_data)

        if save_btn:
            m.save(f"{utils.tiles_folder}/{base_layer}/map.html")