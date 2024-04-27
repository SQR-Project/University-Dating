from unittest.mock import patch, MagicMock

from app.src.controllers import matching
from app.src.enums.interests_enum import Interest
from app.src.models.auth import VerifyAccessTokenResult
from app.src.models.profile import ProfileInformation
from app.src.models.response import SuccessResponse
from app.src.models.like import MatchingResponse

def test_router_data():
    assert matching.matching_router is not None
    assert matching.matching_router.prefix == "/matching"

    assert len(matching.matching_router.tags) == 1
    assert matching.matching_router.tags[0] == "matching"

    assert matching.matching_router.routes[0].path == "/matching/like"
    assert matching.matching_router.routes[1].path == "/matching/is-matched"


@patch("app.src.controllers.matching.auth_service.verify_access_token")
@patch("app.src.controllers.matching.like_service.like_profile")
def test_like(
        mock_like_profile,
        mock_verify_access_token
):
    # Arrange
    mock_verify_access_token.return_value = VerifyAccessTokenResult(
        user_id="UserId", email="Email")
    mock_like_profile.return_value = SuccessResponse()
    request = MagicMock()

    # Act
    response = matching.like(request)

    # Assert
    assert isinstance(response, SuccessResponse)
    assert response.status == "success"


@patch("app.src.controllers.profile.auth_service.verify_access_token")
@patch("app.src.controllers.matching.like_service.is_matched")
def test_is_matched(mock_is_matched, mock_verify_access_token):
    # Arrange
    mock_is_matched.return_value = MatchingResponse(matched = True)
    mock_verify_access_token.return_value = VerifyAccessTokenResult(
        user_id="UserId", email="Email")
    
    # Act
    request = MagicMock()
    response = matching.is_matched(request)

    # Assert
    assert isinstance(response, MatchingResponse)
    assert response.matched == True
