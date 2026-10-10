"""API Test Suite: Authentication & Authorization."""

import pytest
from tests.api.client import BookingApiClient, ReqResApiClient


@pytest.mark.api
@pytest.mark.smoke
class TestBookingAuth:
    """Test authentication flows for Restful-Booker."""

    def test_successful_token_generation(self, booking_api: BookingApiClient):
        """Verify token is generated with valid admin credentials."""
        token = booking_api.create_token(username="admin", password="password123")
        assert token is not None, "Auth token should not be null"
        assert len(token) > 0, "Auth token should not be empty string"

    def test_invalid_credentials_returns_bad_credentials(self, booking_api: BookingApiClient):
        """Verify server responds with Bad credentials message on wrong password."""
        response = booking_api.session.post(
            f"{booking_api.base_url}/auth",
            json={"username": "admin", "password": "wrong_password_999"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "reason" in data
        assert data["reason"] == "Bad credentials"


@pytest.mark.api
@pytest.mark.regression
class TestReqResAuth:
    """Test user registration and login workflows on ReqRes."""

    def test_successful_user_registration(self, reqres_api: ReqResApiClient):
        """Verify account creation returns valid user id and token."""
        response = reqres_api.register(email="eve.holt@reqres.in", password="pistol_pistol")
        assert response.status_code == 200
        data = response.json()
        assert "token" in data
        assert "id" in data

    def test_registration_missing_password_fails(self, reqres_api: ReqResApiClient):
        """Verify registration without password returns 400 error."""
        response = reqres_api.register(email="sydney@fife")
        assert response.status_code == 400
        data = response.json()
        assert data.get("error") == "Missing password"

    def test_successful_user_login(self, reqres_api: ReqResApiClient):
        """Verify standard user login returns auth token."""
        response = reqres_api.login(email="eve.holt@reqres.in", password="cityslicka")
        assert response.status_code == 200
        data = response.json()
        assert "token" in data

    def test_login_missing_password_fails(self, reqres_api: ReqResApiClient):
        """Verify login without password yields 400 error with descriptive message."""
        response = reqres_api.login(email="peter@klaven")
        assert response.status_code == 400
        assert response.json().get("error") == "Missing password"
