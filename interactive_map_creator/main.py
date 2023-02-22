import streamlit as st
from streamlit_option_menu import option_menu

from apps import home, create, library, settings

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

# A dictionary of apps in the format of {"func": foo, "title": "foo", "icon": "bootstrap-icon-name"}
# More icons can be found here: https://icons.getbootstrap.com
apps = [
    {"func": home.app, "title": "Home", "icon": "house"},
    {"func": create.app, "title": "Create", "icon": "file-earmark-plus"},
    {"func": library.app, "title": "Library", "icon": "collection"},
    {"func": settings.app, "title": "Settings", "icon": "gear"},
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