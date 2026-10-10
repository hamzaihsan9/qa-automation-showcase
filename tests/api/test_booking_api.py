"""API Test Suite: Restful-Booker Booking CRUD Operations & Schema Validation."""

import pytest
from typing import Dict, Any
from tests.api.client import BookingApiClient


@pytest.mark.api
@pytest.mark.regression
class TestBookingOperations:
    """End-to-end lifecycle testing for bookings."""

    def test_health_check(self, booking_api: BookingApiClient):
        """Verify API service ping endpoint returns 201 Created."""
        response = booking_api.health_check()
        assert response.status_code == 201, f"Expected 201 Created, got {response.status_code}"

    def test_get_booking_ids_list(self, booking_api: BookingApiClient):
        """Verify fetching list of booking IDs returns non-empty list of objects with bookingid."""
        response = booking_api.get_booking_ids()
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        assert "bookingid" in data[0]

    def test_create_and_retrieve_booking(
        self, booking_api: BookingApiClient, sample_booking_payload: Dict[str, Any]
    ):
        """Verify booking creation returns assigned ID and matches payload structure."""
        # Create
        create_res = booking_api.create_booking(sample_booking_payload)
        assert create_res.status_code == 200
        created_data = create_res.json()
        assert "bookingid" in created_data
        booking_id = created_data["bookingid"]
        assert created_data["booking"]["firstname"] == sample_booking_payload["firstname"]
        assert created_data["booking"]["totalprice"] == sample_booking_payload["totalprice"]

        # Retrieve
        get_res = booking_api.get_booking(booking_id)
        assert get_res.status_code == 200
        retrieved_data = get_res.json()
        assert retrieved_data["firstname"] == sample_booking_payload["firstname"]
        assert retrieved_data["lastname"] == sample_booking_payload["lastname"]
        assert retrieved_data["bookingdates"]["checkin"] == sample_booking_payload["bookingdates"]["checkin"]

    def test_update_booking_full(
        self, booking_api: BookingApiClient, sample_booking_payload: Dict[str, Any]
    ):
        """Verify updating entire booking record with authorized PUT request."""
        # 1. Create initial booking
        create_res = booking_api.create_booking(sample_booking_payload)
        assert create_res.status_code == 200
        booking_id = create_res.json()["bookingid"]

        # 2. Modify payload
        updated_payload = sample_booking_payload.copy()
        updated_payload["firstname"] = "Alexander-Updated"
        updated_payload["totalprice"] = 999

        # 3. Perform PUT update
        update_res = booking_api.update_booking(booking_id, updated_payload)
        assert update_res.status_code == 200
        updated_data = update_res.json()
        assert updated_data["firstname"] == "Alexander-Updated"
        assert updated_data["totalprice"] == 999

    def test_partial_update_booking_patch(
        self, booking_api: BookingApiClient, sample_booking_payload: Dict[str, Any]
    ):
        """Verify partial update modifying only targeted fields via PATCH request."""
        # 1. Create booking
        create_res = booking_api.create_booking(sample_booking_payload)
        booking_id = create_res.json()["bookingid"]

        # 2. Patch specific attributes
        patch_payload = {
            "firstname": "Morgan",
            "additionalneeds": "VIP Champagne Service",
        }
        patch_res = booking_api.partial_update_booking(booking_id, patch_payload)
        assert patch_res.status_code == 200
        data = patch_res.json()
        assert data["firstname"] == "Morgan"
        assert data["additionalneeds"] == "VIP Champagne Service"
        # Ensure unaffected fields remain preserved
        assert data["lastname"] == sample_booking_payload["lastname"]

    def test_delete_booking(
        self, booking_api: BookingApiClient, sample_booking_payload: Dict[str, Any]
    ):
        """Verify booking deletion removes record and returns 201 Created status."""
        # 1. Create booking
        create_res = booking_api.create_booking(sample_booking_payload)
        booking_id = create_res.json()["bookingid"]

        # 2. Delete
        delete_res = booking_api.delete_booking(booking_id)
        assert delete_res.status_code in (201, 200)

        # 3. Confirm deletion
        get_res = booking_api.get_booking(booking_id)
        assert get_res.status_code == 404

    def test_get_nonexistent_booking_returns_404(self, booking_api: BookingApiClient):
        """Verify querying non-existent booking ID yields 404 Not Found."""
        response = booking_api.get_booking(999999999)
        assert response.status_code == 404
