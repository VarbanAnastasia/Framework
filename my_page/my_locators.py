from base_page import BasePage
from web.locator import Locator

class MyLocators:
    NEW_LOCATOR = Locator(
        name='Новый локатор',
        locator=('xpath', '//div[@class="orangehrm-login-layout"]'),
    )