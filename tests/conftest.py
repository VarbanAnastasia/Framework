import pytest
from selenium import webdriver

from config import BASE_URL


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


@pytest.fixture
def open_page(driver):
    driver.get(BASE_URL)
    yield driver
