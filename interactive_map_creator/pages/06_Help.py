import streamlit as st


import imc

st.set_page_config(
    page_title="Help - Interactive Map Creator",
    menu_items={
    "Get Help": f"{imc.GIT_URL}/wiki",
    "Report a bug": f"{imc.GIT_URL}/issues",
    "About": f"{imc.ABOUT_STR}"
    },
)

st.title("Help & Documentation")