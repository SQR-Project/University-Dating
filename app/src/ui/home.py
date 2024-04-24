import streamlit as st

def app():
    if not st.session_state["loggedin"]:
        st.write("To view your matches please log in")
    else:
        st.write("Here soon to be matches")
