from venv import logger

from selenium.webdriver.chrome.webdriver import WebDriver

from framework_mixins.element_actions_mixin import _ElementActionsMixin
from web.locator import Locator



class _CheckerElementsMixin(_ElementActionsMixin):
    def __init__(self, driver: WebDriver):
        _ElementActionsMixin.__init__(self, driver=driver)

    def is_displayed_by_locator(self, locator: Locator, timeout=15) -> bool:
        try:
            element = self.find_element(locator=locator, timeout=timeout)

            if not (result := element.is_displayed()):
                logger.info('Элемент найден, но значение атрибута isdisplayed = False')

            return result

        except Exception:
            logger.info(f'Элемент {locator} не отображен или не существует! {timeout}')
            return False
