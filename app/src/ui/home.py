import streamlit as st


def app():
    if not st.session_state["loggedin"]:  # pragma: no mutate
        st.write("To view your matches please log in")  # pragma: no mutate
    else:
        st.write("Here soon to be matches")  # pragma: no mutate
