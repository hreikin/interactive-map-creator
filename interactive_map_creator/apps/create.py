import streamlit as st
import logging
import folium
from pathlib import Path
from streamlit_folium import st_folium
import libs.gdal2tiles.gdal2tiles as gd2
import utils

logger = logging.getLogger(__name__)

def init_create_mode():
    if "create_mode" not in st.session_state or st.session_state["create_mode"] == False:
        st.session_state["create_mode"] = True
        # Tile creation
        library_files = list()
        for item in utils.library_folder.iterdir():
            if item.is_file():
                library_files.append(item.name)
        st.session_state["library_files"] = library_files
        st.session_state["create_tiles_min_zoom"] = 0
        st.session_state["create_tiles_max_zoom"] = 19
        st.session_state["number_of_processes"] = 7
        # Map options
        library_tiles = list()
        for item in utils.tiles_folder.iterdir():
            if item.is_dir():
                library_tiles.append(item.name)
        st.session_state["library_tiles"] = library_tiles
        st.session_state["map_options_min_zoom"] = 0
        st.session_state["map_options_max_zoom"] = 19
        # Marker options
        library_icons = list()
        for icon in utils.icons_folder.iterdir():
            library_icons.append(icon.stem)
        st.session_state["library_icons"] = library_icons
        st.session_state["last_clicked"] = {'lat': 0, 'lng': 0}
        # Markers list or use FeatureGroup for removing markers ? This just allows the selector in the 
        # "Remove" markers tab to load at present.
        markers_list = list()
        st.session_state["markers_list"] = markers_list


# Needs to be used on the Library page also, move to `tiles.py` file ? 
def process_into_tiles(src_img, min_zoom, max_zoom, number_of_processes):
    tiles_folder = Path(utils.tiles_folder/src_img.stem)
    tiles_folder.resolve().mkdir(parents=True, exist_ok=True)
    if max_zoom <= min_zoom:
        gdal_zoom = min_zoom
    else:
        gdal_zoom = [min_zoom, max_zoom]
    gdal_options = {
        "profile": "raster",
        "zoom": gdal_zoom,
        "nb_processes": number_of_processes,
        "tile_size": 256,
    }
    for item in utils.library_folder.iterdir():
        if str(item.name) == str(src_img.name):
            gd2.generate_tiles(str(src_img), tiles_folder, **gdal_options)
    return  # Return the tiles or path for the map ?

def app():
    # Initialize create mode with default values in session state
    init_create_mode()

    # Basic layout of sidebar
    with st.sidebar:
        sidebar_sub_1, sidebar_sub_2 = st.columns(2)
        save_download_btn_warning_msg = st.empty()
        upload_options = st.expander(label="Step 1 (optional):")
        create_tiles_options = st.expander(label="Step 2 (optional):")
        create_map_options = st.expander(label="Step 3 (required):")

    # Save & Download buttons
    with sidebar_sub_1:
        save_btn = st.button("Save Map", type="primary", use_container_width=True)
    with sidebar_sub_2:
        download_btn = st.button("Download Map", type="secondary", use_container_width=True)

    # Step 1 - upload files and/or icons
    with upload_options:
        upload_options_msg = st.info("Upload files here to use as the base for tile creation or marker icons. If you want to use a previously uploaded file then it is safe to skip this step.")
        uploaded_file = st.file_uploader("Upload Base Image File", type=["png", "jpg", "jpeg"], help="Upload a new image to create map tiles from.")
        uploaded_icon = st.file_uploader("Upload Icon", type=["png", "jpg", "jpeg", "ico"], help="Upload a new icon.")
    if uploaded_file is not None:
        utils.save_uploaded_file(uploaded_file, utils.library_folder)
    if uploaded_icon is not None:
        utils.save_uploaded_file(uploaded_icon, utils.icons_folder)

    # Step 2 - create tiles from uploaded files
    with create_tiles_options:
        create_tiles_options_msg = st.info("Create tiles from a previously uploaded image using the options available below. If you want to re-use some previously created tiles then it is safe to skip this step.")
        create_tiles_form = st.form(key="create_tiles_form")
    with create_tiles_form:
        image_file = st.selectbox(label="Image File", options=st.session_state["library_files"], help="Choose an image from the library to use as the map tile source. To upload a new image use the uploader in the sidebar and then select it from this menu.")
        create_tiles_min_zoom = st.selectbox(label="Min Zoom", options=range(1,21), index=st.session_state["create_tiles_min_zoom"], help="Select minimum zoom for tile generation.")
        create_tiles_max_zoom = st.selectbox(label="Max Zoom", options=range(1,21), index=st.session_state["create_tiles_max_zoom"], help="Select maximum zoom for tile generation.")
        number_of_processes = st.selectbox(label="Number Of Processes", options=range(1,17), index=st.session_state["number_of_processes"], help="Select number of processes to use to generate tiles.")
        create_tiles_warning_msg = st.empty()
        create_tiles_spinner = st.empty()
        create_tiles_btn = st.form_submit_button(label="Create Tiles", type="primary", use_container_width=True)
    if create_tiles_btn:
        with create_tiles_warning_msg:
            st.warning("This process may take a long time, do not refresh the page or navigate away from it.")
        with create_tiles_spinner:
            with st.spinner("Creating tiles..."):
                src_img = Path(utils.library_folder/str(image_file)).resolve()
                process_into_tiles(src_img, create_tiles_min_zoom, create_tiles_max_zoom, number_of_processes)
        with create_tiles_warning_msg:
            st.empty()

    # Step 3 - create map from options
    with create_map_options:
        create_map_options_msg = st.info("Create your map by defining the options available below, the map will update to reflect your changes.")
        map_options_form = st.form(key="Map Options")
        marker_options_form = st.form(key="Marker Options")
        zone_options_form = st.form(key="Zone Options")

    with map_options_form:
        map_options_subheader = st.subheader("Map Options")
        map_name_warning_msg = st.empty()
        map_name = st.text_input(label="Map Name", placeholder="Select a name for your map", help="Select a name for your map, this will also be the base layers name in the layers control on the map.")
        base_layer = st.selectbox(label="Base Layer", options=st.session_state["library_tiles"], help="Choose tiles from the library to use as the base layer.")
        map_options_min_zoom = st.selectbox(label="Min Zoom", options=range(1,21), index=st.session_state["map_options_min_zoom"], help="Select minimum zoom for the map. This should be the same as the 'Min Zoom' setting used when creating the tiles or higher.")
        map_options_max_zoom = st.selectbox(label="Max Zoom", options=range(1,21), index=st.session_state["map_options_max_zoom"], help="Select maximum zoom for the map. This should be the same as the 'Max Zoom' setting used when creating the tiles or lower.")
        map_options_btn = st.form_submit_button(label="Apply", type="primary", use_container_width=True)
    
    if map_options_btn:
        if len(map_name) > 0:
            with map_name_warning_msg:
                st.empty()
            st.session_state["map_name"] = map_name
            st.session_state["base_layer"] = base_layer
            st.session_state["map_options_min_zoom"] = map_options_min_zoom
            st.session_state["map_options_max_zoom"] = map_options_max_zoom
        else:
            with map_name_warning_msg:
                st.error("Please provide a name for the map and click apply.")

    with marker_options_form:
        marker_options_subheader = st.subheader("Marker Options")
        marker_options_add_tab, marker_options_remove_tab = st.tabs(["Add", "Remove"])
    with marker_options_add_tab:
        marker_name = st.text_input(label="Name (ID)", placeholder="Choose a name for the marker", help="Choose a name for the marker to be used as its ID. This will not be displayed on the map.")
        marker_icon = st.selectbox(label="Icon", options=st.session_state["library_icons"], help="Choose icons from the library to use with your marker.")
        marker_options_add_tab_lcol, marker_options_remove_tab_rcol = st.columns(2)
        marker_popup_text = st.text_input(label="Popup Content", placeholder="Create some content for your popup", help="The text that will be displayed when the user clicks the marker and the popup shows. Leave empty to dsable the popup.")
        marker_tooltip_text = st.text_input(label="Tooltip Content", placeholder="Create some content for your tooltip", help="The text that will be displayed when the user hovers over the marker and the tooltip shows. Leave empty to disable the tooltip.")
        marker_options_add_btn = st.form_submit_button(label="Add", type="primary", use_container_width=True)
    with marker_options_add_tab_lcol:
        marker_lat = st.number_input(label="Lat", value=st.session_state["last_clicked"]["lat"], help="Latitude of the marker.")
        marker_width = st.number_input(label="Width", min_value=0, value=30, help="Width of the marker in pixels.")
    with marker_options_remove_tab_rcol:
        marker_lng = st.number_input(label="Lng", value=st.session_state["last_clicked"]["lng"], help="Longitude of the marker.")
        marker_height = st.number_input(label="Height", min_value=0, value=30, help="Height of the marker in pixels.")
    with marker_options_remove_tab:
        marker_options_remove_warning_msg = st.warning("Choose a marker to delete from the map. This can not be undone.")
        remove_marker = st.selectbox(label="Marker To Remove", options=st.session_state["markers_list"], help="Choose a marker to delete from the map. This can not be undone.")
        marker_options_remove_btn = st.form_submit_button(label="Remove", type="secondary", use_container_width=True)

    if marker_options_add_btn:
        # Do something
        pass

    with zone_options_form:
        zone_options_subheader = st.subheader("Zone Options")
        zone_options_btn = st.form_submit_button(label="Add", type="primary", use_container_width=True)

    # Main page that displays the map
    m = folium.Map(location=(-75, 0), tiles=None, width="100%", height="100%", zoom_start=3, max_bounds=True)
    if base_layer:
        folium.TileLayer(tiles=f"http://127.0.0.1:8888/{base_layer}/{{z}}/{{x}}/{{-y}}.png", name=map_name, min_zoom=map_options_min_zoom, max_zoom=map_options_max_zoom, attr="@hreikin").add_to(m)

        markers_fg = folium.FeatureGroup(name="Markers")
        markers_fg.add_to(m)
        zones_fg = folium.FeatureGroup(name="Zones")
        zones_fg.add_to(m)
        # Needs to be added last
        folium.LayerControl().add_to(m)
        map_data = st_folium(m, width=1175)
        logger.info(f"MAP DATA: {map_data}")
        if map_data["last_clicked"] == None:
            st.session_state["last_clicked"] = {'lat': 0, 'lng': 0}
        else:
            st.session_state["last_clicked"] = map_data["last_clicked"]
    else:
        st.warning("You haven't selected a base layer, please configure the map using the 'Map Options' section in the sidebar.")

    if save_btn:
        if "map_name" in st.session_state:
            m.save(f"{utils.tiles_folder}/{st.session_state['base_layer']}/{st.session_state['map_name']}.html")
        else:
            with save_download_btn_warning_msg:
                st.error("Please provide a name for the map in the 'Map Options' section and click apply before saving again.")