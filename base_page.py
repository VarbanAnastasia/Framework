from selenium.webdriver.chrome.webdriver import WebDriver

from config import BASE_URL
from framework_mixins.browser_actions_mixins import _BrowserActionsMixin
from framework_mixins.checker_actions_mixin import _CheckerElementsMixin
from framework_mixins.waiter_actions_mixin import _WaiterElementsMixin


class BasePage(_CheckerElementsMixin, _BrowserActionsMixin, _WaiterElementsMixin):
    def __init__(self, driver: WebDriver, url: str = BASE_URL):
        self._driver = driver
        self.url = url

        _CheckerElementsMixin.__init__(self, driver=self._driver)
        _BrowserActionsMixin.__init__(self, driver=self._driver, url=self.url)
        _WaiterElementsMixin.__init__(self, driver=self._driver)

    @property
    def driver(self) -> WebDriver:
        return self._driver

