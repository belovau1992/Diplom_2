import allure
import pytest
from .helpers import generate_user_data, ApiClient


@allure.feature("Регистрация пользователя")
class TestUserRegistration:
    @allure.title("Регистрация нового пользователя")
    def test_register_new_user(self):
        with allure.step("Создание API клиента"):
            client = ApiClient()

        with allure.step("Подготовка тестовых данных"):
            user = generate_user_data()
            allure.attach(str(user), name="User Data", attachment_type=allure.attachment_type.JSON)

        with allure.step("Отправка запроса на регистрацию"):
            response = client.register_user(user)
            allure.attach(str(response.json()), name="Response", attachment_type=allure.attachment_type.JSON)

        with allure.step("Проверка ответа"):
            assert response.status_code == 200
            assert "accessToken" in response.json()

    @allure.title("Регистрация существующего пользователя")
    def test_register_existing_user(self, registered_user):
        with allure.step("Создание API клиента"):
            client = ApiClient()

        with allure.step("Повторная регистрация пользователя"):
            response = client.register_user(registered_user)
            allure.attach(str(response.json()), name="Error Response", attachment_type=allure.attachment_type.JSON)

        with allure.step("Проверка ошибки"):
            assert response.status_code == 403
            assert "User already exists" in response.json()["message"]


    @allure.title("Регистрация без обязательного поля")
    @pytest.mark.parametrize("field", ["email", "password", "name"])
    def test_register_missing_field(self, field):
        with allure.step("Создание API клиента"):
            client = ApiClient()

        with allure.step("Подготовка данных без обязательного поля"):
            user = generate_user_data()
            user.pop(field)
            allure.attach(str(user), name="Invalid Data", attachment_type=allure.attachment_type.JSON)

        with allure.step("Отправка невалидного запроса"):
            response = client.register_user(user)
            allure.attach(str(response.status_code), name="Status Code", attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверка ошибки валидации"):
            assert response.status_code == 403