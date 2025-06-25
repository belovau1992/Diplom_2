import requests
import random
import string


class ApiClient:
    BASE_URL = "https://stellarburgers.nomoreparties.site/api"

    def __init__(self):
        self.session = requests.Session()
        self.token = None

    def register_user(self, data):
        return self._post("/auth/register", data)

    def login_user(self, data):
        response = self._post("/auth/login", data)
        if response.status_code == 200:
            self.token = response.json().get("accessToken")
        return response

    def create_order(self, ingredients):
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return self._post("/orders", {"ingredients": ingredients}, headers)

    def _post(self, endpoint, data, headers=None):
        url = f"{self.BASE_URL}{endpoint}"
        default_headers = {"Content-Type": "application/json"}
        if headers:
            default_headers.update(headers)
        return self.session.post(url, json=data, headers=default_headers)


def generate_user_data():
    random_str = ''.join(random.choices(string.ascii_lowercase, k=6))
    return {
        "email": f"test_{random_str}@example.com",
        "password": f"password_{random_str}",
        "name": f"User_{random_str}"
    }