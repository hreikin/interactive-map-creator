import streamlit as st

def app():

    if st.session_state["authentication_status"]:
        st.header(f"Welcome *{st.session_state['name']}*.")
        st.markdown(
            """
            Interactive Map Creator makes it easy for anyone to create interactive maps.
            """
            )