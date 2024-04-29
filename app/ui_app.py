from app.src.ui import login, matching
import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="University Dating",  # pragma: no mutate
)


class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):

        self.apps.append({
            "title": title,  # pragma: no mutate
            "function": func  # pragma: no mutate
        })

    def run():
        # app = st.sidebar(
        with st.sidebar:
            app = option_menu(
                menu_title='Dating site ',  # pragma: no mutate
                options=['Home', 'Account'],  # pragma: no mutate
                icons=['house-fill', 'person-circle'],  # pragma: no mutate
                menu_icon='chat-text-fill',  # pragma: no mutate
                default_index=1,
                styles={
                    "container": {  # pragma: no mutate
                        "padding": "5!important",   # pragma: no mutate
                        "background-color": 'black'  # pragma: no mutate
                    },  # pragma: no mutate
                    "icon": {  # pragma: no mutate
                        "color": "white",  # pragma: no mutate
                        "font-size": "23px"  # pragma: no mutate
                    },  # pragma: no mutate
                    "nav-link": {  # pragma: no mutate
                        "color": "white",  # pragma: no mutate
                        "font-size": "20px",  # pragma: no mutate
                        "text-align": "left",  # pragma: no mutate
                        "margin": "0px",  # pragma: no mutate
                        "--hover-color": "blue"  # pragma: no mutate
                    },  # pragma: no mutate
                    "nav-link-selected": {  # pragma: no mutate
                        "background-color": "#02ab21"  # pragma: no mutate
                    },  # pragma: no mutate
                }  # pragma: no mutate
            )

        if app == "Home":  # pragma: no mutate
            matching.app()
        if app == "Account":  # pragma: no mutate
            login.app()

    run()
