import streamlit as st
from requests import Response
from app.src.models.like import LikeProfileRequest
from app.src.services import like_service, auth_service, profile_service
from app.src.services.auth_service import ACCESS_TOKEN_NAME, REFRESH_TOKEN_NAME
from extra_streamlit_components import CookieManager


current_image_index = 0


st.title('Welcome to University Dating')

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


if 'current_index' not in st.session_state:
    st.session_state['current_index'] = 0

# images = [
#     "app/src/ui/pics/meme.jpg",
#     "app/src/ui/pics/meme2.jpg",
#     "app/src/ui/pics/cat1.jpg",
#     "app/src/ui/pics/cat3.jpg"
# ]

all_profiles = profile_service.get_all_profiles()
logins = [profile.email for profile in all_profiles]


col1, col2, col3 = st.columns([1, 1, 1])
next = col1.button("Next")
like = col2.button("Like")
prev = col3.button("Prev")


def render_next():
    session_state = st.session_state.get('current_index', 0)
    st.text(logins[session_state % len(logins)])
# st.image(images[(session_state + 1) % len(images)], use_column_width=True)
    st.session_state['current_index'] = session_state + 1


def render_prev():
    session_state = st.session_state.get('current_index', 0)
    st.text(logins[session_state % len(logins)])
# st.image(images[(session_state - 1) % len(images)], use_column_width=True)
    st.session_state['current_index'] = session_state - 1


def render_current():
    session_state = st.session_state.get('current_index', 0)
    st.text(logins[session_state % len(logins)])
# st.image(images[session_state % len(images)], use_column_width=True)


def render_like():
    session_state = st.session_state.get('current_index', 0)
    token_data = verify_access_cookie()
    like_profile_request = LikeProfileRequest(
        email=logins[session_state % len(logins)])
    like_service.like_profile(token_data, like_profile_request)
    st.markdown("<h1 style='text-align: center; font-size: 70px;'>💖</h1>",
                unsafe_allow_html=True)

    if like_service.is_matched(token_data, like_profile_request):
        st.markdown(
            "<h1 style='text-align: center; font-size: 70px;'>💖Matched💖</h1>",
            unsafe_allow_html=True
        )
    render_current()


if next:
    render_next()

if prev:
    render_prev()

if like:
    render_like()
