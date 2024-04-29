from src.models.auth import AuthWithEmailRequest
from src.services.auth_service import ACCESS_TOKEN_NAME, REFRESH_TOKEN_NAME
import streamlit as st
from fastapi import HTTPException
from requests import Response
from src.enums.interests_enum import Interest
from src.models.profile import CreateProfileRequest
from src.services import auth_service
from src.services import profile_service
from src.validators import email_validator
from extra_streamlit_components import CookieManager


def app():
    st.title('Welcome to University Dating')  # pragma: no mutate
    if 'userid' not in st.session_state:
        st.session_state['userid'] = ''  # pragma: no mutate
    if 'email' not in st.session_state:
        st.session_state['email'] = ''  # pragma: no mutate
    if 'loggedin' not in st.session_state:
        st.session_state['loggedin'] = False  # pragma: no mutate

    cookie_manager = CookieManager()

    def set_cookie(response: Response):
        data = response.json()
        access_token = data["idToken"]  # pragma: no mutate
        refresh_token = data["refreshToken"]  # pragma: no mutate

        cookie_manager.set(
            ACCESS_TOKEN_NAME,
            f'Bearer {access_token}',  # pragma: no mutate
            key='fuck'  # pragma: no mutate
        )  # pragma: no mutate
        cookie_manager.set(
            REFRESH_TOKEN_NAME,
            refresh_token,
            key='you'  # pragma: no mutate
        )  # pragma: no mutate

    def verify_access_cookie():
        access_cookie = cookie_manager.get(ACCESS_TOKEN_NAME)
        token_data = auth_service.verify_access_token_string(access_cookie)
        return token_data

    def register_and_create_account(
        email,
        password,
        name,
        surname,
        age,
        main_interest_box
    ):
        email_validator.validate(email)
        auth_request = AuthWithEmailRequest(email=email, password=password)
        auth_response = auth_service.email_auth_call(
            auth_request,
            "accounts:signUp"  # pragma: no mutate
        )  # pragma: no mutate
        set_cookie(auth_response)

        token_data = verify_access_cookie()
        profile_to_create = CreateProfileRequest(
            name=name,
            surname=surname,
            age=age,
            primary_interest=main_interest_box
        )

        profile_service.create_profile(token_data, profile_to_create)
        st.session_state['userid'] = token_data.user_id  # pragma: no mutate
        st.session_state['email'] = token_data.email  # pragma: no mutate

    def login(email, password):
        email_validator.validate(email)
        auth_request = AuthWithEmailRequest(email=email, password=password)

        auth_response = auth_service.email_auth_call(
            auth_request,
            "accounts:signInWithPassword"  # pragma: no mutate
        )  # pragma: no mutate
        set_cookie(auth_response)

    def register_click(email, password, name, surname, age, main_interest_box):
        try:
            register_and_create_account(
                email, password, name, surname, age, main_interest_box)
            st.session_state['loggedin'] = True  # pragma: no mutate
            st.success('Account created successfully!')  # pragma: no mutate
        except HTTPException as e:
            st.warning(e.detail)

    def login_click(email, password):
        try:
            login(email, password)
            token_data = verify_access_cookie()
            st.session_state['userid'] = token_data.user_id  # pragma: no mutate  # noqa: E501
            st.session_state['email'] = token_data.email  # pragma: no mutate
            st.session_state['loggedin'] = True  # pragma: no mutate
        except HTTPException as e:
            st.warning(e.detail)

    def login_window():
        choice = st.selectbox('Login/Signup', ['Login', 'Sign up'])  # pragma: no mutate  # noqa: E501
        email = st.text_input('Email Address')  # pragma: no mutate
        password = st.text_input('Password', type='password')  # pragma: no mutate  # noqa: E501

        if choice == 'Sign up':
            name = st.text_input('Name')  # pragma: no mutate
            surname = st.text_input('Surname')  # pragma: no mutate
            age = st.number_input(
                'Age',  # pragma: no mutate
                value=None,  # pragma: no mutate
                placeholder="Type a number...", step=1  # pragma: no mutate
            )  # pragma: no mutate
            main_interest_box = st.selectbox(
                'Main interest',  # pragma: no mutate
                [e.value for e in Interest]  # pragma: no mutate
            )  # pragma: no mutate

            st.button(
                'Create my account',  # pragma: no mutate
                on_click=register_click,
                args=[
                    email,
                    password,
                    name,
                    surname,
                    age,
                    main_interest_box
                ])  # pragma: no mutate
        else:
            st.button(
                'Login',  # pragma: no mutate
                on_click=login_click,
                args=[email, password]
            )  # pragma: no mutate

    def sign_out():
        st.session_state['loggedin'] = False  # pragma: no mutate
        st.session_state['userid'] = ''  # pragma: no mutate
        st.session_state['email'] = ''  # pragma: no mutate

    if not st.session_state.get("loggedin", False):  # pragma: no mutate
        login_window()
    else:
        profile = profile_service.get_profile_by_email(
            st.session_state["email"])  # pragma: no mutate
        st.text('Name : ' + profile.name + ' ' + profile.surname)  # pragma: no mutate  # noqa: E501
        st.text('Email : ' + profile.email)  # pragma: no mutate
        st.text('Age : ' + str(profile.age))  # pragma: no mutate
        st.text('Main interest : ' + profile.primary_interest.value)  # pragma: no mutate  # noqa: E501
        st.button('Sign out', on_click=sign_out)  # pragma: no mutate


app()