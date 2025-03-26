from venv import logger

from selenium.webdriver.chrome.webdriver import WebDriver


class _BrowserActionsMixin:
    def __init__(self, driver: WebDriver, url: str):
        self._driver = driver
        self.url = url

    @property
    def get(self) -> WebDriver:
        logger.info(f'Открытие страницы {self.url}')
        self._driver.get(self.url)
        logger.info(f'Страница {self.url} открыта!')
        return self._driver