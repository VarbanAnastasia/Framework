from base_page import BasePage
from web.locator import Locator

class MyLocators:
    NEW_LOCATOR = Locator(
        name='Новый локатор',
        locator=('XPATH', '(//div[@class="header-text text-color"])[1]'),
    )