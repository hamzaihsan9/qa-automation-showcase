"""API Test Suite: ReqRes User Management & Pagination Contract Tests."""

import pytest
from tests.api.client import ReqResApiClient


@pytest.mark.api
@pytest.mark.regression
class TestReqResUsers:
    """Test user retrieval, pagination, creation and deletion."""

    def test_list_users_pagination(self, reqres_api: ReqResApiClient):
        """Verify user list response contains metadata, page count, and users array."""
        response = reqres_api.get_users(page=2)
        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 2
        assert "per_page" in data
        assert "total" in data
        assert "total_pages" in data
        assert isinstance(data["data"], list)
        assert len(data["data"]) > 0

        # Validate schema of each user item
        first_user = data["data"][0]
        assert "id" in first_user
        assert "email" in first_user
        assert "first_name" in first_user
        assert "last_name" in first_user
        assert "avatar" in first_user

    def test_get_single_user_found(self, reqres_api: ReqResApiClient):
        """Verify querying valid user ID returns 200 with populated details."""
        response = reqres_api.get_user(2)
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["id"] == 2
        assert data["email"] == "janet.weaver@reqres.in"
        assert data["first_name"] == "Janet"
        assert data["last_name"] == "Weaver"

    def test_get_single_user_not_found(self, reqres_api: ReqResApiClient):
        """Verify querying non-existent user returns 404 status."""
        response = reqres_api.get_user(23)
        assert response.status_code == 404

    def test_create_user(self, reqres_api: ReqResApiClient):
        """Verify user creation returns 201 with generated id and timestamp."""
        response = reqres_api.create_user(name="morpheus", job="leader")
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "morpheus"
        assert data["job"] == "leader"
        assert "id" in data
        assert "createdAt" in data

    def test_update_user(self, reqres_api: ReqResApiClient):
        """Verify user modification returns 200 with updated fields and updatedAt timestamp."""
        response = reqres_api.update_user(user_id=2, name="morpheus", job="zion resident")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "morpheus"
        assert data["job"] == "zion resident"
        assert "updatedAt" in data

    def test_delete_user(self, reqres_api: ReqResApiClient):
        """Verify user removal returns 204 No Content status."""
        response = reqres_api.delete_user(2)
        assert response.status_code == 204
