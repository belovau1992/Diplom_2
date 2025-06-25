import allure
import sys
from pathlib import Path

# Явно добавляем путь к модулям
sys.path.insert(0, str(Path(__file__).parent.resolve()))

from .helpers import ApiClient
from .conftest import authorized_client, available_ingredients


@allure.feature("Работа с заказами")
class TestOrders:
    @allure.title("Создание заказа с авторизацией")
    def test_create_order_authenticated(self, authorized_client, available_ingredients):
        with allure.step("Подготовка тестовых данных"):
            test_ingredients = available_ingredients[:2]
            allure.attach(str(test_ingredients), name="Ингредиенты", attachment_type=allure.attachment_type.TEXT)

        with allure.step("Отправка запроса на создание заказа"):
            response = authorized_client.create_order(test_ingredients)
            allure.attach(str(response.json()), name="Ответ API", attachment_type=allure.attachment_type.JSON)

        with allure.step("Проверка ответа"):
            assert response.status_code == 200
            assert "order" in response.json()

    @allure.title("Создание заказа без авторизации")
    def test_create_order_unauthenticated(self, available_ingredients):
        with allure.step("Создание API клиента"):
            client = ApiClient()  # Создаём клиент напрямую

        with allure.step("Подготовка тестовых данных"):
            test_ingredients = available_ingredients[:2]

        with allure.step("Отправка запроса без авторизации"):
            response = client.create_order(test_ingredients)
            allure.attach(str(response.status_code), name="Status Code", attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверка успешного создания"):
            assert response.status_code == 200

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_empty_ingredients(self, authorized_client):
        with allure.step("Отправка запроса с пустым списком ингредиентов"):
            response = authorized_client.create_order([])
            allure.attach(str(response.json()), name="Error Response", attachment_type=allure.attachment_type.JSON)

        with allure.step("Проверка ошибки валидации"):
            assert response.status_code == 400
            assert "Ingredient ids must be provided" in response.json()["message"]