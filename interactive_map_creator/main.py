import streamlit as st
from streamlit_option_menu import option_menu
import streamlit_authenticator as st_auth
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

# Load streamlit-authenticator config file and instantiate authenticator.
with open(".streamlit/config.yaml") as file:
    config = st_auth.yaml.load(file, Loader=st_auth.SafeLoader)

authenticator = st_auth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
    config["preauthorized"]
)

# Show login form if user isn't logged in.
if st.session_state["authentication_status"] == None:
    name, authentication_status, username = authenticator.login("Login", "main")
    
# Show error message if authentication fails and reset authentication_status to
# none to avoid issues with forms disappearing after the user tries to log in.
if st.session_state["authentication_status"] == False:
    st.error("Username/password is incorrect.")
    st.session_state["authentication_status"] = None

# Forgotten ussername and password forms.
if st.session_state["authentication_status"] == None:
    st.info("If you have forgotten your username or password, then please use one of the forms below.")
    col_1, col_2 = st.columns(2)
    with col_1:
        username_forgot_username, email_forgot_username = authenticator.forgot_username("Forgotten Username ?")
        try:
            if username_forgot_username:
                st.success("Username sent securely.")
                # Username to be transferred to user securely
            elif username_forgot_username == False:
                st.error("Email not found.")
        except Exception as e:
            st.error(e)
    with col_2:
        username_forgot_pw, email_forgot_password, random_password = authenticator.forgot_password("Forgotten Password ?")
        try:
            if username_forgot_pw:
                st.success("New password sent securely.")
                # Random password to be transferred to user securely
            elif username_forgot_pw == False:
                st.error("Username not found.")
        except Exception as e:
            st.error(e)

# Registration form.
if st.session_state["authentication_status"] == None:
    st.warning("If you would like to register for an account then please use the form below.")
    try:
        if authenticator.register_user("New User Registration", preauthorization=True):
            st.success("User registered successfully.")
    except Exception as e:
        st.error(e)

with st.sidebar:
    # Sidebar menu from streamlit-option-menu
    selected = option_menu(
        "Interactive Map Creator",
        options=titles,
        icons=icons,
        menu_icon="map",
        default_index=default_index,
    )
    col_1_sidebar, col_2_sidebar = st.columns(2)

# If user is logged in then display a message and button to logout.
with col_1_sidebar:
    if st.session_state["authentication_status"]:
        authenticator.logout("Logout", "main")
with col_2_sidebar:
    if st.session_state["authentication_status"]:
        st.write(f"Welcome *{st.session_state['name']}*")

# When the user makes a menu selection run the relevant app.
for app in apps:
    if app["title"] == selected:
        app["func"]()
        break