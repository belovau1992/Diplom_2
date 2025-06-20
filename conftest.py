import pytest
import requests
from .helpers import ApiClient, generate_user_data

BASE_URL = "https://stellarburgers.nomoreparties.site/api"


def pytest_configure():
    """Конфигурация pytest с настройкой Allure"""
    pytest.allure_dir = "allure-results"
    pytest.registered_users = []


@pytest.fixture(autouse=True)
def configure_pytest(request):
    """Автоматическая настройка для всех тестов"""
    request.config.option.alluredir = pytest.allure_dir


@pytest.fixture
def api_client():
    """Фикстура для создания API клиента"""
    return ApiClient()


@pytest.fixture
def registered_user(api_client):
    """
    Фикстура для регистрации пользователя с автоматической очисткой.
    Возвращает словарь с данными пользователя и токеном.
    """
    user_data = generate_user_data()
    response = api_client.register_user(user_data)

    if response.status_code != 200:
        pytest.fail(f"Failed to register test user: {response.text}")

    auth_token = response.json().get("accessToken")
    user_data["auth_token"] = auth_token
    pytest.registered_users.append(user_data.copy())

    yield user_data

    # Пост-обработка: очистка тестовых данных
    cleanup_user_data(user_data)


@pytest.fixture
def authorized_client(registered_user, api_client):
    """Фикстура для авторизованного клиента"""
    api_client.login_user({
        "email": registered_user["email"],
        "password": registered_user["password"]
    })
    return api_client


@pytest.fixture
def available_ingredients():
    """Фикстура для получения доступных ингредиентов"""
    try:
        response = requests.get(f"{BASE_URL}/ingredients", timeout=5)
        if response.status_code == 200:
            return [ingredient["_id"] for ingredient in response.json()["data"]]
    except requests.exceptions.RequestException:
        # Fallback тестовые ингредиенты
        pass

    return [
        "60d3b41abdacab0026a733c6",  # Флюоресцентная булка
        "60d3b41abdacab0026a733c7",  # Мясо бессмертных моллюсков
    ]


def cleanup_user_data(user_data):
    """Функция для очистки тестовых данных пользователя"""
    if not user_data.get("auth_token"):
        return

    headers = {"Authorization": f"Bearer {user_data['auth_token']}"}

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


def pytest_sessionfinish(session, exitstatus):
    """Очистка оставшихся пользователей после всех тестов"""
    for user in pytest.registered_users:
        cleanup_user_data(user)