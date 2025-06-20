import allure
import sys
from pathlib import Path

# Явно добавляем путь к модулям
sys.path.insert(0, str(Path(__file__).parent.resolve()))
from helpers import ApiClient
from .conftest import registered_user




@allure.feature("Авторизация пользователя")
class TestUserAuth:
    @allure.title("Успешная авторизация")
    def test_login_success(self, registered_user, api_client):
        response = api_client.login_user({
            "email": registered_user["email"],
            "password": registered_user["password"]
        })
        assert response.status_code == 200
        assert "accessToken" in response.json()

    @allure.title("Неверные учетные данные")
    def test_login_failure(self, registered_user, api_client):
        response = api_client.login_user({
            "email": registered_user["email"],
            "password": "wrong_password"
        })
        assert response.status_code == 401