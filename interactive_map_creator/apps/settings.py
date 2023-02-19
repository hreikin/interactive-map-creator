import streamlit as st

def app():

    if st.session_state["authentication_status"]:
        st.header("Settings")
        st.subheader(f"Welcome *{st.session_state['name']}*.")
    try:
        if st.session_state["authenticator"].update_user_details(st.session_state["username"], "Update User Details"):
            st.success("Entries updated successfully.")
    except Exception as e:
        st.error(e)
    try:
        if st.session_state["authenticator"].reset_password(st.session_state["username"], "Change Password"):
            st.success("Password modified successfully.")
    except Exception as e:
        st.error(e)