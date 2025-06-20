import allure
import pytest
from .helpers import generate_user_data
from .conftest import api_client


@allure.feature("Регистрация пользователя")
class TestUserRegistration:
    @allure.title("Регистрация нового пользователя")
    def test_register_new_user(self, api_client):
        user = generate_user_data()
        response = api_client.register_user(user)
        assert response.status_code == 200
        assert "accessToken" in response.json()

    @allure.title("Регистрация существующего пользователя")
    def test_register_existing_user(self, registered_user, api_client):
        response = api_client.register_user(registered_user)
        assert response.status_code == 403
        assert "User already exists" in response.json()["message"]

    @allure.title("Регистрация без обязательного поля")
    @pytest.mark.parametrize("field", ["email", "password", "name"])
    def test_register_missing_field(self, field, api_client):
        user = generate_user_data()
        user.pop(field)
        response = api_client.register_user(user)
        assert response.status_code == 403