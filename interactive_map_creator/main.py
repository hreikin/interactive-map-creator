import streamlit as st
import threading
from streamlit_option_menu import option_menu
import utils
from apps import create, docs, home, library

# Configure page title, layout, menu items and links.
st.set_page_config(
    page_title="Interactive Map Creator",
    layout="wide",
    menu_items={
        "Get Help": "https://github.com/hreikin/interactive-map-creator",
        "Report a bug": "https://github.com/hreikin/interactive-map-creator/issues",
        "About": """
        Interactive Map Creator is created and maintained by [Michael Haslam](https://hreikin.co.uk). The source code is available on [GitHub](https://github.com/hreikin/interactive-map-creator), community contributions are always welcome.
        
        GNU Affero General Public License v3.0 or later: [AGPL v3.0](https://www.gnu.org/licenses/agpl-3.0.en.html)
        """
    },
    )    
if utils.server_started is None:
    thread = threading.Thread(target=utils.create_server, args=[utils.server_started]).start()
    server_started = True
else:
    server_started = False
if server_started == True:
    utils.server_started = True

# A dictionary of apps in the format of {"func": foo, "title": "foo", "icon": "bootstrap-icon-name"}
# More icons can be found here: https://icons.getbootstrap.com
apps = [
    {"func": home.app, "title": "Home", "icon": "house"},
    {"func": create.app, "title": "Create New", "icon": "file-earmark-plus"},
    {"func": library.app, "title": "Library", "icon": "collection"},
    {"func": docs.app, "title": "Help", "icon": "question-circle"},
]

titles = [app["title"] for app in apps]
titles_lower = [title.lower() for title in titles]
icons = [app["icon"] for app in apps]

params = st.experimental_get_query_params()

if "page" in params:
    default_index = int(titles_lower.index(params["page"][0].lower()))
else:
    default_index = 0

selected = option_menu(
    "Interactive Map Creator",
    options=titles,
    icons=icons,
    menu_icon="map",
    default_index=default_index,
    orientation="horizontal"
)

# When the user makes a menu selection run the relevant app.
for app in apps:
    if app["title"] == selected:
        app["func"]()
        break