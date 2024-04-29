import unittest
from app.src.models.profile import ProfileInformation
import pytest
from unittest.mock import patch, MagicMock
from app.src.models.auth import VerifyAccessTokenResult
from app.src.models.response import SuccessResponse
from app.src.enums.interests_enum import Interest
from fastapi import HTTPException
from streamlit.testing.v1 import AppTest
from tests.unit.services.test_auth_service import VALID_ACCESS_TOKEN, VALID_EMAIL, VALID_REFRESH_TOKEN, VALID_USER_ID

def valid_email_auth_data_response():
    return {
        "idToken": VALID_ACCESS_TOKEN,
        "refreshToken": VALID_REFRESH_TOKEN,
        "email": VALID_EMAIL,
        "localId": VALID_USER_ID
    }

def valid_verify_accss_token_response():
    return VerifyAccessTokenResult(
        user_id = VALID_USER_ID,
        email = VALID_EMAIL
    )

def valid_profile():
    return ProfileInformation(
            email=VALID_EMAIL,
            name="Name",
            surname="Surname",
            liked_profiles="",
            age=22,
            primary_interest="music"
        )

class TestButtonProcessing(unittest.TestCase):

    def test_page(self):
        at = AppTest.from_file("app/src/ui/login.py")
        at.run()
        assert not at.exception
        assert not at.session_state["loggedin"]
        assert at.session_state["userid"] == ""
        assert at.session_state['email'] == ''
        assert at.title[0].body == "Welcome to University Dating"

    def test_login_window_selectbox_select_signup(self):
        at = AppTest.from_file("app/src/ui/login.py")
        at.run()
        at.selectbox[0].set_value("Sign up").run()

        assert at.text_input[0].label == "Email Address"
        assert at.text_input[1].label == "Password"

        assert at.number_input[0].label == "Age"
        assert at.number_input[0].placeholder == "Type a number..."
        assert at.number_input[0].step == 1

        assert at.selectbox[1].label == "Main interest"
        assert at.selectbox[1].options == ["sport", "programming", "reading", "travel", "music"]

        assert at.button[0].label == "Create my account"

    def test_login_window_selectbox_select_login(self):
        at = AppTest.from_file("app/src/ui/login.py")
        at.run()
        at.selectbox[0].set_value("Login").run()

        assert at.text_input[0].label == "Email Address"
        assert at.text_input[1].label == "Password"

        assert at.button[0].label == "Login"

    @patch('app.src.ui.login.profile_service.create_profile')
    @patch('app.src.ui.login.auth_service.verify_access_token_string')
    @patch('app.src.ui.login.auth_service.email_auth_call')
    def test_login_window_button_sign_up_success(
        self,
        mock_auth,
        mock_verify_access_cookie,
        mock_create_account
    ):
        at = AppTest.from_file("app/src/ui/login.py")
        at.run()
        at.selectbox[0].set_value("Sign up").run()

        at.text_input[0].set_value("e.mail@innopolis.university").run()
        at.text_input[1].set_value("p@ssword").run()
        at.number_input[0].set_value(22).run()
        at.selectbox[1].set_value("programming").run()

        mock_auth.return_value.json.return_value = valid_email_auth_data_response()
        mock_verify_access_cookie.return_value = valid_verify_accss_token_response()
        mock_create_account.return_value = SuccessResponse()

        at.button[0].click().run()

        assert at.session_state["loggedin"]
        assert at.session_state["userid"] == VALID_USER_ID
        assert at.session_state['email'] == VALID_EMAIL
        assert at.success[0].value == "Account created successfully!"

    @patch('app.src.ui.login.profile_service.create_profile')
    @patch('app.src.ui.login.auth_service.verify_access_token_string')
    @patch('app.src.ui.login.auth_service.email_auth_call', side_effect = HTTPException(
            status_code=401,
            detail={
                "status": "error",
                "message": "Test error message"
            }
        ))
    def test_login_window_button_sign_up_auth_error(
        self,
        mock_auth,
        mock_verify_access_cookie,
        mock_create_account
    ):
        at = AppTest.from_file("app/src/ui/login.py")
        at.run()
        at.selectbox[0].set_value("Sign up").run()

        at.text_input[0].set_value("e.mail@innopolis.university").run()
        at.text_input[1].set_value("p@ssword").run()
        at.number_input[0].set_value(22).run()
        at.selectbox[1].set_value("programming").run()

        mock_verify_access_cookie.return_value = valid_verify_accss_token_response()
        mock_create_account.return_value = SuccessResponse()

        at.button[0].click().run()

        assert not at.session_state["loggedin"]
        assert at.session_state["userid"] == ""
        assert at.session_state['email'] == ''
        assert at.warning[0].value == "{'status': 'error', 'message': 'Test error message'}"

    @patch('app.src.ui.login.profile_service.create_profile', side_effect = HTTPException(
            status_code=400,
            detail="Profile does not exist"
        ))
    @patch('app.src.ui.login.auth_service.verify_access_token_string')
    @patch('app.src.ui.login.auth_service.email_auth_call')
    def test_login_window_button_sign_up_account_exists(
        self,
        mock_auth,
        mock_verify_access_cookie,
        mock_create_account
    ):
        at = AppTest.from_file("app/src/ui/login.py")
        at.run()
        at.selectbox[0].set_value("Sign up").run()

        at.text_input[0].set_value("e.mail@innopolis.university").run()
        at.text_input[1].set_value("p@ssword").run()
        at.number_input[0].set_value(22).run()
        at.selectbox[1].set_value("programming").run()

        mock_auth.return_value.json.return_value = valid_email_auth_data_response()
        mock_verify_access_cookie.return_value = valid_verify_accss_token_response()

        at.button[0].click().run()

        assert not at.session_state["loggedin"]
        assert at.session_state["userid"] == ""
        assert at.session_state['email'] == ''
        assert at.warning[0].value == "Profile does not exist"


    @patch('app.src.ui.login.profile_service.create_profile')
    @patch('app.src.ui.login.auth_service.verify_access_token_string')
    @patch('app.src.ui.login.auth_service.email_auth_call')
    def test_login_window_button_login_success(
        self,
        mock_auth,
        mock_verify_access_cookie,
        mock_create_account
    ):
        at = AppTest.from_file("app/src/ui/login.py")
        at.run()
        at.selectbox[0].set_value("Login").run()

        at.text_input[0].set_value("e.mail@innopolis.university").run()
        at.text_input[1].set_value("p@ssword").run()

        mock_auth.return_value.json.return_value = valid_email_auth_data_response()
        mock_verify_access_cookie.return_value = valid_verify_accss_token_response()
        mock_create_account.return_value = SuccessResponse()
        at.button[0].click().run()

        assert at.session_state["loggedin"]
        assert at.session_state["userid"] == VALID_USER_ID
        assert at.session_state['email'] == VALID_EMAIL

    @patch('app.src.ui.login.profile_service.create_profile')
    @patch('app.src.ui.login.auth_service.verify_access_token_string')
    @patch('app.src.ui.login.auth_service.email_auth_call', side_effect = HTTPException(
            status_code=401,
            detail={
                "status": "error",
                "message": "Test error login message"
            }
        ))
    def test_login_window_button_login_auth_error(
        self,
        mock_auth,
        mock_verify_access_cookie,
        mock_create_account
    ):
        at = AppTest.from_file("app/src/ui/login.py")
        at.run()
        at.selectbox[0].set_value("Login").run()

        at.text_input[0].set_value("e.mail@innopolis.university").run()
        at.text_input[1].set_value("p@ssword").run()

        mock_verify_access_cookie.return_value = valid_verify_accss_token_response()
        mock_create_account.return_value = SuccessResponse()
        at.button[0].click().run()

        assert not at.session_state["loggedin"]
        assert at.session_state["userid"] == ""
        assert at.session_state['email'] == ''
        assert at.warning[0].value == "{'status': 'error', 'message': 'Test error login message'}"

    @patch('app.src.ui.login.profile_service.get_profile_by_email')
    def test_logged_in(
        self,
        mock_get_profile
    ):
        at = AppTest.from_file("app/src/ui/login.py")
        at.session_state["loggedin"] = True
        at.session_state["userid"] = VALID_USER_ID
        at.session_state['email'] = VALID_EMAIL

        mock_get_profile.return_value = valid_profile()

        at.run()

        assert at.text[0].value == "Name : Name Surname"
        assert at.text[1].value == "Email : " + VALID_EMAIL
        assert at.text[2].value == "Age : 22"
        assert at.text[3].value == "Main interest : music"

        assert at.button[0].label == "Sign out"

    @patch('app.src.ui.login.profile_service.get_profile_by_email')
    def test_logged_in_sign_out(
        self,
        mock_get_profile
    ):
        at = AppTest.from_file("app/src/ui/login.py")
        at.session_state["loggedin"] = True
        at.session_state["userid"] = VALID_USER_ID
        at.session_state['email'] = VALID_EMAIL

        mock_get_profile.return_value = valid_profile()

        at.run()

        assert at.text[0].value == "Name : Name Surname"
        assert at.text[1].value == "Email : " + VALID_EMAIL
        assert at.text[2].value == "Age : 22"
        assert at.text[3].value == "Main interest : music"

        assert at.button[0].label == "Sign out"

        at.button[0].click().run()

        assert not at.session_state["loggedin"]
        assert at.session_state["userid"] == ""
        assert at.session_state['email'] == ''
        assert at.title[0].body == "Welcome to University Dating"


if __name__ == '__main__':
    unittest.main()