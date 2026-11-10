import requests

from config import settings


class ReqResClient:
    """Thin wrapper around the ReqRes REST API."""

    def __init__(self):
        self.base = settings.API_BASE_URL.rstrip("/")
        self.session = requests.Session()
        if settings.REQRES_API_KEY:
            self.session.headers["x-api-key"] = settings.REQRES_API_KEY

    def _request(self, method, path, **kwargs):
        resp = self.session.request(
            method, self.base + path, timeout=settings.API_TIMEOUT, **kwargs
        )
        if resp.status_code >= 400:
            # pytest shows captured stdout for failing tests, which makes CI failures easier to read
            print(f"{method} {path} -> {resp.status_code}: {resp.text[:300]}")
        return resp

    def list_users(self, page=1):
        return self._request("GET", "/users", params={"page": page})

    def get_user(self, user_id):
        return self._request("GET", f"/users/{user_id}")

    def create_user(self, name, job):
        return self._request("POST", "/users", json={"name": name, "job": job})

    def update_user(self, user_id, name, job):
        return self._request("PUT", f"/users/{user_id}", json={"name": name, "job": job})

    def delete_user(self, user_id):
        return self._request("DELETE", f"/users/{user_id}")

    def register(self, payload):
        return self._request("POST", "/register", json=payload)

    def login(self, payload):
        return self._request("POST", "/login", json=payload)
