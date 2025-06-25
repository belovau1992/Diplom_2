import pytest
import requests
from .helpers import ApiClient, generate_user_data

BASE_URL = "https://stellarburgers.nomoreparties.site/api"


def pytest_configure():
    """Конфигурация pytest с настройкой Allure"""
    pytest.allure_dir = "allure-results"


@pytest.fixture(autouse=True)
def configure_pytest(request):
    """Автоматическая настройка для всех тестов"""
    request.config.option.alluredir = pytest.allure_dir

@pytest.fixture
def registered_user():
    """
    Фикстура для регистрации пользователя с автоматической очисткой.
    Возвращает словарь с данными пользователя и токеном.
    """
    client = ApiClient()
    user_data = generate_user_data()
    response = client.register_user(user_data)

    if response.status_code != 200:
        pytest.fail(f"Failed to register test user: {response.text}")

    auth_token = response.json().get("accessToken")
    user_data["auth_token"] = auth_token

    yield user_data

    # Пост-обработка: очистка тестовых данных
    cleanup_user_data(user_data)


@pytest.fixture
def authorized_client(registered_user):
    """Фикстура для авторизованного клиента"""
    client = ApiClient()
    response = client.login_user({
        "email": registered_user["email"],
        "password": registered_user["password"]
    })

    if response.status_code != 200:
        pytest.fail(f"Failed to login test user: {response.text}")

    return client


@pytest.fixture
def available_ingredients():
    """Фикстура для получения доступных ингредиентов"""
    try:
        response = requests.get(f"{BASE_URL}/ingredients", timeout=5)
        if response.status_code == 200:
            return [ingredient["_id"] for ingredient in response.json()["data"]]
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to get ingredients: {str(e)}")

        # Fallback тестовые ингредиенты
        return [
            "60d3b41abdacab0026a733c6",  # Флюоресцентная булка
            "60d3b41abdacab0026a733c7",  # Мясо бессмертных моллюсков
        ]


def cleanup_user_data(user_data):
    """Функция для очистки тестовых данных пользователя"""
    if not user_data.get("auth_token"):
        return

    headers = {"Authorization": f"Bearer {user_data['auth_token']}"}

    try:
        # 1. Выход из системы (инвалидация токена)
        requests.post(
            f"{BASE_URL}/auth/logout",
            headers=headers,
            timeout=3
        )

        # 2. Удаление пользователя
        requests.delete(
            f"{BASE_URL}/auth/user",
            headers=headers,
            timeout=3
        )
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Cleanup failed: {str(e)}")
