import allure
import sys
from pathlib import Path

# Явно добавляем путь к модулям
sys.path.insert(0, str(Path(__file__).parent.resolve()))

from helpers import ApiClient
from .conftest import api_client
from .conftest import authorized_client, available_ingredients




@allure.feature("Работа с заказами")
class TestOrders:
    @allure.title("Создание заказа с авторизацией")
    def test_create_order_authenticated(self, authorized_client, available_ingredients):
        response = authorized_client.create_order(available_ingredients[:2])
        assert response.status_code == 200
        assert "order" in response.json()

    @allure.title("Создание заказа без авторизации")
    def test_create_order_unauthenticated(self, api_client, available_ingredients):
        response = api_client.create_order(available_ingredients[:2])
        assert response.status_code == 200

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_empty_ingredients(self, authorized_client):
        response = authorized_client.create_order([])
        assert response.status_code == 400
        assert "Ingredient ids must be provided" in response.json()["message"]