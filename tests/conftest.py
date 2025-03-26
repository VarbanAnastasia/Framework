import pytest
from selenium import webdriver


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


@pytest.fixture
def open_page(driver):
    driver.get('https://spongebob-squarepants-lordfilm.ru/')
    yield driver
    driver.quit()
