import requests
import allure

@allure.title("Проверка, что GET-запрос возвращает 200")
@allure.feature("HTTP-запросы")
def test_get_status_code():
    """Проверка, что запрос возвращает 200"""
    response = requests.get("https://petstore.swagger.io/v2/pet/findByStatus")
    assert response.status_code == 200
