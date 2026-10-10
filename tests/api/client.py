"""REST API Client Wrappers for Restful-Booker and ReqRes APIs."""

from typing import Any, Dict, Optional
import requests


class BookingApiClient:
    """HTTP client wrapper for Restful-Booker service."""

    BASE_URL = "https://restful-booker.herokuapp.com"

    def __init__(self, base_url: Optional[str] = None):
        self.base_url = (base_url or self.BASE_URL).rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })
        self._token: Optional[str] = None

    def health_check(self) -> requests.Response:
        """Ping endpoint to verify API health."""
        return self.session.get(f"{self.base_url}/ping")

    def create_token(self, username: str = "admin", password: str = "password123") -> str:
        """Authenticate and obtain auth token."""
        payload = {"username": username, "password": password}
        response = self.session.post(f"{self.base_url}/auth", json=payload)
        response.raise_for_status()
        self._token = response.json().get("token")
        return self._token

    @property
    def token(self) -> str:
        """Retrieve cached token or generate a new one."""
        if not self._token:
            self.create_token()
        return self._token

    def _get_auth_headers(self, custom_token: Optional[str] = None) -> Dict[str, str]:
        token_val = custom_token or self.token
        return {
            "Cookie": f"token={token_val}",
            "Authorisation": f"Basic {token_val}",
        }

    def get_booking_ids(self, params: Optional[Dict[str, Any]] = None) -> requests.Response:
        """List booking IDs with optional query filters."""
        return self.session.get(f"{self.base_url}/booking", params=params)

    def get_booking(self, booking_id: int) -> requests.Response:
        """Retrieve booking record by ID."""
        return self.session.get(f"{self.base_url}/booking/{booking_id}")

    def create_booking(self, payload: Dict[str, Any]) -> requests.Response:
        """Create a new booking entry."""
        return self.session.post(f"{self.base_url}/booking", json=payload)

    def update_booking(
        self, booking_id: int, payload: Dict[str, Any], token: Optional[str] = None
    ) -> requests.Response:
        """Fully update booking record (PUT)."""
        headers = self._get_auth_headers(token)
        return self.session.put(f"{self.base_url}/booking/{booking_id}", json=payload, headers=headers)

    def partial_update_booking(
        self, booking_id: int, payload: Dict[str, Any], token: Optional[str] = None
    ) -> requests.Response:
        """Partially update booking record (PATCH)."""
        headers = self._get_auth_headers(token)
        return self.session.patch(f"{self.base_url}/booking/{booking_id}", json=payload, headers=headers)

    def delete_booking(self, booking_id: int, token: Optional[str] = None) -> requests.Response:
        """Delete booking record by ID."""
        headers = self._get_auth_headers(token)
        return self.session.delete(f"{self.base_url}/booking/{booking_id}", headers=headers)


class ReqResApiClient:
    """HTTP client wrapper for ReqRes mock REST API."""

    BASE_URL = "https://reqres.in/api"

    def __init__(self, base_url: Optional[str] = None):
        self.base_url = (base_url or self.BASE_URL).rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

    def get_users(self, page: int = 1) -> requests.Response:
        """Retrieve paginated list of users."""
        return self.session.get(f"{self.base_url}/users", params={"page": page})

    def get_user(self, user_id: int) -> requests.Response:
        """Retrieve single user details."""
        return self.session.get(f"{self.base_url}/users/{user_id}")

    def create_user(self, name: str, job: str) -> requests.Response:
        """Create new user profile."""
        return self.session.post(f"{self.base_url}/users", json={"name": name, "job": job})

    def update_user(self, user_id: int, name: str, job: str) -> requests.Response:
        """Update existing user profile (PUT)."""
        return self.session.put(f"{self.base_url}/users/{user_id}", json={"name": name, "job": job})

    def delete_user(self, user_id: int) -> requests.Response:
        """Delete user profile by ID."""
        return self.session.delete(f"{self.base_url}/users/{user_id}")

    def register(self, email: str, password: Optional[str] = None) -> requests.Response:
        """Register account."""
        payload: Dict[str, Any] = {"email": email}
        if password is not None:
            payload["password"] = password
        return self.session.post(f"{self.base_url}/register", json=payload)

    def login(self, email: str, password: Optional[str] = None) -> requests.Response:
        """Authenticate user."""
        payload: Dict[str, Any] = {"email": email}
        if password is not None:
            payload["password"] = password
        return self.session.post(f"{self.base_url}/login", json=payload)
