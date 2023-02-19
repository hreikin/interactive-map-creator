import streamlit as st

def app():

    if st.session_state["authentication_status"]:
        st.header("Library")
        st.write(f"Welcome *{st.session_state['name']}*.")
        st.write("Content to show to authenticated users.")