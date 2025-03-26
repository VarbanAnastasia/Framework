from venv import logger

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from framework_mixins.element_actions_mixin import _ElementActionsMixin


class _WaiterElementsMixin(_ElementActionsMixin):
    def __init__(self, driver: WebDriver):
        super().__init__(driver=driver)

    def wait_for_url_to_contains(self, expected_str: str, timeout: int = 15):
        try:
            logger.info(f'Ожидание присутствия {expected_str} в URL страницы в течение {timeout} секунд')
            WebDriverWait(driver=self._driver, timeout=timeout).until(
                EC.url_contains(expected_str)
            )
            logger.info(f'URL страницы содержит {expected_str} в течение {timeout} секунд')
        except TimeoutException as ex:
            logger.error(msg := f'Не удалось найти {expected_str} в URL страницы в течение {timeout} секунд')