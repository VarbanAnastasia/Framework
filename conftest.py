import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from loguru import logger
from config import BASE_URL


@pytest.fixture
def driver(request):
    env = request.config.getini("env")

    options = Options()
    options.add_argument("--window-size=1920,1080")

    if env == "selenoid":
        logger.info("🚀 Запуск в Selenoid")
        logger.info("🌐 Статус: http://localhost:4444/status")
        logger.info("🖥 UI: http://localhost:8080")

        options.set_capability("browserName", "chrome")
        options.set_capability("browserVersion", "116.0")
        options.set_capability("selenoid:options", {
            "enableVNC": True,
            "enableVideo": False
        })
        driver = webdriver.Remote(
            command_executor="http://localhost:4444",
            options=options
        )


    else:
        logger.info("✅ Запуск локального Chrome")
        driver = webdriver.Chrome(options=options)

    yield driver
    driver.quit()


@pytest.fixture
def open_page(driver):
    logger.info(f"🌍 Переход на страницу: {BASE_URL}")
    driver.get(BASE_URL)
    yield driver


def pytest_addoption(parser):
    parser.addini("env", "Окружение: local или selenoid", default="local")
