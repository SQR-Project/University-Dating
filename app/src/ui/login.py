
from http.client import HTTPException
from src.models.auth import AuthWithEmailRequest
from src.services.auth_service import ACCESS_TOKEN_NAME, REFRESH_TOKEN_NAME
import streamlit as st
from fastapi import Request, HTTPException
from requests import Response
from src.enums.interests_enum import Interest
from src.models.profile import CreateProfileRequest
from src.services import auth_service
from src.services import profile_service
from src.validators import email_validator
from extra_streamlit_components import CookieManager

def app():
    st.title('Welcome to University Dating')
    if 'userid' not in st.session_state:
        st.session_state['userid'] = ''
    if 'email' not in st.session_state:
        st.session_state['email'] = ''
    if 'loggedin' not in st.session_state:
        st.session_state['loggedin'] = False

    cookie_manager = CookieManager()

    def set_cookie(response: Response):
        data = response.json()
        access_token = data["idToken"]  # pragma: no mutate
        refresh_token = data["refreshToken"]  # pragma: no mutate

        cookie_manager.set(ACCESS_TOKEN_NAME, f'Bearer {access_token}', key='fuck')
        cookie_manager.set(REFRESH_TOKEN_NAME, refresh_token, key='you')


    def verify_access_cookie():
        access_cookie = cookie_manager.get(ACCESS_TOKEN_NAME)
        token_data = auth_service.verify_access_token_string(access_cookie)
        return token_data


    def register_and_create_account(email, password, name, surname, age, main_interest_box):
        email_validator.validate(email)
        auth_request = AuthWithEmailRequest(email = email, password = password)
        auth_response = auth_service.email_auth_call(
            auth_request,
            "accounts:signUp"  # pragma: no mutate
        )
        set_cookie(auth_response)

        token_data = verify_access_cookie()
        profile_to_create = CreateProfileRequest(name = name, surname = surname, age = age, primary_interest = Interest(main_interest_box))

        profile_service.create_profile(token_data, profile_to_create)
        st.session_state['userid'] = token_data.user_id
        st.session_state['email'] = token_data.email

    def login(email, password):
        email_validator.validate(email)
        auth_request = AuthWithEmailRequest(email = email, password = password)

        auth_response = auth_service.email_auth_call(
            auth_request,
            "accounts:signInWithPassword"  # pragma: no mutate
        )
        set_cookie(auth_response)

    def register_click(email, password, name, surname, age, main_interest_box):
        try:
            register_and_create_account(email, password, name, surname, age, main_interest_box)
            st.session_state['loggedin'] = True
            st.success('Account created successfully!')
        except HTTPException as e:
            st.warning(e.detail)

    def login_click(email, password):
        try:
            login(email, password)
            token_data = verify_access_cookie()
            st.session_state['userid'] = token_data.user_id
            st.session_state['email'] = token_data.email
            st.session_state['loggedin'] = True
        except HTTPException as e:
            st.warning(e.detail)

    def login_window():
        choice = st.selectbox('Login/Signup',['Login','Sign up'])
        email = st.text_input('Email Address')
        password = st.text_input('Password',type='password')

        if choice == 'Sign up':
            name = st.text_input('Name')
            surname = st.text_input('Surname')
            age = st.number_input('Age',value=None, placeholder="Type a number...", step=1)
            main_interest_box = st.selectbox('Main interest', [e.value for e in Interest])

            st.button('Create my account', on_click=register_click, args=[email, password, name, surname, age, main_interest_box])
        else:
            st.button('Login', on_click=login_click, args=[email, password])


    def sign_out():
        st.session_state['loggedin'] = False
        st.session_state['userid'] = ''
        st.session_state['email'] = ''

    if not st.session_state["loggedin"]:
        login_window()
    else:
        profile = profile_service.get_profile_by_email(st.session_state["email"])
        st.text('Name :'  + profile.name + ' ' + profile.surname)
        st.text('Email : ' + profile.email)
        st.text('Age : ' + str(profile.age))
        st.text('Main interest : ' + profile.primary_interest.value)
        st.button('Sign out', on_click=sign_out)