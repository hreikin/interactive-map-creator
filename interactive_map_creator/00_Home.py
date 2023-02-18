import streamlit as st


import imc

st.set_page_config(
    page_title="Home - Interactive Map Creator",
    menu_items={
    "Get Help": f"{imc.GIT_URL}/wiki",
    "Report a bug": f"{imc.GIT_URL}/issues",
    "About": f"{imc.ABOUT_STR}"
    },
)

st.title("Home")

st.markdown("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")