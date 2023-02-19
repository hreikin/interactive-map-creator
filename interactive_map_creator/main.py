import streamlit as st
from streamlit_option_menu import option_menu
import streamlit_authenticator as st_auth
from apps import home, create, library, settings

st.set_page_config(page_title="Interactive Map Creator", layout="wide")

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

with open('config.yaml') as file:
    config = st_auth.yaml.load(file, Loader=st_auth.SafeLoader)

authenticator = st_auth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login('Login', 'sidebar')

selected = option_menu(
    "Interactive Map Creator",
    options=titles,
    icons=icons,
    menu_icon="map",
    default_index=default_index,
    orientation="horizontal",
)

if st.session_state["authentication_status"] == None:
        st.info('Please login using the sidebar.')
        st.write("Content to show un-authenticated users.")

with st.sidebar:
    
    if st.session_state["authentication_status"]:
        st.write(f"Welcome *{st.session_state['name']}*")
        authenticator.logout("Logout", "sidebar")
    elif st.session_state["authentication_status"] == False:
        st.error("Username/password is incorrect.")

    st.sidebar.info(
        """
        # About

        Interactive Map Creator is created and maintained by [Michael Haslam](https://hreikin.co.uk). You can find me on [GitHub](https://github.com/hreikin).
        
        Source code is available [here](https://github.com/hreikin/interactive-map-creator), community contributions are welcome.
        
        GNU Affero General Public License v3.0 or later: [AGPL v3.0](https://www.gnu.org/licenses/agpl-3.0.en.html)
        """
    )

for app in apps:
    if app["title"] == selected:
        app["func"]()
        break