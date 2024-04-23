
from http.client import HTTPException
from src.models.auth import AuthWithEmailRequest
from src.services.auth_service import ACCESS_TOKEN_NAME, REFRESH_TOKEN_NAME
import streamlit as st
import json
from fastapi import Request, HTTPException
from requests import Response
from src.enums.interests_enum import Interest
from src.models.profile import CreateProfileRequest
from src.services import auth_service
from src.services import profile_service
from src.validators import email_validator
import extra_streamlit_components as stx

cookie_manager = stx.CookieManager()

def set_cookie(response: Response):
    data = response.json()
    access_token = data["idToken"]  # pragma: no mutate
    refresh_token = data["refreshToken"]  # pragma: no mutate

    cookie_manager.set(ACCESS_TOKEN_NAME, f'Bearer {access_token}', key='fuck')
    cookie_manager.set(REFRESH_TOKEN_NAME, refresh_token, key='you')


def verify_access_cookie():
    access_cookie = cookie_manager.get(ACCESS_TOKEN_NAME)
    token_data = auth_service.verify_access_token_string(access_cookie)
    print(st.session_state)
    st.session_state.userid = token_data.user_id
    st.session_state.email = token_data.email
    print("YAY")


def register_and_create_account(email, password, name, surname, age, main_interest_box):
    email_validator.validate(email)
    auth_request = AuthWithEmailRequest(email = email, password = password)
    auth_response = auth_service.email_auth_call(
        auth_request,
        "accounts:signUp"  # pragma: no mutate
    )
    set_cookie(auth_response)

    print("NO TOKEN DATA")
    token_data = verify_access_cookie()
    profile_to_create = CreateProfileRequest(name = name, surname = surname, age = age, primary_interest = Interest(main_interest_box))
    print("TOKEN DATA IS HERE")

    profile_service.create_profile(token_data, profile_to_create)
    print("YAY")

def login(email, password):
    print("BLYAT!!")
    print("BLYAT!!", password)
    email_validator.validate(email)
    auth_request = AuthWithEmailRequest(email = email, password = password)

    auth_response = auth_service.email_auth_call(
        auth_request,
        "accounts:signInWithPassword"  # pragma: no mutate
    )
    set_cookie(auth_response)


def login_window():
    choice = st.selectbox('Login/Signup',['Login','Sign up'])
    email = st.text_input('Email Address')
    password = st.text_input('Password',type='password')

    if choice == 'Sign up':
        name = st.text_input('Name')
        surname = st.text_input('Surname')
        age = st.number_input('Age',value=None, placeholder="Type a number...", step=1)
        main_interest_box = st.selectbox('Main interest', [e.value for e in Interest])

        if st.button('Create my account'):
            try:
                register_and_create_account(email, password, name, surname, age, main_interest_box)
                print("YAY")
                st.session_state.loggedin = True
                st.success('Account created successfully!')
            except HTTPException as e:
                st.warning(e.detail)
    else:
        if (st.button('Login')):
            try:
                login(email, password)
                verify_access_cookie()
                st.session_state.loggedin = True
                st.success('Login successfull!')
            except HTTPException as e:
                st.warning(e.detail)

def account_window():
    print("YEAH")
    profile = profile_service.get_profile_by_email(st.session_state.email)
    st.text('Name '  + profile.name + ' ' + profile.surname)
    st.text('Email : ' + profile.email)
    st.text('Age: ' + profile.age)
    st.text('Main interest: ' + profile.primary_interest)
    st.button('Sign out', on_click=sign_out)

def sign_out():
    st.session_state.logged_in = False
    st.session_state.userid = ''
    st.session_state.email = ''

def app():
    st.title('Welcome to University Dating')
    if 'userid' not in st.session_state:
        st.session_state.userid = ''
    if 'email' not in st.session_state:
        st.session_state.email = ''
    if 'loggedin' not in st.session_state:
        st.session_state['loggedin'] = False

    if not st.session_state["loggedin"]:
        login_window()
    else:
        account_window()

