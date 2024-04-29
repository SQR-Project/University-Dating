from streamlit.testing.v1 import AppTest
from unittest.mock import patch, call
from app.src.models.profile import ProfileInformation
from app.src.models.like import MatchingResponse, LikeProfileRequest
from app.src.enums import interests_enum
from app.src.models.auth import VerifyAccessTokenResult

default_profile = ProfileInformation(
    email="Some email",
    name="Name",
    surname="Surname",
    age=5,
    liked_profiles="Masha",
    primary_interest=interests_enum.Interest.MUSIC
)

default_like_request = LikeProfileRequest(email='Some email')

like_text = "<h1 style='text-align: center; font-size: 70px;'>💖</h1>"
matching_text = (
    "<h1 style='text-align: center; font-size: 70px;'>💖Matched💖</h1>"
)

valid_token_data = VerifyAccessTokenResult(
    user_id="1",
    email="email"
)


@patch('app.src.ui.matching.profile_service.get_all_profiles')
def test_run(mock_get_all_profiles):
    mock_get_all_profiles.return_value = []
    at = AppTest.from_file("app/src/ui/matching.py").run()

    assert "Welcome to University Dating" in at.title[0].value
    assert not at.exception


@patch('app.src.ui.matching.profile_service.get_all_profiles')
def test_title(mock_get_all_profiles):
    mock_get_all_profiles.return_value = [default_profile]
    at = AppTest.from_file("app/src/ui/matching.py").run()

    assert not at.exception
    assert "Welcome to University Dating" in at.title[0].value


@patch('app.src.ui.matching.like_service.is_matched')
@patch('app.src.ui.matching.auth_service.verify_access_token_string')
@patch('app.src.ui.matching.profile_service.get_all_profiles')
def test_all_buttons(
    mock_get_all_profiles,
    mock_verify_access_token_string,
    mock_is_matched
):
    expected_calls = [call(), call()]
    mock_is_matched.return_value = MatchingResponse(matched=True)
    mock_verify_access_token_string.return_value = valid_token_data
    mock_get_all_profiles.return_value = [default_profile]

    at = AppTest.from_file("app/src/ui/matching.py").run()

    assert at.button[0].value is False
    at.button[0].click().run()
    assert at.button[0].value
    assert at.text[0].value == default_profile.email

    assert at.button[1].value is False
    at.button[1].click().run()
    assert at.button[1].value
    assert at.text[0].value == default_profile.email

    assert at.button[2].value is False
    at.button[2].click().run()
    assert at.button[2].value

    assert at.text[0].value == default_profile.email
    assert not at.exception
    assert "Welcome to University Dating" in at.title[0].value
    mock_is_matched.assert_called_once_with(
        valid_token_data, default_like_request)
    mock_get_all_profiles.assert_has_calls(expected_calls)


@patch('app.src.ui.matching.profile_service.get_all_profiles')
def test_next_button_click_behaviour(mock_get_all_profiles):
    mock_get_all_profiles.return_value = [default_profile]

    at = AppTest.from_file("app/src/ui/matching.py").run()

    assert at.session_state['current_index'] == 0

    at.button[0].click().run()

    assert at.session_state['current_index'] == 1
    assert "Welcome to University Dating" in at.title[0].value
    assert at.text[0].value == default_profile.email


@patch('app.src.ui.matching.profile_service.get_all_profiles')
def test_prev_button_click_behaviour(mock_get_all_profiles):
    mock_get_all_profiles.return_value = [default_profile]

    at = AppTest.from_file("app/src/ui/matching.py").run()

    assert at.session_state['current_index'] == 0

    at.button[2].click().run()

    assert at.session_state['current_index'] == -1
    assert not at.exception
    assert "Welcome to University Dating" in at.title[0].value
    assert at.text[0].value == default_profile.email


@patch('app.src.ui.matching.like_service.is_matched')
@patch('app.src.ui.matching.auth_service.verify_access_token_string')
@patch('app.src.ui.matching.profile_service.get_all_profiles')
def test_like_button_click_behaviour(
    mock_get_all_profiles,
    mock_verify_access_token_string,
    mock_is_matched
):
    expected_calls = [call(), call()]

    mock_is_matched.return_value = MatchingResponse(matched=True)
    mock_verify_access_token_string.return_value = valid_token_data
    mock_get_all_profiles.return_value = [default_profile]

    at = AppTest.from_file("app/src/ui/matching.py").run()

    assert at.session_state['current_index'] == 0

    at.button[1].click().run()

    assert at.text[0].value == default_profile.email
    assert at.session_state['current_index'] == 0
    assert not at.exception
    assert "Welcome to University Dating" in at.title[0].value
    mock_is_matched.assert_called_once_with(
        valid_token_data, default_like_request)
    mock_get_all_profiles.assert_has_calls(expected_calls)


@patch('app.src.ui.matching.like_service.is_matched')
@patch('app.src.ui.matching.auth_service.verify_access_token_string')
@patch('app.src.ui.matching.profile_service.get_all_profiles')
def test_like_button_text(
    mock_get_all_profiles,
    mock_verify_access_token_string,
    mock_is_matched
):
    expected_calls = [call(), call()]
    mock_is_matched.return_value = MatchingResponse(matched=True)
    mock_verify_access_token_string.return_value = valid_token_data
    mock_get_all_profiles.return_value = [default_profile]

    at = AppTest.from_file("app/src/ui/matching.py").run()

    at.button[1].click().run()

    assert at.text[0].value == default_profile.email
    assert like_text in at.markdown[1].value
    assert not at.exception
    assert "Welcome to University Dating" in at.title[0].value
    mock_is_matched.assert_called_once_with(
        valid_token_data, default_like_request)
    mock_get_all_profiles.assert_has_calls(expected_calls)


@patch('app.src.ui.matching.like_service.is_matched')
@patch('app.src.ui.matching.auth_service.verify_access_token_string')
@patch('app.src.ui.matching.profile_service.get_all_profiles')
def test_like_button_if_matched(
    mock_get_all_profiles,
    mock_verify_access_token_string,
    mock_is_matched
):
    expected_calls = [call(), call()]
    mock_is_matched.return_value = MatchingResponse(matched=True)
    mock_verify_access_token_string.return_value = valid_token_data
    mock_get_all_profiles.return_value = [default_profile]

    at = AppTest.from_file("app/src/ui/matching.py").run()

    at.button[1].click().run()

    assert at.text[0].value == default_profile.email
    assert matching_text in at.markdown[2].value
    assert not at.exception
    assert "Welcome to University Dating" in at.title[0].value
    mock_is_matched.assert_called_once_with(
        valid_token_data, default_like_request)
    mock_get_all_profiles.assert_has_calls(expected_calls)


@patch('app.src.ui.matching.like_service.is_matched')
@patch('app.src.ui.matching.auth_service.verify_access_token_string')
@patch('app.src.ui.matching.profile_service.get_all_profiles')
def test_like_button_if_not_matched(
    mock_get_all_profiles,
    mock_verify_access_token_string,
    mock_is_matched
):
    expected_calls = [call(), call()]
    mock_is_matched.return_value = MatchingResponse(matched=False)
    mock_verify_access_token_string.return_value = valid_token_data
    mock_get_all_profiles.return_value = [default_profile]

    at = AppTest.from_file("app/src/ui/matching.py").run()

    at.button[1].click().run()

    assert matching_text in at.markdown[2].value
    assert not at.exception
    assert "Welcome to University Dating" in at.title[0].value
    assert at.text[0].value == default_profile.email
    mock_get_all_profiles.assert_has_calls(expected_calls)
    mock_is_matched.assert_called_once_with(
        valid_token_data, default_like_request)
