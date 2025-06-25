import allure
import sys
from pathlib import Path
from .helpers import ApiClient

# Явно добавляем путь к модулям
sys.path.insert(0, str(Path(__file__).parent.resolve()))
from .conftest import registered_user




@allure.feature("Авторизация пользователя")
class TestUserAuth:
    @allure.title("Успешная авторизация")
    def test_login_success(self, registered_user):
        with allure.step("Создание API клиента"):
            client = ApiClient()

        with allure.step("Подготовка валидных учетных данных"):
            credentials = {
                "email": registered_user["email"],
                "password": registered_user["password"]
            }
            allure.attach(str(credentials), name="Credentials", attachment_type=allure.attachment_type.JSON)

        with allure.step("Отправка запроса на авторизацию"):
            response = client.login_user(credentials)
            allure.attach(str(response.json()), name="Response", attachment_type=allure.attachment_type.JSON)

        with allure.step("Проверка ответа"):
            assert response.status_code == 200
            assert "accessToken" in response.json()

    @allure.title("Неверные учетные данные")
    def test_login_failure(self, registered_user):
        with allure.step("Создание API клиента"):
            client = ApiClient()

        with allure.step("Подготовка невалидных учетных данных"):
            invalid_credentials = {
                "email": registered_user["email"],
                "password": "wrong_password"
            }
            allure.attach(str(invalid_credentials), name="Invalid Credentials", attachment_type=allure.attachment_type.JSON)

        with allure.step("Отправка запроса с неверным паролем"):
            response = client.login_user(invalid_credentials)
            allure.attach(str(response.json()), name="Error Response", attachment_type=allure.attachment_type.JSON)

        with allure.step("Проверка ошибки авторизации"):
            assert response.status_code == 401