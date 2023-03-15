import streamlit as st
import folium, logging
from streamlit_folium import st_folium
from streamlit_uploads_library.uploads import UploadFiles
import tiles, utils

logger = logging.getLogger(__name__)

class CreateMap():
    def __init__(self):
        self.init_state()
        self.create_sidebar()

        if self.save_btn:
            if "map_name" in st.session_state and len(st.session_state["map_name"]) > 0:
                self.m.save(f"{utils.tiles_folder}/{st.session_state['base_layer']}/{st.session_state['map_name']}.html")
            else:
                with self.save_download_btn_warning_msg:
                    st.error("Please provide a name for the map in the 'Map Options' section and click apply before saving again.")

        if self.map_options_btn:
            if len(self.map_options_map_name) > 0:
                with self.map_options_name_warning_msg:
                    st.empty()
                st.session_state["map_name"] = self.map_options_map_name
                st.session_state["base_layer"] = self.base_layer
                st.session_state["map_options_min_zoom"] = self.map_options_min_zoom
                st.session_state["map_options_max_zoom"] = self.map_options_max_zoom
            else:
                with self.map_options_name_warning_msg:
                    st.error("Please provide a name for the map and click apply.")

        if self.layer_options_add_btn:
            # Do something
            pass
        if self.layer_options_edit_btn:
            # Do something
            pass
        if self.layer_options_remove_btn:
            # Do something
            pass
        if self.marker_options_add_btn:
            # Do something
            pass
        if self.marker_options_edit_btn:
            # Do something
            pass
        if self.marker_options_remove_btn:
            # Do something
            pass
        if self.zone_options_add_btn:
            # Do something
            pass
        if self.zone_options_edit_btn:
            # Do something
            pass
        if self.zone_options_remove_btn:
            # Do something
            pass

        # Main page that displays the map
        self.m = folium.Map(location=(-75, 0), tiles=None, width="100%", height="100%", zoom_start=3, max_bounds=True)
        if self.base_layer:
            self.base_tile_layer = folium.TileLayer(tiles=f"http://127.0.0.1:8888/{self.base_layer}/{{z}}/{{x}}/{{-y}}.png", name=st.session_state["map_name"], min_zoom=st.session_state["map_options_min_zoom"], max_zoom=st.session_state["map_options_max_zoom"], attr="@hreikin").add_to(self.m)
            self.markers_fg = folium.FeatureGroup(name="Markers")
            self.markers_fg.add_to(self.m)
            self.zones_fg = folium.FeatureGroup(name="Zones")
            self.zones_fg.add_to(self.m)
            # Needs to be added last
            self.layer_control = folium.LayerControl().add_to(self.m)
            self.map_data = st_folium(self.m, width=1175)
            logger.info(f"MAP DATA: {self.map_data}")
            if self.map_data["last_clicked"] == None:
                st.session_state["last_clicked"] = {'lat': 0, 'lng': 0}
            else:
                st.session_state["last_clicked"] = self.map_data["last_clicked"]
        else:
            st.warning("You haven't selected a base layer, please configure the map using the 'Map Options' section in the sidebar.")

    def init_state(self):
        if "create_mode" not in st.session_state or st.session_state["create_mode"] == False:
            st.session_state["create_mode"] = True
            # Map options
            st.session_state["map_name"] = ""
            self.library_tiles = list()
            for item in utils.tiles_folder.iterdir():
                if item.is_dir():
                    self.library_tiles.append(item.name)
            st.session_state["library_tiles"] = self.library_tiles
            st.session_state["map_options_min_zoom"] = 0
            st.session_state["map_options_max_zoom"] = 19
            # Marker options
            self.library_icons = list()
            for icon in utils.icons_folder.iterdir():
                self.library_icons.append(icon.stem)
            st.session_state["library_icons"] = self.library_icons
            st.session_state["last_clicked"] = {'lat': 0, 'lng': 0}
            # Markers list or use FeatureGroup for removing markers ? This just allows the selector in the 
            # "Remove" markers tab to load at present.
            self.layers_list = list()
            st.session_state["layers_list"] = self.layers_list
            self.markers_list = list()
            st.session_state["markers_list"] = self.markers_list
            self.zones_list = list()
            st.session_state["zones_list"] = self.zones_list

    def create_sidebar(self):
        # General sidebar layout
        with st.sidebar:
            self.sidebar_sub_1, self.sidebar_sub_2 = st.columns(2)
            self.save_download_btn_warning_msg = st.empty()
            with st.expander(label="Step 1 (optional):"):
                self.upload_images = UploadFiles(save_location="library/images/", header="Images", info_msg="Upload images to create tiles from here.", uid="images", upload_label="Upload Images")
                self.upload_icons = UploadFiles(save_location="library/icons/", header="Icons", info_msg="Upload custom icons to use on your map here.", uid="icons", upload_label="Upload Icons")
            self.create_tiles = tiles.CreateTiles(label="Step 2 (optional):", expanded=False)
            self.create_map_options = st.expander(label="Step 3 (required):", expanded=True)
        # Save & Download buttons
        with self.sidebar_sub_1:
            self.save_btn = st.button("Save Map", type="primary", use_container_width=True)
        with self.sidebar_sub_2:
            self.download_btn = st.button("Download Map", type="secondary", use_container_width=True)
        # Map options layout
        with self.create_map_options:
            self.create_map_options_msg = st.info("Create your map by defining the options available below, the map will update to reflect your changes.")
            self.map_options_form = st.form(key="Map Options")
            self.layer_options_form = st.form(key="Layers")
            self.marker_options_form = st.form(key="Markers")
            self.zone_options_form = st.form(key="Zones")
        # Map options form
        with self.map_options_form:
            self.map_options_subheader = st.subheader("Map Options")
            self.map_options_info_msg = st.info("Configure your maps default values.")
            self.map_options_name_warning_msg = st.empty()
            self.map_options_map_name = st.text_input(label="Map Name", placeholder="Select a name for your map.", help="Select a name for your map, this will also be the base layers name in the layers control on the map.")
            self.base_layer = st.selectbox(label="Base Layer", options=st.session_state["library_tiles"], help="Choose tiles from the library to use as the base layer.")
            self.map_options_min_zoom = st.selectbox(label="Min Zoom", options=range(1,21), index=st.session_state["map_options_min_zoom"], help="Select minimum zoom for the map. This should be the same as the 'Min Zoom' setting used when creating the tiles or higher.")
            self.map_options_max_zoom = st.selectbox(label="Max Zoom", options=range(1,21), index=st.session_state["map_options_max_zoom"], help="Select maximum zoom for the map. This should be the same as the 'Max Zoom' setting used when creating the tiles or lower.")
            self.map_options_btn = st.form_submit_button(label="Apply", type="primary", use_container_width=True)
        # Layer options form
        with self.layer_options_form:
            self.layer_options_subheader = st.subheader("Layers")
            self.layer_options_info_msg = st.info("Select the current active layer to add all markers and zones too.")
            self.layer_options_current_layer = st.selectbox(label="Current Acive Layer", options=st.session_state["layers_list"], help="Select the current active layer to add all markers and zones too.")
            self.layer_options_add_tab, self.layer_options_edit_tab, self.layer_options_remove_tab = st.tabs(["Add", "Edit", "Remove"])
        # Add tab
        with self.layer_options_add_tab:
            self.layer_options_add_info_msg = st.info("Give your new layer a name and define its position in the layers controller.")
            self.layer_options_add_layer_name = st.text_input(label="New Layer Name", key="add-layer-name", placeholder="Select a name for your layer.", help="Select a name for your layer, this will also be the layers name in the layers control on the map.")
            self.layer_options_add_position = st.number_input(label="Position", key="add-layer-position", min_value=1)
            self.layer_options_add_btn = st.form_submit_button(label="Add", type="primary", use_container_width=True)
        # Edit tab
        with self.layer_options_edit_tab:
            self.layer_options_edit_info_msg = st.info("Edit the selected layers name and position in the layers controller.")
            self.layer_options_edit_selected_layer = st.selectbox(label="Layer To Edit", options=st.session_state["layers_list"], help="Select the layer you wish to edit.")
            self.layer_options_edit_layer_name = st.text_input(label="Layer Name", key="edit-layer-name", placeholder="Select a name for the layer.", help="Select a name for your layer, this will also be the layers name in the layers control on the map.")
            self.layer_options_edit_layer_position = st.number_input(label="Position", key="edit-layer-position", min_value=1)
            self.layer_options_edit_btn = st.form_submit_button(label="Update", type="primary", use_container_width=True)
        # Remove tab
        with self.layer_options_remove_tab:
            self.layer_options_remove_warning_msg = st.warning("Choose a layer to delete from the map. This can not be undone.")
            self.layer_options_remove_selected_layer = st.selectbox(label="Layer To Remove", options=st.session_state["layers_list"], help="Select the layer you wish to delete from the map, this will also delete all markers and zones associated with it.")
            self.layer_options_remove_btn = st.form_submit_button(label="Delete", use_container_width=True)
        # Marker options form
        with self.marker_options_form:
            self.marker_options_subheader = st.subheader("Markers")
            self.marker_options_add_tab, self.marker_options_edit_tab, self.marker_options_remove_tab = st.tabs(["Add", "Edit", "Remove"])
        # Add tab
        with self.marker_options_add_tab:
            self.marker_options_add_info_msg = st.info("Give your new marker a name and define its position and icon to be used.")
            self.marker_options_add_name = st.text_input(label="Name (ID)", key="add-marker-name", placeholder="Choose a name for the marker.", help="Choose a name for the marker to be used as its ID. This will not be displayed on the map.")
            self.marker_options_add_icon = st.selectbox(label="Icon", key="add-marker-icon", options=st.session_state["library_icons"], help="Choose icons from the library to use with your marker.")
            self.marker_options_add_tab_lcol, self.marker_options_add_tab_rcol = st.columns(2)
            self.marker_options_add_popup_text = st.text_area(label="Popup Content", key="add-marker-popup", placeholder="Create some content for your popup, supports Markdown so you can add headers, images, links, etc.", help="The text that will be displayed when the user clicks the marker and the popup shows. Leave empty to dsable the popup.")
            self.marker_options_add_tooltip_text = st.text_area(label="Tooltip Content", key="add-marker-tooltip", placeholder="Create some content for your tooltip, supports Markdown so you can add headers, images, links, etc.", help="The text that will be displayed when the user hovers over the marker and the tooltip shows. Leave empty to disable the tooltip.")
            self.marker_options_add_btn = st.form_submit_button(label="Add", type="primary", use_container_width=True)
        with self.marker_options_add_tab_lcol:
            self.marker_options_add_lat = st.number_input(label="Lat", key="add-marker-lat", value=st.session_state["last_clicked"]["lat"], help="Latitude of the marker.")
            self.marker_options_add_width = st.number_input(label="Width", key="add-marker-width", min_value=0, value=30, help="Width of the marker in pixels.")
        with self.marker_options_add_tab_rcol:
            self.marker_options_add_lng = st.number_input(label="Lng", key="add-marker-lng", value=st.session_state["last_clicked"]["lng"], help="Longitude of the marker.")
            self.marker_options_add_height = st.number_input(label="Height", key="add-marker-height", min_value=0, value=30, help="Height of the marker in pixels.")
        # Edit tab
        with self.marker_options_edit_tab:
            self.marker_options_edit_info_msg = st.info("Edit the selected markers details.")
            self.marker_options_edit_selected_marker = st.selectbox(label="Marker To Edit", options=st.session_state["markers_list"], help="Choose a marker from the map to edit its details.")
            self.marker_options_edit_name = st.text_input(label="Name (ID)", key="edit-marker-name", placeholder="Choose a name for the marker.", help="Choose a name for the marker to be used as its ID. This will not be displayed on the map.")
            self.marker_options_edit_icon = st.selectbox(label="Icon", key="edit-marker-icon", options=st.session_state["library_icons"], help="Choose icons from the library to use with your marker.")
            self.marker_options_edit_tab_lcol, self.marker_options_edit_tab_rcol = st.columns(2)
            self.marker_options_edit_popup_text = st.text_area(label="Popup Content", key="edit-marker-popup", placeholder="Create some content for your popup, supports Markdown so you can add headers, images, links, etc.", help="The text that will be displayed when the user clicks the marker and the popup shows. Leave empty to dsable the popup.")
            self.marker_options_edit_tooltip_text = st.text_area(label="Tooltip Content", key="edit-marker-tooltip", placeholder="Create some content for your tooltip, supports Markdown so you can add headers, images, links, etc.", help="The text that will be displayed when the user hovers over the marker and the tooltip shows. Leave empty to disable the tooltip.")
            self.marker_options_edit_btn = st.form_submit_button(label="Update", type="primary", use_container_width=True)
        with self.marker_options_edit_tab_lcol:
            self.marker_options_edit_lat = st.number_input(label="Lat", key="edit-marker-lat", value=st.session_state["last_clicked"]["lat"], help="Latitude of the marker.")
            self.marker_options_edit_width = st.number_input(label="Width", key="edit-marker-width", min_value=0, value=30, help="Width of the marker in pixels.")
        with self.marker_options_edit_tab_rcol:
            self.marker_options_edit_lng = st.number_input(label="Lng", key="edit-marker-lng", value=st.session_state["last_clicked"]["lng"], help="Longitude of the marker.")
            self.marker_options_edit_height = st.number_input(label="Height", key="edit-marker-height", min_value=0, value=30, help="Height of the marker in pixels.")
        # Remove tab
        with self.marker_options_remove_tab:
            self.marker_options_remove_warning_msg = st.warning("Choose a marker to delete from the map. This can not be undone.")
            self.marker_options_remove_selected_marker = st.selectbox(label="Marker To Remove", options=st.session_state["markers_list"], help="Choose a marker to delete from the map. This can not be undone.")
            self.marker_options_remove_btn = st.form_submit_button(label="Remove", type="secondary", use_container_width=True)
        # Zone options form
        with self.zone_options_form:
            self.zone_options_subheader = st.subheader("Zones")
            self.zone_options_add_tab, self.zone_options_edit_tab, self.zone_options_remove_tab = st.tabs(["Add", "Edit", "Remove"])
        # Add tab
        with self.zone_options_add_tab:
            self.zone_options_add_info_msg = st.info("Give your new zone a name and define its position and colour to be used.")
            self.zone_options_add_btn = st.form_submit_button(label="Add", type="primary", use_container_width=True)
        # Edit tab
        with self.zone_options_edit_tab:
            self.zone_options_edit_info_msg = st.info("Edit the selected zones details.")
            self.zone_options_edit_selected_zone = st.selectbox(label="Zone To Edit", options=st.session_state["zones_list"], help="Choose a zone from the map to edit its details.")
            self.zone_options_edit_btn = st.form_submit_button(label="Update", type="primary", use_container_width=True)
        # Remove tab
        with self.zone_options_remove_tab:
            self.zone_options_remove_warning_msg = st.warning("Choose a zone to delete from the map. This can not be undone.")
            self.zone_options_remove_selected_zone = st.selectbox(label="Zone To Remove", options=st.session_state["zones_list"], help="Choose a zone to delete from the map. This can not be undone.")
            self.zone_options_remove_btn = st.form_submit_button(label="Remove", use_container_width=True)

class EditMap():
    pass